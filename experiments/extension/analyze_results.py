"""
Turn raw_{dataset}.csv files into the tables and figures for the presentation.

Model selection for the extension uses ONLY tuning-set columns (tune_stretch);
calibration/test columns are then read for the selected configuration.

Usage: .venv/bin/python experiments/extension/analyze_results.py
"""

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "extension"
FIGS = ROOT / "figures" / "extension"
KEYS = ["dataset", "seed", "alpha", "tau"]

# Table 1 of the paper (mean over 36 runs): (dataset, 1-alpha, tau) -> (cov, stretch, lambda)
PAPER_T1 = {
    ("polyps", 0.90, 0.9): (0.909, 1.253, 6.083), ("polyps", 0.90, 0.99): (0.898, 1.780, 17.500),
    ("polyps", 0.90, 0.999): (0.904, 2.031, 22.500), ("polyps", 0.95, 0.9): (0.953, 3.093, 41.389),
    ("polyps", 0.95, 0.99): (0.955, 4.144, 58.611), ("polyps", 0.95, 0.999): (0.962, 4.840, 69.167),
    ("wbc", 0.90, 0.9): (0.952, 1.108, 1.056), ("wbc", 0.90, 0.99): (0.932, 1.646, 6.278),
    ("wbc", 0.90, 0.999): (0.928, 1.865, 8.389), ("wbc", 0.95, 0.9): (0.984, 1.449, 4.361),
    ("wbc", 0.95, 0.99): (0.985, 2.448, 13.667), ("wbc", 0.95, 0.999): (0.985, 2.776, 16.528),
    ("oasis", 0.90, 0.9): (0.969, 1.774, 4.500), ("oasis", 0.90, 0.99): (0.941, 2.198, 12.333),
    ("oasis", 0.90, 0.999): (0.940, 2.247, 15.417), ("oasis", 0.95, 0.9): (0.997, 1.845, 5.194),
    ("oasis", 0.95, 0.99): (0.990, 2.232, 14.222), ("oasis", 0.95, 0.999): (0.993, 2.259, 17.917),
}

METHODS = {
    # name: (filter on candidate rows) -- selection by tune_stretch within the filter
    "Paper (baseline)": lambda d: (d.kind == "uniform") & (d.gamma == 0),
    "E2: size-adaptive": lambda d: d.kind == "uniform",
    "E1: geodesic (black-box)": lambda d: d.kind.isin(["uniform", "region", "edge"]) & (d.gamma == 0),
    "AG-MPS (black-box, E1+E2)": lambda d: d.kind.isin(["uniform", "region", "edge"]),
    "AG-MPS (gray-box, +sigmoid)": lambda d: d.kind.isin(["uniform", "region", "edge", "sigmoid"]),
}


def load():
    dfs = [pd.read_csv(p) for p in sorted(RESULTS.glob("raw_*.csv"))]
    return pd.concat(dfs, ignore_index=True)


def fmt(m, s):
    return f"{m:.3f} ({s:.3f})"


def reproduction_table(df):
    d = df[df.protocol == "paper"]
    g = d.groupby(["dataset", "alpha", "tau"])
    rows = []
    for (ds, a, t), x in g:
        p = PAPER_T1.get((ds, round(1 - a, 2), t), (np.nan,) * 3)
        rows.append({
            "dataset": ds, "1-alpha": round(1 - a, 2), "tau": t,
            "Cov (ours)": fmt(x.coverage.mean(), x.coverage.std()), "Cov (paper)": p[0],
            "stretch (ours)": fmt(x.stretch.mean(), x.stretch.std()), "stretch (paper)": p[1],
            "lambda (ours)": fmt(x.q_hat.mean(), x.q_hat.std()), "lambda (paper)": p[2],
        })
    return pd.DataFrame(rows)


def select(df, cond):
    d = df[(df.protocol == "extension")]
    d = d[cond(d)]
    idx = d.groupby(KEYS)["tune_stretch"].idxmin()
    return d.loc[idx]


