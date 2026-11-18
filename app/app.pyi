"""
ConSeMa + AG-MPS results viewer (Gradio).

Tab 1  "36-seed results"      : tables/figures from results/extension (precomputed)
Tab 2  "Interactive explorer" : calibrate paper vs AG-MPS live on one seed (demo/*.npz)
Tab 3  "Method"               : short summary for the presentation

Run locally (memory-capped):
    scripts/safe_run.sh -m 4G .venv/bin/python app/app.py
    -> open http://127.0.0.1:7860
In Colab:
    !python app/app.py --share        (prints a public *.gradio.live link)
"""

import argparse
import functools
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import gradio as gr  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "extension"))

from consema.extension.cp import conformal_quantile, size_scale  # noqa: E402
from consema.extension.distances import distance_map, resistance_map  # noqa: E402
from qualitative import overlay  # noqa: E402

RESULTS = ROOT / "results" / "extension"
FIGS = ROOT / "figures" / "extension"
DEMO = ROOT / "demo"
DATASETS = ["wbc", "oasis", "polyps"]
KINDS = ["uniform", "region", "edge", "sigmoid"]
BETAS = [0, 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256]
SETTINGS = ["1-α=0.9, τ=0.9", "1-α=0.9, τ=0.99", "1-α=0.9, τ=0.999",
            "1-α=0.95, τ=0.9", "1-α=0.95, τ=0.99", "1-α=0.95, τ=0.999"]
METHOD_ORDER = ["Paper (baseline)", "E2: size-adaptive", "E1: geodesic (black-box)",
                "AG-MPS (black-box, E1+E2)", "AG-MPS (gray-box, +sigmoid)"]

from gradio.events import Dependency

class SafeSlider(gr.Slider):
    """Slider that accepts numbers arriving as text (e.g. "2.0") from the browser.

    Plain gr.Slider then crashes in Gradio's bounds check with
    "TypeError: '<' not supported between instances of 'str' and 'int'".
    """

    def preprocess(self, payload):
        if isinstance(payload, str):
            payload = float(payload)
        return super().preprocess(payload)
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer
        from gradio.components.base import Component


def parse_setting(s):
    a, t = s.replace("1-α=", "").replace(" τ=", "").split(",")
    return round(1 - float(a), 2), float(t)


# =========================================================================== #
#  Tab 1: precomputed 36-seed results
# =========================================================================== #
@functools.lru_cache(maxsize=1)
def tables():
    return (pd.read_csv(RESULTS / "table_main.csv"),
            pd.read_csv(RESULTS / "table_reproduction.csv"),
            pd.read_csv(RESULTS / "selected_hparams.csv"))


def results_view(ds, setting):
    main, rep, _ = tables()
    alpha, tau = parse_setting(setting)
    m = main[(main.dataset == ds) & np.isclose(main["1-alpha"], 1 - alpha) & (main.tau == tau)]
    m = m.set_index("method").loc[[x for x in METHOD_ORDER if x in set(m.method)]].reset_index()
    m = pd.DataFrame({
        "method": m.method,
        "coverage (target ≥ %.2f)" % (1 - alpha): m.coverage.round(3),
        "mean stretch ↓": m.stretch.round(3),
        "Δ stretch vs paper": m["stretch_vs_paper_%"].map(lambda v: f"{v:+.1f}%"),
        "worst size-group coverage": m.worst_group_cov.round(3),
        "stretch small objects": m.stretch_small.round(3),
        "stretch large objects": m.stretch_large.round(3),
    })
    r = rep[rep.dataset == ds].copy()
    r.columns = [c.replace("lambda", "λ̂") for c in r.columns]
    gallery = [str(p) for p in [FIGS / f"main_stretch_{ds}.png",
                                *sorted(FIGS.glob(f"qualitative_{ds}*.png")),
                                *sorted(FIGS.glob("ablation_*.png")),
                                *sorted(FIGS.glob("conditional_cov_*.png"))] if p.exists()]
    return m, r, gallery


# =========================================================================== #
#  Tab 2: live explorer on the demo split (seed 1989)
# =========================================================================== #
@functools.lru_cache(maxsize=3)
def demo(ds):
    z = np.load(DEMO / f"{ds}.npz")
    out = {}
    for split in ["calib", "test"]:
        out[split] = dict(images=z[f"{split}_images"], gts=z[f"{split}_gts"].astype(bool),
                          hards=z[f"{split}_hards"].astype(bool),
                          softs=z[f"{split}_softs"].astype(np.float32))
    return out


def _dmap(img, hard, soft, kind, beta):
    image = img.astype(np.float32) / 255.0
    if kind == "uniform" or beta == 0:
        return distance_map(hard, "uniform")
    res = resistance_map(kind, hard, image=image, soft_pred=soft)
    return distance_map(hard, kind, beta, resistance=res)


