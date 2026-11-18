"""Equivalence and validity tests for the AG-MPS extension.

Run:  .venv/bin/python -m pytest tests -q
"""

import numpy as np
import pytest
from scipy import ndimage as ndi

from consema.morphology import operator_dilation_sequential, dilation_score_fixed_disk
from consema.extension import (
    l1_distance,
    geodesic_distance,
    distance_map,
    resistance_map,
    nonconformity_score,
    conformal_quantile,
    build_record,
    scores_of,
    evaluate,
)

CROSS = dict(strict_radius=True)  # the paper's 3x3 cross


def random_blob(rng, shape=(64, 64), n_seeds=3, iters=6):
    m = np.zeros(shape, bool)
    idx = rng.integers(8, shape[0] - 8, size=(n_seeds, 2))
    m[idx[:, 0], idx[:, 1]] = True
    m = ndi.binary_dilation(m, iterations=int(rng.integers(2, iters + 1)))
    return m


@pytest.mark.parametrize("seed", range(10))
def test_l1_sublevel_sets_equal_paper_dilations(seed):
    rng = np.random.default_rng(seed)
    pred = random_blob(rng)
    d = l1_distance(pred)
    for lam in range(0, 12):
        paper = operator_dilation_sequential(pred, lam, CROSS).astype(bool)
        assert np.array_equal(paper, d <= lam), lam


@pytest.mark.parametrize("seed", range(10))
@pytest.mark.parametrize("tau", [0.9, 0.99, 0.999, 1.0])
def test_score_equals_paper_score(seed, tau):
    rng = np.random.default_rng(seed)
    pred = random_blob(rng).astype(np.uint8)
    gt = random_blob(rng).astype(np.uint8)
    paper = dilation_score_fixed_disk(gt, pred, CROSS, tau)
    ours = nonconformity_score(l1_distance(pred), gt, tau)
    assert paper == ours
    assert build_record(l1_distance(pred), gt, pred).score(tau) == ours


@pytest.mark.parametrize("seed", range(5))
def test_geodesic_with_unit_cost_is_l1(seed):
    rng = np.random.default_rng(seed)
    pred = random_blob(rng)
    g = geodesic_distance(pred, np.ones(pred.shape))
    assert np.allclose(g, l1_distance(pred))


@pytest.mark.parametrize("seed", range(5))
def test_geodesic_dominates_l1_and_beta0_is_paper(seed):
    rng = np.random.default_rng(seed)
    pred = random_blob(rng)
    img = rng.random(pred.shape)
    d0 = distance_map(pred, "edge", beta=0.0, image=img)
    d = distance_map(pred, "edge", beta=4.0, image=img)
    assert np.array_equal(d0, l1_distance(pred))
    assert np.all(d >= l1_distance(pred) - 1e-9)
    assert np.all(d[pred] == 0)


def test_resistance_ranges():
    rng = np.random.default_rng(0)
    pred = random_blob(rng)
    img = rng.random(pred.shape + (3,))
    for kind in ["region", "edge"]:
        h = resistance_map(kind, pred, image=img)
        assert h.min() >= 0 and h.max() <= 1
    h = resistance_map("sigmoid", pred, soft_pred=rng.random(pred.shape))
    assert h.min() >= 0 and h.max() <= 1


def test_quantile_index_matches_official_code():
    # official: sorted(scores)[ceil((1-a)(n+1))]  (0-based)  -> paper_index=True
    scores = np.arange(50)
    for a in [0.1, 0.05]:
        k = int(np.ceil((1 - a) * (len(scores) + 1)))
        assert conformal_quantile(scores, a, paper_index=True) == sorted(scores)[k]
        assert conformal_quantile(scores, a, paper_index=False) == sorted(scores)[k - 1]


@pytest.mark.parametrize("gamma", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("kind,beta", [("uniform", 0.0), ("edge", 4.0)])
def test_marginal_coverage_simulation(gamma, kind, beta):
    """Exchangeable synthetic data: average coverage must be >= 1 - alpha."""
    rng = np.random.default_rng(123)
    alpha, tau = 0.1, 0.95
    records = []
    for _ in range(200):
        gt = random_blob(rng, shape=(48, 48), n_seeds=2, iters=7)
        pred = ndi.binary_erosion(gt, iterations=int(rng.integers(0, 3))) | random_blob(
            rng, shape=(48, 48), n_seeds=1, iters=2
        )
        if not pred.any():
            pred = gt.copy()
        img = gt.astype(float) + 0.3 * rng.standard_normal(gt.shape)
        d = distance_map(pred, kind, beta=beta, image=img)
        records.append(build_record(d, gt, pred))
    covs = []
    for _ in range(200):
        perm = rng.permutation(len(records))
        cal = [records[i] for i in perm[:100]]
        test = [records[i] for i in perm[100:]]
        q = conformal_quantile(scores_of(cal, tau, gamma), alpha)
        covs.append(evaluate(test, q, tau, gamma)["coverage"])
    assert np.mean(covs) >= 1 - alpha - 0.01
