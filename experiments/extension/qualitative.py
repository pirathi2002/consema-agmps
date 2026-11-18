"""
Qualitative comparison: paper margin vs AG-MPS margin on the same test images.

For one seed, calibrates both methods on the calibration split and draws, for
a few test images: input | GT vs prediction | paper set | AG-MPS set.
Colours as in the paper: purple = true positive, red = missed GT pixel
(false negative), light blue = conformal margin, orange = FN recovered.

Usage:
  .venv/bin/python experiments/extension/qualitative.py --dataset wbc \
      --kind region --beta 4 --gamma 0.5
"""

import argparse
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from consema.extension.cp import build_record, conformal_quantile, scores_of, size_scale  # noqa: E402
from consema.extension.distances import distance_map  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / "benchmarks" / "cache"
FIGS = ROOT / "figures" / "extension"


def overlay(gt, pred, cset=None):
    h, w = gt.shape
    rgb = np.ones((h, w, 3))
    if cset is not None:
        rgb[cset & ~pred] = (0.68, 0.85, 0.95)  # margin
        rgb[cset & ~pred & gt] = (1.0, 0.6, 0.0)  # FN recovered
    rgb[pred & ~gt] = (0.35, 0.55, 0.9)  # false positive
    rgb[pred & gt] = (0.5, 0.2, 0.6)  # true positive
    missed = gt & ~pred if cset is None else gt & ~cset
    rgb[missed] = (0.9, 0.1, 0.1)  # missed GT
    return rgb


def load(dataset, seed):
    if dataset == "polyps":
        from run_extension import load_polyps

        ids, images, gts, hards, softs = load_polyps()
        perm = np.random.default_rng(seed).permutation(len(ids))
        sl = dict(calib=perm[100:300], test=perm[300:])
        return {k: ([images[i] for i in v], [gts[i] for i in v], [hards[i] for i in v],
                    [softs[i] for i in v]) for k, v in sl.items()}
    base = np.load(CACHE / dataset / "base.npz")
    z = np.load(CACHE / dataset / f"seed_{seed}.npz")
    out = {}
    for k in ["calib", "test"]:
        idx = z[f"idx_{k}"]
        out[k] = (list(base["images"][idx]), list(base["gts"][idx]), list(z[f"hard_{k}"]),
                  list(z[f"soft_{k}"].astype(np.float32)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="wbc")
    ap.add_argument("--seed", type=int, default=1989)
    ap.add_argument("--kind", default="region")
    ap.add_argument("--beta", type=float, default=4.0)
    ap.add_argument("--gamma", type=float, default=0.5)
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--tau", type=float, default=0.99)
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()

    data = load(args.dataset, args.seed)
    methods = {"paper": ("uniform", 0.0, 0.0), "AG-MPS": (args.kind, args.beta, args.gamma)}

    dmaps, qs = {}, {}
    for name, (kind, beta, gamma) in methods.items():
        for split in ["calib", "test"]:
            im, gt, hd, sf = data[split]
            dmaps[name, split] = [distance_map(h.astype(bool), kind, beta, image=i, soft_pred=s)
                                  for i, h, s in zip(im, hd, sf)]
        recs = [build_record(d, g, h) for d, g, h in zip(dmaps[name, "calib"], *data["calib"][1:3])]
        qs[name] = conformal_quantile(scores_of(recs, args.tau, gamma), args.alpha)

    im, gts, hds, _ = data["test"]
    # pick images where the baseline margin is large relative to the object
    order = np.argsort([-(dm <= qs["paper"]).sum() / max(h.sum(), 1)
                        for dm, h in zip(dmaps["paper", "test"], hds)])
    picks = order[1 : 1 + args.n]

    fig, axes = plt.subplots(len(picks), 4, figsize=(11, 2.8 * len(picks)), squeeze=False)
    for r, i in enumerate(picks):
        gt, pred = gts[i].astype(bool), hds[i].astype(bool)
        img = np.squeeze(im[i])
        axes[r, 0].imshow(img, cmap=None if img.ndim == 3 else "gray")
        axes[r, 1].imshow(overlay(gt, pred))
        for c, name in [(2, "paper"), (3, "AG-MPS")]:
            kind, beta, gamma = methods[name]
            lam = qs[name] * size_scale(pred.sum(), gamma)
            cset = dmaps[name, "test"][i] <= lam
            cov = (cset & gt).sum() / gt.sum()
            axes[r, c].imshow(overlay(gt, pred, cset))
            axes[r, c].set_title(f"{name}: stretch {cset.sum()/pred.sum():.2f}, "
                                 f"cov {cov:.3f}", fontsize=9)
        axes[r, 0].set_title("input", fontsize=9)
        axes[r, 1].set_title("GT vs prediction", fontsize=9)
        for a in axes[r]:
            a.axis("off")
    k, b, g = methods["AG-MPS"]
    fig.suptitle(f"{args.dataset}, 1-α={1-args.alpha:.2f}, τ={args.tau}; AG-MPS: {k}, β={b}, γ={g}")
    fig.tight_layout()
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / f"qualitative_{args.dataset}{args.tag}.png"
    fig.savefig(out, dpi=140)
    print("saved", out)


if __name__ == "__main__":
    main()
