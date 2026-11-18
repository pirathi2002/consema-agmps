"""
Distance maps from the predicted mask.

Every prediction set in this package is a sub-level set of a distance map:

    C_lambda = { p : D(p) <= lambda }

* l1_distance        -> paper's method (lambda dilations by the 3x3 cross)
* geodesic_distance  -> extension E1: cost-weighted (geodesic) dilation
"""

from typing import Literal, Optional

import numpy as np
from scipy import ndimage as ndi
from skimage.graph import MCP_Geometric

ResistanceType = Literal["uniform", "region", "edge", "sigmoid"]


# --------------------------------------------------------------------------- #
#  Paper baseline: lambda dilations by the 3x3 cross == L1 distance <= lambda
# --------------------------------------------------------------------------- #
def l1_distance(pred_mask: np.ndarray) -> np.ndarray:
    """Taxicab distance of every pixel to the predicted mask (0 inside it).

    {p : l1_distance(Y_hat)[p] <= lam} == delta_cross^lam (Y_hat), exactly.
    This replaces the paper's loop of lambda binary dilations by a single
    distance transform (O(HW) instead of O(lambda * HW)).
    """
    pred_mask = np.asarray(pred_mask).astype(bool)
    if not pred_mask.any():
        return np.full(pred_mask.shape, np.inf, dtype=np.float64)
    return ndi.distance_transform_cdt(~pred_mask, metric="taxicab").astype(np.float64)


# --------------------------------------------------------------------------- #
#  Extension E1: resistance maps h(p) in [0, 1]
# --------------------------------------------------------------------------- #
def _to_float_image(image: np.ndarray, shape) -> np.ndarray:
    """Return image as float (H, W, C) in [0, 1], resized to `shape` if needed."""
    from skimage.transform import resize

    img = np.asarray(image, dtype=np.float64)
    img = np.squeeze(img)
    if img.ndim == 3 and img.shape[0] in (1, 3) and img.shape[-1] not in (1, 3):
        img = np.moveaxis(img, 0, -1)  # CHW -> HWC
    if img.ndim == 2:
        img = img[..., None]
    if img.shape[:2] != tuple(shape):
        img = resize(img, tuple(shape) + (img.shape[2],), anti_aliasing=True)
    lo, hi = np.percentile(img, 1), np.percentile(img, 99)
    img = np.clip((img - lo) / max(hi - lo, 1e-8), 0, 1)
    return img


def resistance_map(
    kind: ResistanceType,
    pred_mask: np.ndarray,
    image: Optional[np.ndarray] = None,
    soft_pred: Optional[np.ndarray] = None,
    smoothing: float = 1.0,
    ring_width: int = 10,
) -> np.ndarray:
    """Per-pixel resistance h(p) in [0, 1]; traversal cost is c = 1 + beta*h.

    kind:
      "uniform": h = 0               -> paper's isotropic dilation
      "region" : h = colour distance to the predicted object's mean colour,
                 normalised by the object/background contrast. Pixels that
                 *look like* the predicted object are cheap to add, background-
                 looking pixels are expensive. Uses only X and Y_hat (black-box).
      "edge"   : h = normalised gradient magnitude of the smoothed image;
                 margins slow down when crossing image edges (black-box).
      "sigmoid": h = clip(1 - 2 s, 0, 1) with s the sigmoid score: the margin
                 follows the model's own soft output (gray-box; needs logits).
    """
    pred_mask = np.asarray(pred_mask).astype(bool)
    shape = pred_mask.shape

    if kind == "uniform":
        return np.zeros(shape, dtype=np.float64)

    if kind == "sigmoid":
        if soft_pred is None:
            raise ValueError("sigmoid resistance needs soft_pred")
        s = np.squeeze(np.asarray(soft_pred, dtype=np.float64))
        return np.clip(1.0 - 2.0 * s, 0.0, 1.0)

    if image is None:
        raise ValueError(f"{kind} resistance needs the input image")
    img = _to_float_image(image, shape)
    if smoothing > 0:
        img = ndi.gaussian_filter(img, sigma=(smoothing, smoothing, 0))

    if kind == "edge":
        grad = np.zeros(shape)
        for c in range(img.shape[2]):
            gx = ndi.sobel(img[..., c], axis=0)
            gy = ndi.sobel(img[..., c], axis=1)
            grad += gx**2 + gy**2
        grad = np.sqrt(grad)
        scale = np.percentile(grad, 99)
        return np.clip(grad / max(scale, 1e-8), 0.0, 1.0)

    if kind == "region":
        if not pred_mask.any():
            return np.zeros(shape, dtype=np.float64)
        mu_in = img[pred_mask].mean(axis=0)
        ring = ndi.binary_dilation(pred_mask, iterations=ring_width) & ~pred_mask
        if not ring.any():
            return np.zeros(shape, dtype=np.float64)
        mu_out = img[ring].mean(axis=0)
        contrast = np.linalg.norm(mu_in - mu_out)
        dist = np.linalg.norm(img - mu_in, axis=-1)
        return np.clip(dist / max(contrast, 1e-3), 0.0, 1.0)

    raise ValueError(f"unknown resistance kind {kind!r}")


# --------------------------------------------------------------------------- #
#  Extension E1: geodesic distance (cost-weighted, 4-connected)
# --------------------------------------------------------------------------- #
def geodesic_distance(pred_mask: np.ndarray, cost: np.ndarray) -> np.ndarray:
    """Minimum path cost from the predicted mask to every pixel.

    Uses 4-connectivity, so with cost == 1 everywhere this equals the L1
    distance, i.e. the paper's dilation by the 3x3 cross. Moving between
    neighbours a and b costs (c(a) + c(b)) / 2 (MCP_Geometric convention).
    """
    pred_mask = np.asarray(pred_mask).astype(bool)
    if not pred_mask.any():
        return np.full(pred_mask.shape, np.inf, dtype=np.float64)
    cost = np.asarray(cost, dtype=np.float64)
    if np.any(cost < 1.0 - 1e-12):
        raise ValueError("costs must be >= 1 so that D >= L1 (keeps sets compact)")

    # Only boundary pixels of Y_hat need to be seeds (interior is dominated).
    boundary = pred_mask & ~ndi.binary_erosion(pred_mask, border_value=1)
    starts = np.argwhere(boundary)
    mcp = MCP_Geometric(cost, fully_connected=False)
    dist, _ = mcp.find_costs(starts)
    dist = np.asarray(dist, dtype=np.float64)
    dist[pred_mask] = 0.0
    return dist


def distance_map(
    pred_mask: np.ndarray,
    kind: ResistanceType = "uniform",
    beta: float = 0.0,
    image: Optional[np.ndarray] = None,
    soft_pred: Optional[np.ndarray] = None,
    resistance: Optional[np.ndarray] = None,
) -> np.ndarray:
    """D(p) for prediction sets C_lambda = {D <= lambda}.

    kind="uniform" or beta == 0 -> exact paper baseline (L1 distance).
    """
    if kind == "uniform" or beta == 0:
        return l1_distance(pred_mask)
    if resistance is None:
        resistance = resistance_map(kind, pred_mask, image=image, soft_pred=soft_pred)
    return geodesic_distance(pred_mask, 1.0 + beta * resistance)
