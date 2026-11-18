"""
Build small, self-contained demo files for the results viewer (app/app.py).

For each dataset, one seed (1989): calibration + test images, GT, hard and soft
predictions, exactly the splits used in run_extension.py.

  demo/wbc.npz, demo/oasis.npz   (~5 MB each, from benchmarks/cache)
  demo/polyps.npz                (~60 MB, 200 calib + 200 test images)

Memory: polyps loading peaks at ~2.7 GB. Run it capped:
  scripts/safe_run.sh -m 6G .venv/bin/python experiments/extension/make_demo_bundle.py
"""

import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / "benchmarks" / "cache"
OUT = ROOT / "demo"
SEED = 1989


def save(name, splits):
    OUT.mkdir(exist_ok=True)
    arrays = {}
    for split, (imgs, gts, hards, softs) in splits.items():
        imgs = np.asarray(imgs)
        if imgs.dtype != np.uint8:  # store images as uint8 (display + resistance maps)
            imgs = np.clip(np.round(imgs * 255), 0, 255).astype(np.uint8)
        arrays[f"{split}_images"] = imgs
        arrays[f"{split}_gts"] = np.asarray(gts, dtype=np.uint8)
        arrays[f"{split}_hards"] = np.asarray(hards, dtype=np.uint8)
        arrays[f"{split}_softs"] = np.asarray(softs, dtype=np.float16)
    np.savez_compressed(OUT / f"{name}.npz", seed=SEED, **arrays)
    print(f"saved {OUT / name}.npz  ({(OUT / f'{name}.npz').stat().st_size / 1e6:.1f} MB)")


def universeg(ds):
    base = np.load(CACHE / ds / "base.npz")
    z = np.load(CACHE / ds / f"seed_{SEED}.npz")
    splits = {}
    for split in ["calib", "test"]:
        idx = z[f"idx_{split}"]
        splits[split] = (base["images"][idx], base["gts"][idx], z[f"hard_{split}"],
                         z[f"soft_{split}"])
    save(ds, splits)


def polyps():
    sys.path.insert(0, str(ROOT / "experiments" / "extension"))
    from run_extension import load_polyps

    ids, images, gts, hards, softs = load_polyps()
    perm = np.random.default_rng(SEED).permutation(len(ids))  # same as run_extension
    sl = dict(calib=perm[100:300], test=perm[300:])
    save("polyps", {k: ([images[i] for i in v], [gts[i] for i in v], [hards[i] for i in v],
                        [softs[i] for i in v]) for k, v in sl.items()})


if __name__ == "__main__":
    for ds in ["wbc", "oasis"]:
        universeg(ds)
    polyps()
