"""
Cache UniverSeg predictions for WBC / OASIS for every random seed of the paper.

Exactly follows the paper's protocol (experiments/experiments.py):
  - ExtendedWBCDataset / ExtendedOASISDataset splits (support / calibration / test)
  - 24 support (context) images taken from the support split
  - label "nucleus" for WBC, label 0 for OASIS
  - hard prediction = round(sigmoid)

Addition for the extension: a *tuning* set (support-split images that are NOT
used as UniverSeg context) which is disjoint from calibration and test data.
It is used only to choose the extension's hyper-parameters (beta, gamma,
resistance type), so the conformal guarantee on calib/test is untouched.

Output: benchmarks/cache/{dataset}/base.npz         images + GT for all data
        benchmarks/cache/{dataset}/seed_{s}.npz     indices + sigmoid per split

Usage:  .venv/bin/python experiments/extension/cache_predictions.py --dataset wbc
"""

import argparse
import itertools
import os
import pathlib
import sys

import numpy as np
import torch
from einops import rearrange
from tqdm import tqdm

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "benchmarks" / "data"
CACHE = ROOT / "benchmarks" / "cache"
WEIGHTS = ROOT / "benchmarks" / "weights" / "universeg_v1_nf64_ss64_STA.pt"

# --- keep UniverSeg's data out of /tmp: patch its hard-coded download dirs ---
import example_data.wbc as _wbc  # noqa: E402
import example_data.oasis as _oasis  # noqa: E402

_wbc.require_download_wbc = lambda: DATA / "universeg_wbc"
_oasis.require_download_oasis = lambda: DATA / "universeg_oasis"

from benchmarkerie.datasets import ExtendedWBCDataset, ExtendedOASISDataset  # noqa: E402
from universeg import universeg  # noqa: E402

SEEDS = list(range(1989, 2025))  # the 36 seeds used in the paper
N_SUPPORT = 24  # "medium performance predictor" (paper setting)
N_TUNE = 100


def load_model(device):
    model = universeg(pretrained=False)
    model.load_state_dict(torch.load(WEIGHTS, map_location=device))
    return model.to(device).eval()


def make_splits(dataset, seed):
    if dataset == "wbc":
        mk = lambda split: ExtendedWBCDataset(  # noqa: E731
            dataset="JTSC", split=split, label="nucleus", random_seed=seed
        )
    else:
        mk = lambda split: ExtendedOASISDataset(  # noqa: E731
            split=split, label=0, random_seed=seed
        )
    return mk("support"), mk("calibration"), mk("test")


@torch.no_grad()
def predict(model, ds, positions, sup_x, sup_y, device, bs=2):
    out = []
    for i in range(0, len(positions), bs):
        chunk = positions[i : i + bs]
        x = torch.stack([ds[j][0] for j in chunk]).to(device)
        b = x.shape[0]
        sx = sup_x[None].expand(b, *sup_x.shape)
        sy = sup_y[None].expand(b, *sup_y.shape)
        logits = model(x, sx, sy)  # (b, 1, H, W)
        out.append(torch.sigmoid(logits)[:, 0].cpu().numpy())
    return np.concatenate(out).astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=["wbc", "oasis"], required=True)
    ap.add_argument("--seeds", type=int, nargs="*", default=SEEDS)
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.set_num_threads(8)
    model = load_model(device)
    out_dir = CACHE / args.dataset
    out_dir.mkdir(parents=True, exist_ok=True)

    for seed in tqdm(args.seeds, desc=args.dataset):
        dst = out_dir / f"seed_{seed}.npz"
        if dst.exists():
            continue
        sup, cal, test = make_splits(args.dataset, seed)

        if not (out_dir / "base.npz").exists():  # images and GT are seed-independent
            imgs = np.stack([x.numpy()[0] for x, _ in sup._data]).astype(np.float32)
            lab = sup._ilabel
            if args.dataset == "wbc":
                gts = np.stack([y.numpy()[lab] for _, y in sup._data]).astype(np.uint8)
            else:
                gts = np.stack([(y.numpy() == lab) for _, y in sup._data]).astype(np.uint8)
            np.savez_compressed(out_dir / "base.npz", images=imgs, gts=gts)

        sx, sy = zip(*itertools.islice(sup, N_SUPPORT))
        sx, sy = torch.stack(sx).to(device), torch.stack(sy).float().to(device)

        tune_pos = list(range(N_SUPPORT, min(len(sup), N_SUPPORT + N_TUNE)))
        cal_pos = list(range(len(cal)))
        test_pos = list(range(len(test)))
        # data indices (into the full dataset) for each split
        idx = dict(
            tune=np.asarray(sup._idxs)[tune_pos],
            calib=np.asarray(cal._idxs)[cal_pos],
            test=np.asarray(test._idxs)[test_pos],
        )
        assert not (set(idx["tune"]) & set(idx["calib"])) and not (
            set(idx["calib"]) & set(idx["test"])
        ) and not (set(idx["tune"]) & set(idx["test"]))
        soft = dict(
            tune=predict(model, sup, tune_pos, sx, sy, device),
            calib=predict(model, cal, cal_pos, sx, sy, device),
            test=predict(model, test, test_pos, sx, sy, device),
        )
        np.savez_compressed(
            dst,
            **{f"idx_{k}": v for k, v in idx.items()},
            **{f"soft_{k}": v.astype(np.float16) for k, v in soft.items()},
            **{f"hard_{k}": v.round().clip(0, 1).astype(np.uint8) for k, v in soft.items()},
        )


if __name__ == "__main__":
    main()