@functools.lru_cache(maxsize=24)
def calib_stats(ds, kind, beta):
    """Per calibration image: sorted D over GT pixels, and |Y_hat|."""
    d = demo(ds)["calib"]
    stats = []
    for img, gt, hard, soft in zip(d["images"], d["gts"], d["hards"], d["softs"]):
        D = _dmap(img, hard, soft, kind, beta)
        stats.append((np.sort(D[gt]).astype(np.float32), int(hard.sum())))
    return stats


@functools.lru_cache(maxsize=4)
def test_dmaps(ds, kind, beta):
    d = demo(ds)["test"]
    return [_dmap(i, h, s, kind, beta).astype(np.float32)
            for i, h, s in zip(d["images"], d["hards"], d["softs"])]


def quantile(ds, kind, beta, gamma, alpha, tau):
    scores = []
    for gt_d, n_pred in calib_stats(ds, kind, beta):
        k = min(max(int(np.ceil(tau * len(gt_d) - 1e-9)), 1), len(gt_d))
        scores.append(gt_d[k - 1] / size_scale(n_pred, gamma))
    return conformal_quantile(scores, alpha)


def evaluate_test(ds, kind, beta, gamma, q, tau):
    d = demo(ds)["test"]
    covs, stretches, sets = [], [], []
    for D, gt, hard in zip(test_dmaps(ds, kind, beta), d["gts"], d["hards"]):
        lam = q * size_scale(hard.sum(), gamma)
        cset = D <= lam
        covs.append((cset & gt).sum() / max(gt.sum(), 1))
        stretches.append(cset.sum() / max(hard.sum(), 1))
        sets.append(cset)
    return np.array(covs), np.array(stretches), sets


def explore(ds, setting, kind, beta, gamma, idx, progress=gr.Progress()):
    alpha, tau = parse_setting(setting)
    beta, gamma, idx = float(beta), float(gamma), int(float(idx))
    methods ={"Paper": ("uniform", 0.0, 0.0), "AG-MPS": (kind, beta, float(gamma))}
    res = {}
    for i, (name, (k, b, g)) in enumerate(methods.items()):
        progress((i + 0.1) / 2, desc=f"calibrating {name} on {ds} (first time can take ~20 s)")
        q = quantile(ds, k, b, g, alpha, tau)
        covs, stretch, sets = evaluate_test(ds, k, b, g, q, tau)
        res[name] = dict(q=q, covs=covs, stretch=stretch, sets=sets)

    d = demo(ds)["test"]
    n = len(d["gts"])
    idx = int(min(idx, n - 1))
    gt, hard, img = d["gts"][idx], d["hards"][idx], d["images"][idx]

    fig, ax = plt.subplots(1, 4, figsize=(15, 4.2))
    ax[0].imshow(img if img.ndim == 3 else img, cmap=None if img.ndim == 3 else "gray")
    ax[0].set_title(f"input (test image {idx})")
    ax[1].imshow(overlay(gt, hard))
    ax[1].set_title("GT vs prediction")
    for j, name in [(2, "Paper"), (3, "AG-MPS")]:
        r = res[name]
        ax[j].imshow(overlay(gt, hard, r["sets"][idx]))
        ok = "✓" if r["covs"][idx] >= tau else "✗"
        ax[j].set_title(f"{name}: stretch {r['stretch'][idx]:.2f}, covered {r['covs'][idx]:.3f} {ok}")
    for a in ax:
        a.axis("off")
    fig.text(0.5, 0.01, "purple = true positive · red = missed GT · light blue = conformal margin · "
             "orange = missed pixel recovered by the margin · blue = false positive",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))

    p, a = res["Paper"], res["AG-MPS"]
    summary = pd.DataFrame({
        "": ["conformal quantile q̂", f"test coverage (target ≥ {1 - alpha:.2f})",
             "mean stretch ↓", "median stretch", "this image: covered fraction",
             "this image: stretch"],
        "Paper (uniform dilation)": [f"{p['q']:.3f}", f"{np.mean(p['covs'] >= tau):.3f}",
                                     f"{p['stretch'].mean():.3f}", f"{np.median(p['stretch']):.3f}",
                                     f"{p['covs'][idx]:.3f}", f"{p['stretch'][idx]:.3f}"],
        f"AG-MPS ({kind}, β={beta:g}, γ={gamma:g})": [
            f"{a['q']:.3f}" + (" (normalised)" if gamma else ""),
            f"{np.mean(a['covs'] >= tau):.3f}", f"{a['stretch'].mean():.3f}",
            f"{np.median(a['stretch']):.3f}", f"{a['covs'][idx]:.3f}", f"{a['stretch'][idx]:.3f}"],
    })
    note = (f"**{ds}**, seed 1989: {len(demo(ds)['calib']['gts'])} calibration / {n} test images. "
            f"Single-seed coverage is one random draw. The 36-seed averages are in tab 1. "
            f"Stretch change on this split: **{100 * (a['stretch'].mean() / p['stretch'].mean() - 1):+.1f}%**.")
    return fig, summary, note, gr.update(maximum=n - 1)