def main_table(df):
    rows = []
    base = select(df, METHODS["Paper (baseline)"]).set_index(KEYS)
    for name, cond in METHODS.items():
        sel = select(df, cond)
        rel = (sel.set_index(KEYS).stretch / base.stretch).groupby(["dataset", "alpha", "tau"]).mean()
        for (ds, a, t), x in sel.groupby(["dataset", "alpha", "tau"]):
            rows.append({
                "dataset": ds, "1-alpha": round(1 - a, 2), "tau": t, "method": name,
                "coverage": x.coverage.mean(), "coverage_sd": x.coverage.std(),
                "stretch": x.stretch.mean(), "stretch_sd": x.stretch.std(),
                "stretch_vs_paper_%": 100 * (rel.loc[(ds, a, t)] - 1),
                "cov_small": x.cov_small.mean(), "cov_medium": x.cov_medium.mean(),
                "cov_large": x.cov_large.mean(),
                "worst_group_cov": x[["cov_small", "cov_medium", "cov_large"]].mean().min(),
                "stretch_small": x.stretch_small.mean(), "stretch_large": x.stretch_large.mean(),
            })
    return pd.DataFrame(rows)


def selected_hparams(df):
    sel = select(df, METHODS["AG-MPS (gray-box, +sigmoid)"])
    selb = select(df, METHODS["AG-MPS (black-box, E1+E2)"])
    out = []
    for name, s in [("black-box", selb), ("gray-box", sel)]:
        c = s.groupby(["dataset", "kind", "beta", "gamma"]).size().rename("count").reset_index()
        c["model"] = name
        out.append(c)
    return pd.concat(out)


# --------------------------------------------------------------------------- #
#  Figures
# --------------------------------------------------------------------------- #
def fig_ablation(df, alpha=0.1, tau=0.99):
    d = df[(df.protocol == "extension") & (df.alpha == alpha) & (df.tau == tau)]
    datasets = sorted(d.dataset.unique())
    fig, axes = plt.subplots(2, len(datasets), figsize=(4.2 * len(datasets), 6.5), squeeze=False)
    for j, ds in enumerate(datasets):
        x = d[d.dataset == ds]
        base = x[(x.kind == "uniform") & (x.gamma == 0)].stretch.mean()
        ax = axes[0, j]
        for kind, c in [("region", "C0"), ("edge", "C1"), ("sigmoid", "C2")]:
            y = x[(x.kind == kind) & (x.gamma == 0)].groupby("beta").stretch.mean()
            ax.plot(y.index, y.values, "o-", color=c, label=kind)
        ax.axhline(base, color="k", ls="--", label="paper (uniform)")
        ax.set_xscale("log", base=2)
        ax.set_title(f"{ds}: E1 geodesic (γ=0)")
        ax.set_xlabel("β (resistance strength)")
        ax.set_ylabel("test stretch ↓")
        ax.legend(fontsize=8)
        ax = axes[1, j]
        y = x[x.kind == "uniform"].groupby("gamma")
        ax.plot(y.stretch.mean().index, y.stretch.mean().values, "o-", color="C3", label="stretch")
        ax.set_xlabel("γ (size adaptivity)")
        ax.set_ylabel("test stretch ↓", color="C3")
        ax.axhline(base, color="k", ls="--")
        ax2 = ax.twinx()
        ax2.plot(y.coverage.mean().index, y.coverage.mean().values, "s:", color="C4")
        ax2.axhline(1 - alpha, color="C4", lw=0.8)
        ax2.set_ylim(1 - alpha - 0.05, min(1.0, 1 - alpha + 0.05))
        ax2.set_ylabel("coverage", color="C4")
        ax.set_title(f"{ds}: E2 size-adaptive (uniform)")
    fig.suptitle(f"Ablation, 1-α={1-alpha:.2f}, τ={tau}, mean over 36 seeds")
    fig.tight_layout()
    fig.savefig(FIGS / f"ablation_a{alpha}_t{tau}.png", dpi=150)
    plt.close(fig)


