"""
Run the paper baseline and the AG-MPS extension on WBC, OASIS (UniverSeg) and
Polyps (PraNet), 36 random seeds, all (alpha, tau) settings of Table 1.

For every seed we evaluate a grid of configurations
    kind  in {uniform, region, edge, sigmoid}    (resistance map, E1)
    beta  in BETAS                               (strength of the resistance)
    gamma in GAMMAS                              (size-adaptivity, E2)
and log, for each, the *tuning-set* objective (mean stretch) and the
calibration -> test metrics. Model selection happens afterwards
(analyze_results.py) using only the tuning-set columns.

Splits
  WBC / OASIS : calibration (50) and test (rest) are EXACTLY the paper's;
                tuning = support-split images not used as UniverSeg context.
  Polyps      : paper protocol 250/250 for the reproduction rows; for the
                extension rows: tune 100 / calib 200 / test 200 per seed
                (baseline is re-run on the same 200/200 for a fair comparison).

Usage: .venv/bin/python experiments/extension/run_extension.py --dataset wbc
"""

import argparse
import itertools
import os
import pathlib

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm

from consema.extension.distances import distance_map, resistance_map
from consema.extension.cp import (
    build_record,
    conformal_quantile,
    evaluate,
    scores_of,
)

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / "benchmarks" / "cache"
POLYPS = ROOT / "benchmarks" / "polyps_precomputed" / "data" / "polyps"
RESULTS = ROOT / "results" / "extension"

SEEDS = list(range(1989, 2025))
ALPHAS = [0.1, 0.05]
TAUS = [0.9, 0.99, 0.999]
BETAS = [0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256]
GAMMAS = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
KINDS = ["region", "edge", "sigmoid"]
CONFIGS = [("uniform", 0.0)] + [(k, b) for k in KINDS for b in BETAS]


# --------------------------------------------------------------------------- #
#  Per-image records for every (kind, beta)
# --------------------------------------------------------------------------- #
def image_records(image, gt, hard, soft, configs=CONFIGS):
    gt = np.asarray(gt).astype(bool)
    hard = np.asarray(hard).astype(bool)
    out = {}
    res_cache = {}
    for kind, beta in configs:
        if kind != "uniform" and kind not in res_cache:
            res_cache[kind] = resistance_map(kind, hard, image=image, soft_pred=soft)
        d = distance_map(hard, kind, beta, resistance=res_cache.get(kind))
        out[(kind, beta)] = build_record(d, gt, hard)
    return out


def records_for(images, gts, hards, softs, n_jobs, configs=CONFIGS):
    recs = Parallel(n_jobs=n_jobs)(
        delayed(image_records)(im, g, h, s, configs)
        for im, g, h, s in zip(images, gts, hards, softs)
    )
    return recs  # list (per image) of dict[(kind, beta)] -> ImageRecord


# --------------------------------------------------------------------------- #
#  Evaluation of one seed
# --------------------------------------------------------------------------- #
def size_terciles(calib_recs):
    sizes = np.array([r.n_pred for r in calib_recs])
    return np.quantile(sizes, [1 / 3, 2 / 3])


def eval_split(tune, calib, test, meta, paper_index=False, gammas=GAMMAS, configs=CONFIGS):
    rows = []
    for (kind, beta), gamma, alpha, tau in itertools.product(configs, gammas, ALPHAS, TAUS):
        key = (kind, beta)
        t_recs = [r[key] for r in tune] if tune is not None else None
        c_recs = [r[key] for r in calib]
        s_recs = [r[key] for r in test]

        row = dict(**meta, kind=kind, beta=beta, gamma=gamma, alpha=alpha, tau=tau,
                   paper_index=paper_index, n_calib=len(c_recs), n_test=len(s_recs))
        if t_recs is not None:
            qt = conformal_quantile(scores_of(t_recs, tau, gamma), alpha)
            ev_t = evaluate(t_recs, qt, tau, gamma)
            row.update(tune_stretch=ev_t["mean_stretch"], tune_coverage=ev_t["coverage"])

        q = conformal_quantile(scores_of(c_recs, tau, gamma), alpha, paper_index=paper_index)
        ev = evaluate(s_recs, q, tau, gamma)
        row.update(q_hat=q, coverage=ev["coverage"], stretch=ev["mean_stretch"],
                   median_stretch=ev["median_stretch"], added_pixels=ev["added_pixels"],
                   mean_lambda=ev["mean_lambda"])

        # conditional coverage / stretch by predicted-object size (terciles from calib)
        t1, t2 = size_terciles(c_recs)
        n_pred = np.array([r.n_pred for r in s_recs])
        groups = np.digitize(n_pred, [t1, t2])  # 0 small, 1 medium, 2 large
        for g, name in enumerate(["small", "medium", "large"]):
            m = groups == g
            row[f"cov_{name}"] = float(ev["covered"][m].mean()) if m.any() else np.nan
            row[f"stretch_{name}"] = float(ev["stretch"][m].mean()) if m.any() else np.nan
        rows.append(row)
    return rows


