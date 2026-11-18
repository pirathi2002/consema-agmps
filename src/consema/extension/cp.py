"""
Split conformal prediction on top of distance maps.

For an image with distance map D (see distances.py), ground truth Y and
coverage ratio tau, the paper's nonconformity score (Eq. 3) is

    r = inf{ lam : |Y ∩ {D <= lam}| / |Y| >= tau }
      = k-th smallest value of D over the GT pixels,  k = ceil(tau * |Y|).

Extension E2 normalises it by a size scale sigma(Y_hat):

    s = r / sigma(Y_hat),   sigma = (1 + r_eq)^gamma,  r_eq = sqrt(|Y_hat|/pi)

and uses lambda_test = q_hat * sigma(Y_hat_test). Since {D <= t*sigma}_t is
nested in t and sigma depends only on Y_hat, the CP guarantee is unchanged.
"""

from dataclasses import dataclass

import numpy as np


# --------------------------------------------------------------------------- #
#  Scores
# --------------------------------------------------------------------------- #
def nonconformity_score(dist: np.ndarray, gt_mask: np.ndarray, tau: float) -> float:
    """Paper Eq. (3) generalised to any distance map (exact, no loop)."""
    gt = np.asarray(gt_mask).astype(bool)
    n_gt = int(gt.sum())
    if n_gt == 0:
        return 0.0  # nothing to cover
    d = np.sort(dist[gt])
    k = int(np.ceil(tau * n_gt - 1e-9))
    k = min(max(k, 1), n_gt)
    return float(d[k - 1])


def size_scale(n_pred_pixels, gamma: float) -> np.ndarray:
    """sigma(Y_hat) = (1 + equivalent radius)^gamma. gamma=0 -> 1 (paper)."""
    r_eq = np.sqrt(np.asarray(n_pred_pixels, dtype=np.float64) / np.pi)
    return (1.0 + r_eq) ** gamma


def conformal_quantile(scores, alpha: float, paper_index: bool = False) -> float:
    """Split-CP quantile: the ceil((n+1)(1-alpha))-th smallest score (Eq. 1).

    paper_index=True reproduces the official code, which uses that rank as a
    0-based index, i.e. takes the *next* order statistic (one step more
    conservative than necessary).
    """
    s = np.sort(np.asarray(scores, dtype=np.float64))
    n = len(s)
    k = int(np.ceil((n + 1) * (1 - alpha)))  # 1-based rank
    idx = k if paper_index else k - 1
    if idx >= n:
        return np.inf
    return float(s[idx])


# --------------------------------------------------------------------------- #
#  Compact per-image record: enough to evaluate ANY lambda exactly
# --------------------------------------------------------------------------- #
@dataclass
class ImageRecord:
    gt_d_sorted: np.ndarray  # sorted D over GT pixels       -> coverage(lambda)
    out_d_sorted: np.ndarray  # sorted D over pixels outside Y_hat -> |C(lambda)|
    n_pred: int  # |Y_hat|
    n_gt: int  # |Y|

    def score(self, tau: float) -> float:
        if self.n_gt == 0:
            return 0.0
        k = int(np.ceil(tau * self.n_gt - 1e-9))
        k = min(max(k, 1), self.n_gt)
        return float(self.gt_d_sorted[k - 1])

    def covered_fraction(self, lam: float) -> float:
        if self.n_gt == 0:
            return 1.0
        return np.searchsorted(self.gt_d_sorted, lam, side="right") / self.n_gt

    def set_size(self, lam: float) -> int:
        return self.n_pred + int(np.searchsorted(self.out_d_sorted, lam, side="right"))


def build_record(dist: np.ndarray, gt_mask: np.ndarray, pred_mask: np.ndarray) -> ImageRecord:
    gt = np.asarray(gt_mask).astype(bool)
    pred = np.asarray(pred_mask).astype(bool)
    return ImageRecord(
        gt_d_sorted=np.sort(dist[gt]).astype(np.float32),
        out_d_sorted=np.sort(dist[~pred]).astype(np.float32),
        n_pred=int(pred.sum()),
        n_gt=int(gt.sum()),
    )


# --------------------------------------------------------------------------- #
#  Vectorised evaluation of a list of records
# --------------------------------------------------------------------------- #
def scores_of(records, tau: float, gamma: float = 0.0) -> np.ndarray:
    raw = np.array([r.score(tau) for r in records])
    sig = size_scale([r.n_pred for r in records], gamma)
    return raw / sig


def evaluate(records, q_hat: float, tau: float, gamma: float = 0.0) -> dict:
    """Apply lambda_i = q_hat * sigma_i on each record and compute metrics."""
    sig = size_scale([r.n_pred for r in records], gamma)
    lams = q_hat * sig
    covfrac = np.array([r.covered_fraction(l) for r, l in zip(records, lams)])
    sizes = np.array([r.set_size(l) for r, l in zip(records, lams)], dtype=np.float64)
    n_pred = np.array([r.n_pred for r in records], dtype=np.float64)
    stretch = sizes / np.maximum(n_pred, 1)
    covered = covfrac >= tau - 1e-12
    return dict(
        covered=covered,
        coverage=float(covered.mean()),
        stretch=stretch,
        mean_stretch=float(stretch.mean()),
        median_stretch=float(np.median(stretch)),
        added_pixels=float((sizes - n_pred).mean()),
        mean_lambda=float(np.mean(lams)),
    )
