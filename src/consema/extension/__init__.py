"""
Extension of ConSeMa: Adaptive Geodesic Morphological Prediction Sets (AG-MPS).

The original paper builds nested prediction sets by dilating the predicted mask
lambda times with a fixed structuring element B (3x3 cross):

    C_lambda(X) = delta_B^lambda(Y_hat)

Key observation used throughout this package: lambda dilations by the 3x3 cross
is *exactly* the set of pixels whose 4-connected (taxicab / L1) distance to
Y_hat is <= lambda. Therefore the paper's method is

    C_lambda(X) = { p : D(p) <= lambda },  D = L1 distance transform of Y_hat.

We generalise D and lambda:

  E1 (geodesic, image-guided margins): D is a *geodesic* distance where each
      pixel has a traversal cost c(p) = 1 + beta * h(p) >= 1. h is a
      "resistance" map computed from the image X (black-box compatible) or,
      optionally, from the sigmoid (gray-box). beta = 0 recovers the paper.

  E2 (size-adaptive scores): the nonconformity score is divided by a scale
      sigma(Y_hat) = (1 + r_eq(Y_hat))^gamma with r_eq the equivalent radius of
      the predicted mask. At test time lambda_test = q_hat * sigma(Y_hat_test).
      gamma = 0 recovers the paper.

Both keep the family {C_t}_t nested in a scalar t, with D and sigma fixed
before calibration, so the split-conformal guarantee (Theorem 1 of the paper)
holds unchanged.
"""

from consema.extension.distances import (
    resistance_map,
    geodesic_distance,
    l1_distance,
    distance_map,
)
from consema.extension.cp import (
    nonconformity_score,
    size_scale,
    conformal_quantile,
    ImageRecord,
    build_record,
    scores_of,
    evaluate,
)

__all__ = [
    "scores_of",
    "evaluate",
    "resistance_map",
    "geodesic_distance",
    "l1_distance",
    "distance_map",
    "nonconformity_score",
    "size_scale",
    "conformal_quantile",
    "ImageRecord",
    "build_record",
]
