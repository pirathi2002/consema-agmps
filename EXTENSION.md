# Extension: Adaptive Geodesic Morphological Prediction Sets (AG-MPS)

Extension of *Mossina & Friedrich, "Conformal Prediction for Image Segmentation
Using Morphological Prediction Sets", MICCAI 2025* (this repository).

## 1. Motivation (from the paper's own limitations / perspectives)

| Limitation of the paper | What the extension does |
|---|---|
| The margin grows **isotropically**: λ dilations by a fixed 3×3 cross add the same thickness everywhere, including into obvious background. | **E1 – geodesic margins.** The margin grows along a *geodesic* (cost-weighted) distance. Pixels that look like the object are cheap to add, edges/background are expensive. |
| One λ̂ for **all images** ("CP sets do not adapt to the input instance", Sec. 5). A small object and a large object receive the same absolute margin → huge relative stretch on small objects, and unequal coverage across object sizes. | **E2 – size-adaptive scores.** The score is normalised by the size of the predicted object, so the margin is proportional to the object. |
| Paper suggests "combining morphological sets with other approaches (e.g. thresholding)". | **E1 gray-box variant**: the geodesic cost can come from the sigmoid, giving a contiguous margin (no scattered artefacts, unlike thresholding) that still follows the model's uncertainty. |
| Implementation detail: the official quantile index is off by one (more conservative than Eq. 1). | **E3**: exact split-CP quantile (Eq. 1), reported alongside the official one. |

Both E1 and E2 contain the paper as a special case (β = 0, γ = 0).

## 2. Method

**Key observation (exact).** λ dilations of Ŷ by the 3×3 cross equals the set of
pixels whose 4-connected (taxicab) distance to Ŷ is ≤ λ:

    δ_B^λ(Ŷ) = { p : D_L1(p; Ŷ) ≤ λ }

So the paper's sets are sub-level sets of a distance map, and the score (Eq. 3)
is the ⌈τ|Y|⌉-th smallest value of D over the ground-truth pixels — computed in
one distance transform instead of a loop of λ dilations.
(Verified: `tests/test_extension.py`, and 0/80 mismatches against
`dilation_score_fixed_disk` on real PraNet masks.)

**E1 – geodesic distance.** Replace D_L1 by a geodesic distance with pixel costs

    c(p) = 1 + β · h(p),   h(p) ∈ [0, 1],
    D_β(p) = min over 4-connected paths from Ŷ to p of Σ cost,

computed with Dijkstra / minimum-cost-path (`skimage.graph.MCP_Geometric`).
Resistance maps h (fixed *before* calibration):

* `region` (black-box: uses X and Ŷ only) – colour distance of p to the mean
  colour inside Ŷ, normalised by object/background contrast;
* `edge` (black-box) – normalised image gradient magnitude;
* `sigmoid` (gray-box) – h = clip(1 − 2s, 0, 1) with s the sigmoid score.

**E2 – size-adaptive (normalised) scores.**

    σ(Ŷ) = (1 + r_eq)^γ,   r_eq = sqrt(|Ŷ| / π)   (equivalent radius)
    s_i  = r_i / σ(Ŷ_i),   q̂ = ⌈(n+1)(1−α)⌉-th smallest s_i
    C(X_test) = { p : D_β(p) ≤ q̂ · σ(Ŷ_test) }

**Validity.** For each image, {p : D_β(p) ≤ t·σ(Ŷ)} is nested in t, and D_β, σ
depend only on (X, Ŷ) with β, γ, h fixed before calibration. So the setting of
Theorem 1 is unchanged (nested sets + monotone binary loss), and

    P( |Y_test ∩ C(X_test)| / |Y_test| ≥ τ ) ≥ 1 − α.

**Hyper-parameter selection without breaking exchangeability.** β, γ and the
resistance type are chosen on a **separate tuning set** (never on calibration
data, as the paper requires in Sec. 3.1):