def fig_conditional(df, alpha=0.1, tau=0.99):
    names = ["Paper (baseline)", "AG-MPS (black-box, E1+E2)", "AG-MPS (gray-box, +sigmoid)"]
    datasets = sorted(df.dataset.unique())
    fig, axes = plt.subplots(1, len(datasets), figsize=(4.5 * len(datasets), 3.6), squeeze=False)
    for j, ds in enumerate(datasets):
        ax = axes[0, j]
        for k, name in enumerate(names):
            s = select(df[df.dataset == ds], METHODS[name])
            s = s[(s.alpha == alpha) & (s.tau == tau)]
            vals = [s[f"cov_{g}"].mean() for g in ["small", "medium", "large"]]
            ax.bar(np.arange(3) + (k - 1) * 0.27, vals, width=0.27, label=name)
        ax.axhline(1 - alpha, color="k", ls="--", lw=1)
        ax.set_xticks(range(3), ["small", "medium", "large"])
        ax.set_ylim(0.5, 1.02)
        ax.set_title(f"{ds}: coverage by predicted size")
    axes[0, 0].legend(fontsize=7, loc="lower left")
    fig.tight_layout()
    fig.savefig(FIGS / f"conditional_cov_a{alpha}_t{tau}.png", dpi=150)
    plt.close(fig)


def fig_main(mt):
    for ds in sorted(mt.dataset.unique()):
        x = mt[mt.dataset == ds]
        settings = x[["1-alpha", "tau"]].drop_duplicates().values
        fig, ax = plt.subplots(figsize=(8, 3.4))
        w = 0.8 / len(METHODS)
        for k, name in enumerate(METHODS):
            y = x[x.method == name]
            ax.bar(np.arange(len(settings)) + k * w, y.stretch, w, yerr=y.stretch_sd,
                   label=name, capsize=2)
        ax.set_xticks(np.arange(len(settings)) + 0.4 - w / 2,
                      [f"1-α={a}\nτ={t}" for a, t in settings], fontsize=8)
        ax.set_ylabel("mean stretch ↓")
        ax.set_title(f"{ds}: prediction-set size (all methods reach ≥ 1-α coverage)")
        ax.legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(FIGS / f"main_stretch_{ds}.png", dpi=150)
        plt.close(fig)


def main():
    FIGS.mkdir(parents=True, exist_ok=True)
    df = load()
    rep = reproduction_table(df)
    rep.to_csv(RESULTS / "table_reproduction.csv", index=False)
    mt = main_table(df)
    mt.to_csv(RESULTS / "table_main.csv", index=False)
    hp = selected_hparams(df)
    hp.to_csv(RESULTS / "selected_hparams.csv", index=False)

    with open(RESULTS / "summary.md", "w") as f:
        f.write("# Reproduction of Table 1 (paper protocol, official quantile index)\n\n")
        f.write(rep.to_markdown(index=False))
        f.write("\n\n# Extension results (tune/calib/test protocol, 36 seeds)\n\n")
        cols = ["dataset", "1-alpha", "tau", "method", "coverage", "stretch",
                "stretch_vs_paper_%", "worst_group_cov", "stretch_small", "stretch_large"]
        f.write(mt[cols].round(3).to_markdown(index=False))
        f.write("\n\n# Selected hyper-parameters (counts over seeds x settings)\n\n")
        f.write(hp.to_markdown(index=False))
    for a, t in [(0.1, 0.9), (0.1, 0.99), (0.05, 0.99)]:
        fig_ablation(df, a, t)
        fig_conditional(df, a, t)
    fig_main(mt)
    print((RESULTS / "summary.md").read_text())


if __name__ == "__main__":
    main()