# --------------------------------------------------------------------------- #
#  Datasets
# --------------------------------------------------------------------------- #
def run_universeg(dataset, n_jobs, seeds):
    base = np.load(CACHE / dataset / "base.npz")
    images, gts = base["images"], base["gts"]
    rows = []
    for seed in tqdm(seeds, desc=dataset):
        z = np.load(CACHE / dataset / f"seed_{seed}.npz")
        recs = {}
        for split in ["tune", "calib", "test"]:
            idx = z[f"idx_{split}"]
            soft = z[f"soft_{split}"].astype(np.float32)
            hard = z[f"hard_{split}"]
            recs[split] = records_for(images[idx], gts[idx], hard, soft, n_jobs)
        meta = dict(dataset=dataset, seed=seed, protocol="extension")
        rows += eval_split(recs["tune"], recs["calib"], recs["test"], meta)
        # paper reproduction: same calib/test, uniform, official quantile index
        meta = dict(dataset=dataset, seed=seed, protocol="paper")
        rows += eval_split(None, recs["calib"], recs["test"], meta, paper_index=True,
                           gammas=[0.0], configs=[("uniform", 0.0)])
    return rows


def _npz_memmap(npz_path, key):
    """Memory-map an uncompressed .npz member (same as benchmarkerie.datasets.npz_memmap;
    duplicated so joblib workers don't import torch via benchmarkerie)."""
    import struct
    import zipfile
    from numpy.lib import format as npf

    with zipfile.ZipFile(npz_path) as zf:
        info = zf.getinfo(f"{key}.npy")
    if info.compress_type != zipfile.ZIP_STORED:
        return np.load(npz_path)[key]
    with open(npz_path, "rb") as fh:
        fh.seek(info.header_offset)
        name_len, extra_len = struct.unpack("<HH", fh.read(30)[26:30])
        fh.seek(info.header_offset + 30 + name_len + extra_len)
        version = npf.read_magic(fh)
        read_header = (
            npf.read_array_header_1_0 if version == (1, 0) else npf.read_array_header_2_0
        )
        shape, fortran, dtype = read_header(fh)
        offset = fh.tell()
    return np.memmap(npz_path, dtype=dtype, mode="r", shape=shape,
                     order="F" if fortran else "C", offset=offset)


def load_polyps():
    import matplotlib.pyplot as plt
    from skimage.transform import resize

    npz = POLYPS / "polyps-pranet.npz"
    # memory-map the 1.8 GB arrays instead of loading them (only 500 rows used)
    sgmd, targets = _npz_memmap(npz, "sgmd"), _npz_memmap(npz, "targets")
    ids = [int(e) for e in np.load(npz)["example_indexes"]]
    softs, hards, gts, images = [], [], [], []
    for i in ids:
        s = sgmd[i].astype(np.float64)
        s = (s - s.min()) / (s.max() - s.min())  # same rescaling as the paper
        softs.append(s.astype(np.float32))
        hards.append(s.round().clip(0, 1).astype(np.uint8))
        gts.append((targets[i] > 0.5).astype(np.uint8))
        img = plt.imread(POLYPS / "examples" / f"{i}.jpg")
        images.append(resize(img, s.shape + (img.shape[-1],), anti_aliasing=True))
    return ids, images, gts, hards, softs


def run_polyps(n_jobs, seeds):
    ids, images, gts, hards, softs = load_polyps()
    keep = [i for i in range(len(ids)) if hards[i].any() and gts[i].any()]
    print(f"polyps: {len(ids)} images, {len(keep)} with non-empty prediction and GT")
    pool = np.array(keep)
    perms = {seed: np.random.default_rng(seed).permutation(pool) for seed in seeds}
    rows = []
    # 352x352 images: process one (kind, beta) at a time to bound memory
    for cfg in tqdm(CONFIGS, desc="polyps configs"):
        recs_all = records_for(images, gts, hards, softs, n_jobs, configs=[cfg])
        for seed in seeds:
            perm = perms[seed]
            if cfg == ("uniform", 0.0):  # paper protocol 50/50 calib/test
                half = len(perm) // 2
                cal = [recs_all[i] for i in perm[:half]]
                test = [recs_all[i] for i in perm[half:]]
                rows += eval_split(None, cal, test,
                                   dict(dataset="polyps", seed=seed, protocol="paper"),
                                   paper_index=True, gammas=[0.0], configs=[cfg])
            # extension protocol: tune / calib / test = 100 / 200 / rest
            tune = [recs_all[i] for i in perm[:100]]
            cal = [recs_all[i] for i in perm[100:300]]
            test = [recs_all[i] for i in perm[300:]]
            rows += eval_split(tune, cal, test,
                               dict(dataset="polyps", seed=seed, protocol="extension"),
                               configs=[cfg])
        del recs_all
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=["wbc", "oasis", "polyps"], required=True)
    ap.add_argument("--n_jobs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--seeds", type=int, nargs="*", default=SEEDS)
    args = ap.parse_args()

    RESULTS.mkdir(parents=True, exist_ok=True)
    if args.dataset == "polyps":
        rows = run_polyps(args.n_jobs, args.seeds)
    else:
        rows = run_universeg(args.dataset, args.n_jobs, args.seeds)
    df = pd.DataFrame(rows)
    out = RESULTS / f"raw_{args.dataset}.csv"
    df.to_csv(out, index=False)
    print(f"saved {len(df)} rows -> {out}")


if __name__ == "__main__":
    main()