* WBC / OASIS: tuning = support-split images not used as UniverSeg context
  (calibration and test splits are *exactly* the paper's);
* Polyps: per seed, tune 100 / calibration 200 / test 200
  (the baseline is re-run on the same calibration/test split).

Selection criterion: smallest mean stretch on the tuning set.

## 3. Code map (for the code review)

| Paper | Code |
|---|---|
| Eq. (2) nested sets δ_B^λ(Ŷ) | `src/consema/morphology.py::operator_dilation_sequential` (official) — equivalent: `src/consema/extension/distances.py::l1_distance` |
| Eq. (3) nonconformity score | official: `morphology.py::dilation_score_fixed_disk` (loop) — ours: `extension/cp.py::nonconformity_score`, `ImageRecord.score` |
| Eq. (1) conformal quantile | official: `conformal.py::Conformalizer.get_conformal_quantile` — ours: `extension/cp.py::conformal_quantile` (`paper_index=True` reproduces the official off-by-one) |
| Eq. (5) coverage, Eq. (6) stretch | `extension/cp.py::evaluate` |
| E1 resistance maps | `extension/distances.py::resistance_map` |
| E1 geodesic distance | `extension/distances.py::geodesic_distance` |
| E2 size scale σ(Ŷ) | `extension/cp.py::size_scale`, `scores_of`, `evaluate` |
| Experiments, 36 seeds | `experiments/extension/run_extension.py` |
| UniverSeg predictions (paper protocol) | `experiments/extension/cache_predictions.py` |
| Tables / figures | `experiments/extension/analyze_results.py`, `qualitative.py` |
| Tests | `tests/test_extension.py` |
| Result viewer (Gradio) | `app/app.py`, demo data from `experiments/extension/make_demo_bundle.py` |
| Colab notebook | `notebooks/consema_extension_colab.ipynb`, zip via `scripts/make_colab_bundle.sh` |
| Memory fix of the official polyps loader | `src/benchmarkerie/datasets.py::npz_memmap`, `load_polyps_data` |

## 4. Reproducing

### 4.1 Result viewer (fastest way to check the results)

```bash
scripts/safe_run.sh -m 4G .venv/bin/python app/app.py      # open http://127.0.0.1:7860
```

* **36-seed results**: the extension table, the reproduction of Table 1, and all figures, per dataset and (α, τ).
* **Interactive explorer**: calibrates the paper's method and AG-MPS live on one seed (`demo/*.npz`),
  then shows any test image side by side with coverage and stretch. The "Load tuned settings" buttons
  use the hyperparameters selected on the tuning set.
* **Method**: a one-page summary to use while presenting.

`demo/*.npz` is built by `experiments/extension/make_demo_bundle.py` (needs the datasets).

### 4.2 Google Colab (if the laptop is too slow or short of memory)

`notebooks/consema_extension_colab.ipynb`. Build the upload with
`scripts/make_colab_bundle.sh --demo` (→ `../consema_project.zip`). In Colab:
Runtime → T4 GPU, then section 1 + section 7 to view results, or every section to re-run everything.

### 4.3 Full pipeline on the laptop

**Memory safety:** the laptop has 13 GB of RAM. The official polyps loader used to need more than 6 GB
just at import, which froze the laptop. It now memory-maps the arrays and loads only the
500 rows it uses, with identical results. Still, run every heavy script through the
memory cap, which kills the script instead of freezing the machine:

```bash
scripts/safe_run.sh -m 8G <command>      # systemd memory cap, no swap, PYTHONPATH (ROS) cleared
```

```bash
# environment (CPU is enough except UniverSeg inference, where a GPU helps)
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python torch --index-url https://download.pytorch.org/whl/cpu
uv pip install --python .venv/bin/python -e ".[dev]" -e benchmarks/universeg einops gdown pandas joblib nibabel tabulate gradio
# GPU venv for UniverSeg inference: .venv_gpu (torch cu124)

# data: see Makefile (polyps tarball is gzip despite .xz name);
# OASIS moved to https://huggingface.co/datasets/DalcaLab/neurite-oasis (2D, 24 MB)

R="scripts/safe_run.sh -m 8G"
$R .venv/bin/python -m pytest tests -q                                          # equivalence + validity
$R .venv_gpu/bin/python experiments/extension/cache_predictions.py --dataset wbc   # GPU, 36 seeds
$R .venv_gpu/bin/python experiments/extension/cache_predictions.py --dataset oasis
$R .venv/bin/python experiments/extension/run_extension.py --dataset polyps --n_jobs 8
$R .venv/bin/python experiments/extension/run_extension.py --dataset wbc --n_jobs 8
$R .venv/bin/python experiments/extension/run_extension.py --dataset oasis --n_jobs 8
$R .venv/bin/python experiments/extension/analyze_results.py                    # tables + figures
$R .venv/bin/python experiments/extension/make_demo_bundle.py                   # demo data for the viewer

# official paper script (unchanged method; writes results/results_polyps_fixed_disk_*.csv)
$R .venv/bin/python experiments/experiments.py --dataset polyps
```

## 5. Results (36 random seeds, same seeds as the paper)

### 5.1 Reproduction of the paper (Table 1)

Using the paper's protocol and the official quantile index:

* **WBC**: identical to Table 1 (all coverage / stretch / λ̂ values match to 3 decimals).
* **OASIS**: within 0.005 of Table 1 everywhere.
* **Polyps**: within one standard deviation of Table 1 (e.g. 1−α=0.95, τ=0.99: coverage
  0.952 vs 0.955, stretch 3.96 vs 4.14). The split shuffling differs slightly from
  the official script, which shuffles a global list in place across seeds.

Full table: `results/extension/table_reproduction.csv`.

### 5.2 Extension

Protocol: extension hyper-parameters (resistance type, β, γ) chosen per seed
on the **tuning set only**. The baseline uses the same calibration/test data and the
exact quantile (E3). Stretch = |C|/|Ŷ| (lower is better). All methods are calibrated
to the same 1−α.

### polyps

Mean stretch (change vs paper):

| method                      | 1-α=0.9, τ=0.9   | 1-α=0.9, τ=0.99   | 1-α=0.95, τ=0.9   | 1-α=0.95, τ=0.99   |
|:----------------------------|:-----------------|:------------------|:------------------|:-------------------|
| Paper (baseline)            | 1.226 (0.0%)     | 1.771 (0.0%)      | 2.755 (0.0%)      | 3.602 (0.0%)       |
| E2: size-adaptive           | 1.195 (-2.0%)    | 1.661 (-5.1%)     | 2.074 (-20.9%)    | 2.562 (-25.7%)     |
| E1: geodesic (black-box)    | 1.222 (-0.4%)    | 1.78 (0.9%)       | 2.868 (5.3%)      | 3.765 (5.5%)       |
| AG-MPS (black-box, E1+E2)   | 1.186 (-2.7%)    | 1.658 (-5.2%)     | 2.004 (-24.5%)    | 2.751 (-20.8%)     |
| AG-MPS (gray-box, +sigmoid) | 1.176 (-3.5%)    | 1.526 (-12.4%)    | 1.788 (-32.4%)    | 2.132 (-38.0%)     |

Coverage:

| method                      |   1-α=0.9, τ=0.9 |   1-α=0.9, τ=0.99 |   1-α=0.95, τ=0.9 |   1-α=0.95, τ=0.99 |
|:----------------------------|-----------------:|------------------:|------------------:|-------------------:|
| Paper (baseline)            |            0.894 |             0.893 |             0.947 |              0.945 |
| E2: size-adaptive           |            0.894 |             0.894 |             0.946 |              0.945 |
| E1: geodesic (black-box)    |            0.894 |             0.89  |             0.945 |              0.946 |
| AG-MPS (black-box, E1+E2)   |            0.895 |             0.893 |             0.945 |              0.945 |
| AG-MPS (gray-box, +sigmoid) |            0.895 |             0.891 |             0.946 |              0.946 |

### wbc

Mean stretch (change vs paper):

| method                      | 1-α=0.9, τ=0.9   | 1-α=0.9, τ=0.99   | 1-α=0.95, τ=0.9   | 1-α=0.95, τ=0.99   |
|:----------------------------|:-----------------|:------------------|:------------------|:-------------------|
| Paper (baseline)            | 1.088 (0.0%)     | 1.545 (0.0%)      | 1.22 (0.0%)       | 1.906 (0.0%)       |
| E2: size-adaptive           | 1.053 (-3.1%)    | 1.434 (-6.9%)     | 1.157 (-4.9%)     | 1.798 (-5.3%)      |
| E1: geodesic (black-box)    | 1.039 (-4.4%)    | 1.213 (-20.4%)    | 1.083 (-10.4%)    | 1.348 (-27.8%)     |
| AG-MPS (black-box, E1+E2)   | 1.04 (-4.3%)     | 1.206 (-20.8%)    | 1.084 (-10.3%)    | 1.311 (-29.5%)     |
| AG-MPS (gray-box, +sigmoid) | 1.04 (-4.3%)     | 1.206 (-20.8%)    | 1.084 (-10.3%)    | 1.311 (-29.5%)     |

Coverage:

| method                      |   1-α=0.9, τ=0.9 |   1-α=0.9, τ=0.99 |   1-α=0.95, τ=0.9 |   1-α=0.95, τ=0.99 |
|:----------------------------|-----------------:|------------------:|------------------:|-------------------:|
| Paper (baseline)            |            0.943 |             0.921 |             0.969 |              0.962 |
| E2: size-adaptive           |            0.922 |             0.903 |             0.961 |              0.965 |
| E1: geodesic (black-box)    |            0.923 |             0.897 |             0.963 |              0.958 |
| AG-MPS (black-box, E1+E2)   |            0.919 |             0.898 |             0.965 |              0.963 |
| AG-MPS (gray-box, +sigmoid) |            0.919 |             0.898 |             0.965 |              0.963 |

### oasis

Mean stretch (change vs paper):

| method                      | 1-α=0.9, τ=0.9   | 1-α=0.9, τ=0.99   | 1-α=0.95, τ=0.9   | 1-α=0.95, τ=0.99   |
|:----------------------------|:-----------------|:------------------|:------------------|:-------------------|
| Paper (baseline)            | 1.758 (0.0%)     | 2.191 (0.0%)      | 1.814 (0.0%)      | 2.213 (0.0%)       |
| E2: size-adaptive           | 1.737 (-1.2%)    | 2.181 (-0.5%)     | 1.803 (-0.6%)     | 2.205 (-0.3%)      |
| E1: geodesic (black-box)    | 1.336 (-23.9%)   | 1.526 (-30.4%)    | 1.351 (-25.5%)    | 1.547 (-30.1%)     |
| AG-MPS (black-box, E1+E2)   | 1.336 (-23.9%)   | 1.526 (-30.4%)    | 1.35 (-25.5%)     | 1.547 (-30.1%)     |
| AG-MPS (gray-box, +sigmoid) | 1.336 (-23.9%)   | 1.526 (-30.4%)    | 1.35 (-25.5%)     | 1.547 (-30.1%)     |

Coverage:

| method                      |   1-α=0.9, τ=0.9 |   1-α=0.9, τ=0.99 |   1-α=0.95, τ=0.9 |   1-α=0.95, τ=0.99 |
|:----------------------------|-----------------:|------------------:|------------------:|-------------------:|
| Paper (baseline)            |            0.963 |             0.928 |             0.99  |              0.969 |
| E2: size-adaptive           |            0.913 |             0.906 |             0.967 |              0.956 |
| E1: geodesic (black-box)    |            0.937 |             0.899 |             0.976 |              0.954 |
| AG-MPS (black-box, E1+E2)   |            0.926 |             0.891 |             0.969 |              0.954 |
| AG-MPS (gray-box, +sigmoid) |            0.926 |             0.891 |             0.969 |              0.954 |


Figures: `figures/extension/` (main_stretch_*, ablation_*, conditional_cov_*,
qualitative_*). Selected hyper-parameters: `results/extension/selected_hparams.csv`.

### 5.3 Findings

1. **Validity is preserved.** Every variant's mean test coverage matches the
   baseline's and is within sampling error of 1−α (it is a marginal guarantee:
   n_calib = 50 for WBC/OASIS, 200 for polyps).