def tuned_settings(ds, which):
    _, _, hp = tables()
    h = hp[(hp.dataset == ds) & (hp.model == which)]
    best = h.groupby(["kind", "beta", "gamma"])["count"].sum().idxmax()
    kind, beta, gamma = best
    beta = min(BETAS, key=lambda b: abs(b - float(beta)))
    # plain Python types: numpy floats reach the browser as strings and the
    # gamma slider then fails Gradio's bounds check ('<' between str and int)
    return str(kind), beta, float(gamma)


# =========================================================================== #
#  UI
# =========================================================================== #
METHOD_MD = """
### Paper (Mossina & Friedrich, MICCAI 2025)
Prediction set = predicted mask dilated λ̂ times by a 3×3 cross. λ̂ is the conformal quantile
of the per-image scores *"smallest λ covering ≥ τ of the GT pixels"*. Guarantee:
**P(coverage ≥ τ) ≥ 1−α**, using only the predicted mask (black-box).

**Key identity used here:** λ dilations by the cross = {pixels whose taxicab distance to Ŷ is ≤ λ}.
So the prediction set is a sub-level set of a distance map, which we can generalise.

### Extension: AG-MPS (Adaptive Geodesic Morphological Prediction Sets)
* **E1, geodesic margin:** distance with pixel costs `c = 1 + β·h`. h = colour difference from
  the object (`region`), image gradient (`edge`), or `1−2·sigmoid` (`sigmoid`, gray-box).
  The margin grows easily inside object-like regions and stops at boundaries. β = 0 gives the paper's method.
* **E2, size-adaptive:** score ÷ σ(Ŷ) with σ = (1 + equivalent radius)^γ; at test time
  λ = q̂·σ(Ŷ). γ = 0 gives the paper's method.
* **E3:** exact conformal quantile index (the official code is off by one, so slightly conservative).

The sets stay nested and D and σ depend only on (X, Ŷ), so **Theorem 1 still holds**.
β, γ and h are chosen on a separate tuning set, never on calibration data.
"""


def build():
    with gr.Blocks(title="ConSeMa + AG-MPS results", analytics_enabled=False) as ui:
        gr.Markdown("# Conformal morphological prediction sets: paper vs AG-MPS extension")
        with gr.Tab("36-seed results"):
            with gr.Row():
                ds1 = gr.Dropdown(DATASETS, value="polyps", label="dataset")
                st1 = gr.Dropdown(SETTINGS, value="1-α=0.95, τ=0.99", label="setting")
            gr.Markdown("**Extension results.** Mean over 36 seeds; hyperparameters chosen on the tuning set.")
            t_main = gr.Dataframe(wrap=True)
            gr.Markdown("**Reproduction of the paper's Table 1** (paper protocol, official code index)")
            t_rep = gr.Dataframe(wrap=True)
            gal = gr.Gallery(label="figures", columns=2, height="auto")
            for c in (ds1, st1):
                c.change(results_view, [ds1, st1], [t_main, t_rep, gal])
            ui.load(results_view, [ds1, st1], [t_main, t_rep, gal])

        with gr.Tab("Interactive explorer"):
            with gr.Row():
                ds2 = gr.Dropdown(DATASETS, value="wbc", label="dataset")
                st2 = gr.Dropdown(SETTINGS, value="1-α=0.95, τ=0.99", label="setting")
                kind = gr.Dropdown(KINDS, value="region", label="resistance h (E1)")
                beta = gr.Dropdown(BETAS, value=64, label="β (resistance strength)")
                gamma = SafeSlider(0, 2, value=1.0, step=0.25, label="γ (size adaptivity, E2)")
            with gr.Row():
                bb = gr.Button("Load tuned black-box settings")
                gb = gr.Button("Load tuned gray-box settings")
                run = gr.Button("Calibrate & show", variant="primary")
            idx = SafeSlider(0, 39, value=0, step=1, label="test image")
            plot = gr.Plot()
            note = gr.Markdown()
            table = gr.Dataframe()
            ins = [ds2, st2, kind, beta, gamma, idx]
            outs = [plot, table, note, idx]
            run.click(explore, ins, outs)
            idx.release(explore, ins, outs)
            bb.click(lambda d: tuned_settings(d, "black-box"), ds2, [kind, beta, gamma]).then(
                explore, ins, outs)
            gb.click(lambda d: tuned_settings(d, "gray-box"), ds2, [kind, beta, gamma]).then(
                explore, ins, outs)

        with gr.Tab("Method"):
            gr.Markdown(METHOD_MD)
    return ui


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--share", action="store_true", help="public link (Colab)")
    ap.add_argument("--port", type=int, default=7860)
    args = ap.parse_args()
    build().queue().launch(share=args.share, server_port=args.port,
                           allowed_paths=[str(FIGS)])