2. **E1 (geodesic margins) is the main gain on WBC and OASIS**: −20 to −30 %
   stretch with *black-box* information only (image + mask). Selected costs:
   `region` (colour similarity) on WBC, `edge` on OASIS. The margin stops at
   anatomical boundaries instead of flooding into neighbouring tissue
   (qualitative_wbc_blackbox.png, qualitative_oasis_blackbox.png).
3. **E2 (size adaptivity) is the main gain on polyps** (−21 to −26 % at 1−α=0.95),
   where object sizes vary widely. The paper's single λ̂ gives small polyps a
   huge relative margin (stretch ≈ 9 in qualitative_polyps_graybox.png).
   On OASIS, E2 gives no gain: the paper's OASIS label 0 is the background,
   whose size barely changes between images.
4. **Gray-box variant (+sigmoid)** gives the largest reduction on polyps (−38 %),
   addressing the paper's own proposal to combine morphology with thresholding.
   The margin stays contiguous (unlike sigmoid thresholding), but its shape
   follows the model's uncertainty.
5. **Black-box image costs do not help on polyps** (E1 alone: −0.4 to +5.5 %).
   Colonoscopy images have specular highlights and weak polyp/mucosa contrast.
   Searching over these unhelpful costs even makes the combined black-box method
   up to 7 % worse than E2 alone (2.75 vs 2.56). The selection overfits a
   100-image tuning set. An honest cost of a larger search space.
6. **Conditional coverage is rebalanced, not guaranteed.** The baseline
   under-covers *large* objects (polyps: 0.92, WBC: 0.93 at 1−α=0.95, τ=0.99).
   AG-MPS raises this to ≈0.95, at the cost of slightly lower coverage on
   small polyps (0.92–0.93). Coverage per size group is not part of the guarantee.

### 5.4 Limitations / future work

* Hyper-parameter selection needs a small extra labelled tuning set.
* For the sigmoid cost, β is selected at the largest grid value. In the limit
  the margin stays inside the sigmoid's support ("contiguous thresholding").
* Group-conditional guarantees could be obtained with Mondrian CP
  (calibrating per size group), at the cost of fewer calibration points per group.
* Multi-class extension: run one geodesic distance per class, with a
  Bonferroni-corrected α across classes.
