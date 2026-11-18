# Reproduction of Table 1 (paper protocol, official quantile index)

| dataset   |   1-alpha |   tau | Cov (ours)    |   Cov (paper) | stretch (ours)   |   stretch (paper) | lambda (ours)   |   lambda (paper) |
|:----------|----------:|------:|:--------------|--------------:|:-----------------|------------------:|:----------------|-----------------:|
| oasis     |      0.95 | 0.9   | 0.997 (0.007) |         0.997 | 1.844 (0.040)    |             1.845 | 5.194 (0.401)   |            5.194 |
| oasis     |      0.95 | 0.99  | 0.990 (0.014) |         0.99  | 2.230 (0.033)    |             2.232 | 14.194 (1.117)  |           14.222 |
| oasis     |      0.95 | 0.999 | 0.993 (0.014) |         0.993 | 2.257 (0.028)    |             2.259 | 17.889 (0.919)  |           17.917 |
| oasis     |      0.9  | 0.9   | 0.974 (0.031) |         0.969 | 1.773 (0.062)    |             1.774 | 4.500 (0.507)   |            4.5   |
| oasis     |      0.9  | 0.99  | 0.939 (0.052) |         0.941 | 2.196 (0.034)    |             2.198 | 12.333 (0.793)  |           12.333 |
| oasis     |      0.9  | 0.999 | 0.940 (0.038) |         0.94  | 2.245 (0.030)    |             2.247 | 15.417 (0.996)  |           15.417 |
| polyps    |      0.95 | 0.9   | 0.951 (0.019) |         0.953 | 2.999 (0.825)    |             3.093 | 39.833 (13.758) |           41.389 |
| polyps    |      0.95 | 0.99  | 0.952 (0.017) |         0.955 | 3.963 (0.941)    |             4.144 | 55.667 (14.406) |           58.611 |
| polyps    |      0.95 | 0.999 | 0.952 (0.017) |         0.962 | 4.352 (0.811)    |             4.84  | 61.917 (11.920) |           69.167 |
| polyps    |      0.9  | 0.9   | 0.900 (0.023) |         0.909 | 1.205 (0.091)    |             1.253 | 5.000 (2.098)   |            6.083 |
| polyps    |      0.9  | 0.99  | 0.897 (0.026) |         0.898 | 1.736 (0.247)    |             1.78  | 16.694 (5.008)  |           17.5   |
| polyps    |      0.9  | 0.999 | 0.898 (0.023) |         0.904 | 1.953 (0.294)    |             2.031 | 21.083 (5.704)  |           22.5   |
| wbc       |      0.95 | 0.9   | 0.984 (0.033) |         0.984 | 1.449 (0.365)    |             1.449 | 4.361 (3.523)   |            4.361 |
| wbc       |      0.95 | 0.99  | 0.985 (0.024) |         0.985 | 2.448 (0.664)    |             2.448 | 13.667 (5.826)  |           13.667 |
| wbc       |      0.95 | 0.999 | 0.985 (0.025) |         0.985 | 2.776 (0.735)    |             2.776 | 16.528 (6.236)  |           16.528 |
| wbc       |      0.9  | 0.9   | 0.952 (0.044) |         0.952 | 1.108 (0.065)    |             1.108 | 1.056 (0.630)   |            1.056 |
| wbc       |      0.9  | 0.99  | 0.932 (0.055) |         0.932 | 1.645 (0.261)    |             1.646 | 6.278 (2.514)   |            6.278 |
| wbc       |      0.9  | 0.999 | 0.928 (0.061) |         0.928 | 1.865 (0.284)    |             1.865 | 8.389 (2.686)   |            8.389 |

# Extension results (tune/calib/test protocol, 36 seeds)

| dataset   |   1-alpha |   tau | method                      |   coverage |   stretch |   stretch_vs_paper_% |   worst_group_cov |   stretch_small |   stretch_large |
|:----------|----------:|------:|:----------------------------|-----------:|----------:|---------------------:|------------------:|----------------:|----------------:|
| oasis     |      0.95 | 0.9   | Paper (baseline)            |      0.99  |     1.814 |                0     |             0.979 |           1.889 |           1.734 |
| oasis     |      0.95 | 0.99  | Paper (baseline)            |      0.969 |     2.213 |                0     |             0.966 |           2.323 |           2.096 |
| oasis     |      0.95 | 0.999 | Paper (baseline)            |      0.974 |     2.253 |                0     |             0.971 |           2.367 |           2.131 |
| oasis     |      0.9  | 0.9   | Paper (baseline)            |      0.963 |     1.758 |                0     |             0.925 |           1.828 |           1.684 |
| oasis     |      0.9  | 0.99  | Paper (baseline)            |      0.928 |     2.191 |                0     |             0.923 |           2.299 |           2.076 |
| oasis     |      0.9  | 0.999 | Paper (baseline)            |      0.928 |     2.242 |                0     |             0.917 |           2.355 |           2.121 |
| polyps    |      0.95 | 0.9   | Paper (baseline)            |      0.947 |     2.755 |                0     |             0.923 |           4.087 |           1.782 |
| polyps    |      0.95 | 0.99  | Paper (baseline)            |      0.945 |     3.602 |                0     |             0.918 |           5.722 |           2.068 |
| polyps    |      0.95 | 0.999 | Paper (baseline)            |      0.946 |     4.006 |                0     |             0.919 |           6.517 |           2.197 |
| polyps    |      0.9  | 0.9   | Paper (baseline)            |      0.894 |     1.226 |                0     |             0.84  |           1.363 |           1.126 |
| polyps    |      0.9  | 0.99  | Paper (baseline)            |      0.893 |     1.771 |                0     |             0.834 |           2.279 |           1.395 |
| polyps    |      0.9  | 0.999 | Paper (baseline)            |      0.893 |     1.985 |                0     |             0.831 |           2.659 |           1.491 |
| wbc       |      0.95 | 0.9   | Paper (baseline)            |      0.969 |     1.22  |                0     |             0.95  |           1.269 |           1.175 |
| wbc       |      0.95 | 0.99  | Paper (baseline)            |      0.962 |     1.906 |                0     |             0.927 |           2.105 |           1.724 |
| wbc       |      0.95 | 0.999 | Paper (baseline)            |      0.967 |     2.163 |                0     |             0.942 |           2.416 |           1.93  |
| wbc       |      0.9  | 0.9   | Paper (baseline)            |      0.943 |     1.088 |                0     |             0.904 |           1.108 |           1.07  |
| wbc       |      0.9  | 0.99  | Paper (baseline)            |      0.921 |     1.545 |                0     |             0.866 |           1.666 |           1.433 |
| wbc       |      0.9  | 0.999 | Paper (baseline)            |      0.913 |     1.778 |                0     |             0.845 |           1.948 |           1.619 |
| oasis     |      0.95 | 0.9   | E2: size-adaptive           |      0.967 |     1.803 |               -0.585 |             0.917 |           1.859 |           1.734 |
| oasis     |      0.95 | 0.99  | E2: size-adaptive           |      0.956 |     2.205 |               -0.349 |             0.938 |           2.305 |           2.097 |
| oasis     |      0.95 | 0.999 | E2: size-adaptive           |      0.964 |     2.25  |               -0.132 |             0.945 |           2.36  |           2.131 |
| oasis     |      0.9  | 0.9   | E2: size-adaptive           |      0.913 |     1.737 |               -1.159 |             0.799 |           1.78  |           1.683 |
| oasis     |      0.9  | 0.99  | E2: size-adaptive           |      0.906 |     2.181 |               -0.468 |             0.884 |           2.276 |           2.078 |
| oasis     |      0.9  | 0.999 | E2: size-adaptive           |      0.907 |     2.237 |               -0.216 |             0.873 |           2.343 |           2.123 |
| polyps    |      0.95 | 0.9   | E2: size-adaptive           |      0.946 |     2.074 |              -20.863 |             0.93  |           2.032 |           2.083 |
| polyps    |      0.95 | 0.99  | E2: size-adaptive           |      0.945 |     2.562 |              -25.747 |             0.923 |           2.444 |           2.552 |
| polyps    |      0.95 | 0.999 | E2: size-adaptive           |      0.944 |     2.723 |              -30.221 |             0.921 |           2.643 |           2.638 |
| polyps    |      0.9  | 0.9   | E2: size-adaptive           |      0.894 |     1.195 |               -2.005 |             0.859 |           1.182 |           1.218 |
| polyps    |      0.9  | 0.99  | E2: size-adaptive           |      0.894 |     1.661 |               -5.082 |             0.86  |           1.803 |           1.548 |
| polyps    |      0.9  | 0.999 | E2: size-adaptive           |      0.894 |     1.785 |               -8.667 |             0.859 |           1.942 |           1.645 |
| wbc       |      0.95 | 0.9   | E2: size-adaptive           |      0.961 |     1.157 |               -4.894 |             0.95  |           1.14  |           1.16  |
| wbc       |      0.95 | 0.99  | E2: size-adaptive           |      0.965 |     1.798 |               -5.325 |             0.95  |           1.786 |           1.829 |
| wbc       |      0.95 | 0.999 | E2: size-adaptive           |      0.965 |     2.051 |               -4.867 |             0.949 |           2.063 |           2.066 |
| wbc       |      0.9  | 0.9   | E2: size-adaptive           |      0.922 |     1.053 |               -3.139 |             0.896 |           1.045 |           1.061 |
| wbc       |      0.9  | 0.99  | E2: size-adaptive           |      0.903 |     1.434 |               -6.868 |             0.889 |           1.422 |           1.452 |
| wbc       |      0.9  | 0.999 | E2: size-adaptive           |      0.906 |     1.628 |               -7.863 |             0.887 |           1.607 |           1.662 |
| oasis     |      0.95 | 0.9   | E1: geodesic (black-box)    |      0.976 |     1.351 |              -25.461 |             0.959 |           1.395 |           1.306 |
| oasis     |      0.95 | 0.99  | E1: geodesic (black-box)    |      0.954 |     1.547 |              -30.104 |             0.94  |           1.618 |           1.474 |
| oasis     |      0.95 | 0.999 | E1: geodesic (black-box)    |      0.957 |     2.18  |               -3.243 |             0.944 |           2.277 |           2.076 |
| oasis     |      0.9  | 0.9   | E1: geodesic (black-box)    |      0.937 |     1.336 |              -23.92  |             0.887 |           1.378 |           1.294 |
| oasis     |      0.9  | 0.99  | E1: geodesic (black-box)    |      0.899 |     1.526 |              -30.355 |             0.884 |           1.596 |           1.454 |
| oasis     |      0.9  | 0.999 | E1: geodesic (black-box)    |      0.892 |     2.06  |               -8.098 |             0.869 |           2.151 |           1.963 |
| polyps    |      0.95 | 0.9   | E1: geodesic (black-box)    |      0.945 |     2.868 |                5.34  |             0.918 |           4.451 |           1.773 |
| polyps    |      0.95 | 0.99  | E1: geodesic (black-box)    |      0.946 |     3.765 |                5.497 |             0.918 |           6.149 |           2.086 |
| polyps    |      0.95 | 0.999 | E1: geodesic (black-box)    |      0.947 |     4.2   |                5.298 |             0.919 |           6.958 |           2.231 |
| polyps    |      0.9  | 0.9   | E1: geodesic (black-box)    |      0.894 |     1.222 |               -0.419 |             0.839 |           1.367 |           1.121 |
| polyps    |      0.9  | 0.99  | E1: geodesic (black-box)    |      0.89  |     1.78  |                0.887 |             0.831 |           2.328 |           1.388 |
| polyps    |      0.9  | 0.999 | E1: geodesic (black-box)    |      0.891 |     2.005 |                1.133 |             0.829 |           2.707 |           1.493 |
| wbc       |      0.95 | 0.9   | E1: geodesic (black-box)    |      0.963 |     1.083 |              -10.409 |             0.944 |           1.089 |           1.08  |
| wbc       |      0.95 | 0.99  | E1: geodesic (black-box)    |      0.958 |     1.348 |              -27.757 |             0.913 |           1.398 |           1.312 |
| wbc       |      0.95 | 0.999 | E1: geodesic (black-box)    |      0.96  |     1.52  |              -28.628 |             0.916 |           1.601 |           1.458 |
| wbc       |      0.9  | 0.9   | E1: geodesic (black-box)    |      0.923 |     1.039 |               -4.354 |             0.886 |           1.045 |           1.033 |
| wbc       |      0.9  | 0.99  | E1: geodesic (black-box)    |      0.897 |     1.213 |              -20.37  |             0.801 |           1.239 |           1.195 |
| wbc       |      0.9  | 0.999 | E1: geodesic (black-box)    |      0.892 |     1.329 |              -24.121 |             0.779 |           1.373 |           1.295 |
| oasis     |      0.95 | 0.9   | AG-MPS (black-box, E1+E2)   |      0.969 |     1.35  |              -25.523 |             0.94  |           1.393 |           1.306 |
| oasis     |      0.95 | 0.99  | AG-MPS (black-box, E1+E2)   |      0.954 |     1.547 |              -30.072 |             0.947 |           1.615 |           1.479 |
| oasis     |      0.95 | 0.999 | AG-MPS (black-box, E1+E2)   |      0.956 |     2.179 |               -3.275 |             0.939 |           2.273 |           2.079 |
| oasis     |      0.9  | 0.9   | AG-MPS (black-box, E1+E2)   |      0.926 |     1.336 |              -23.935 |             0.854 |           1.375 |           1.295 |
| oasis     |      0.9  | 0.99  | AG-MPS (black-box, E1+E2)   |      0.891 |     1.526 |              -30.35  |             0.885 |           1.593 |           1.458 |
| oasis     |      0.9  | 0.999 | AG-MPS (black-box, E1+E2)   |      0.895 |     2.059 |               -8.154 |             0.874 |           2.144 |           1.969 |
| polyps    |      0.95 | 0.9   | AG-MPS (black-box, E1+E2)   |      0.945 |     2.004 |              -24.489 |             0.929 |           2.058 |           2.006 |
| polyps    |      0.95 | 0.99  | AG-MPS (black-box, E1+E2)   |      0.945 |     2.751 |              -20.81  |             0.92  |           2.858 |           2.574 |
| polyps    |      0.95 | 0.999 | AG-MPS (black-box, E1+E2)   |      0.946 |     2.997 |              -23.258 |             0.923 |           3.156 |           2.701 |
| polyps    |      0.9  | 0.9   | AG-MPS (black-box, E1+E2)   |      0.895 |     1.186 |               -2.707 |             0.86  |           1.182 |           1.21  |
| polyps    |      0.9  | 0.99  | AG-MPS (black-box, E1+E2)   |      0.893 |     1.658 |               -5.215 |             0.854 |           1.852 |           1.509 |
| polyps    |      0.9  | 0.999 | AG-MPS (black-box, E1+E2)   |      0.892 |     1.821 |               -7.121 |             0.863 |           2.004 |           1.663 |
| wbc       |      0.95 | 0.9   | AG-MPS (black-box, E1+E2)   |      0.965 |     1.084 |              -10.273 |             0.952 |           1.078 |           1.093 |
| wbc       |      0.95 | 0.99  | AG-MPS (black-box, E1+E2)   |      0.963 |     1.311 |              -29.514 |             0.944 |           1.302 |           1.332 |
| wbc       |      0.95 | 0.999 | AG-MPS (black-box, E1+E2)   |      0.968 |     1.456 |              -31.308 |             0.949 |           1.441 |           1.49  |
| wbc       |      0.9  | 0.9   | AG-MPS (black-box, E1+E2)   |      0.919 |     1.04  |               -4.291 |             0.888 |           1.04  |           1.04  |
| wbc       |      0.9  | 0.99  | AG-MPS (black-box, E1+E2)   |      0.898 |     1.206 |              -20.781 |             0.846 |           1.196 |           1.221 |
| wbc       |      0.9  | 0.999 | AG-MPS (black-box, E1+E2)   |      0.9   |     1.318 |              -24.698 |             0.857 |           1.309 |           1.338 |
| oasis     |      0.95 | 0.9   | AG-MPS (gray-box, +sigmoid) |      0.969 |     1.35  |              -25.523 |             0.94  |           1.393 |           1.306 |
| oasis     |      0.95 | 0.99  | AG-MPS (gray-box, +sigmoid) |      0.954 |     1.547 |              -30.072 |             0.947 |           1.615 |           1.479 |
| oasis     |      0.95 | 0.999 | AG-MPS (gray-box, +sigmoid) |      0.957 |     2.176 |               -3.406 |             0.945 |           2.273 |           2.073 |
| oasis     |      0.9  | 0.9   | AG-MPS (gray-box, +sigmoid) |      0.926 |     1.336 |              -23.935 |             0.854 |           1.375 |           1.295 |
| oasis     |      0.9  | 0.99  | AG-MPS (gray-box, +sigmoid) |      0.891 |     1.526 |              -30.35  |             0.885 |           1.593 |           1.458 |
| oasis     |      0.9  | 0.999 | AG-MPS (gray-box, +sigmoid) |      0.895 |     2.058 |               -8.183 |             0.877 |           2.145 |           1.966 |
| polyps    |      0.95 | 0.9   | AG-MPS (gray-box, +sigmoid) |      0.946 |     1.788 |              -32.446 |             0.931 |           1.833 |           1.774 |
| polyps    |      0.95 | 0.99  | AG-MPS (gray-box, +sigmoid) |      0.946 |     2.132 |              -37.989 |             0.927 |           2.195 |           2.075 |
| polyps    |      0.95 | 0.999 | AG-MPS (gray-box, +sigmoid) |      0.944 |     2.349 |              -39.434 |             0.93  |           2.508 |           2.192 |
| polyps    |      0.9  | 0.9   | AG-MPS (gray-box, +sigmoid) |      0.895 |     1.176 |               -3.488 |             0.86  |           1.177 |           1.194 |
| polyps    |      0.9  | 0.99  | AG-MPS (gray-box, +sigmoid) |      0.891 |     1.526 |              -12.433 |             0.862 |           1.674 |           1.419 |
| polyps    |      0.9  | 0.999 | AG-MPS (gray-box, +sigmoid) |      0.893 |     1.662 |              -14.816 |             0.865 |           1.834 |           1.531 |
| wbc       |      0.95 | 0.9   | AG-MPS (gray-box, +sigmoid) |      0.965 |     1.084 |              -10.273 |             0.952 |           1.078 |           1.093 |
| wbc       |      0.95 | 0.99  | AG-MPS (gray-box, +sigmoid) |      0.963 |     1.311 |              -29.514 |             0.944 |           1.302 |           1.332 |
| wbc       |      0.95 | 0.999 | AG-MPS (gray-box, +sigmoid) |      0.968 |     1.456 |              -31.308 |             0.949 |           1.441 |           1.49  |
| wbc       |      0.9  | 0.9   | AG-MPS (gray-box, +sigmoid) |      0.919 |     1.04  |               -4.281 |             0.886 |           1.04  |           1.04  |
| wbc       |      0.9  | 0.99  | AG-MPS (gray-box, +sigmoid) |      0.898 |     1.206 |              -20.781 |             0.846 |           1.196 |           1.221 |
| wbc       |      0.9  | 0.999 | AG-MPS (gray-box, +sigmoid) |      0.9   |     1.318 |              -24.698 |             0.857 |           1.309 |           1.338 |

# Selected hyper-parameters (counts over seeds x settings)

| dataset   | kind    |   beta |   gamma |   count | model     |
|:----------|:--------|-------:|--------:|--------:|:----------|
| oasis     | edge    |    8   |    0    |       2 | black-box |
| oasis     | edge    |   16   |    0    |       2 | black-box |
| oasis     | edge    |   32   |    0    |      23 | black-box |
| oasis     | edge    |   32   |    0.25 |      10 | black-box |
| oasis     | edge    |   32   |    0.5  |      13 | black-box |
| oasis     | edge    |   32   |    0.75 |       4 | black-box |
| oasis     | edge    |   32   |    1    |      10 | black-box |
| oasis     | edge    |   32   |    1.25 |       4 | black-box |
| oasis     | edge    |   32   |    1.5  |       4 | black-box |
| oasis     | edge    |   32   |    1.75 |       2 | black-box |
| oasis     | edge    |   32   |    2    |      10 | black-box |
| oasis     | edge    |   64   |    0    |      14 | black-box |
| oasis     | edge    |   64   |    0.25 |       2 | black-box |
| oasis     | edge    |   64   |    0.5  |       2 | black-box |
| oasis     | edge    |   64   |    0.75 |       1 | black-box |
| oasis     | edge    |   64   |    1    |       1 | black-box |
| oasis     | edge    |   64   |    1.25 |       4 | black-box |
| oasis     | edge    |   64   |    1.5  |       3 | black-box |
| oasis     | edge    |   64   |    1.75 |       1 | black-box |
| oasis     | edge    |   64   |    2    |       2 | black-box |
| oasis     | edge    |  128   |    0    |      15 | black-box |
| oasis     | edge    |  128   |    0.25 |       4 | black-box |
| oasis     | edge    |  128   |    0.5  |       1 | black-box |
| oasis     | edge    |  128   |    0.75 |       2 | black-box |
| oasis     | edge    |  256   |    0    |      21 | black-box |
| oasis     | edge    |  256   |    0.25 |       4 | black-box |
| oasis     | edge    |  256   |    0.5  |       1 | black-box |
| oasis     | edge    |  256   |    0.75 |       3 | black-box |
| oasis     | edge    |  256   |    1    |       2 | black-box |
| oasis     | edge    |  256   |    1.25 |       4 | black-box |
| oasis     | edge    |  256   |    1.5  |       1 | black-box |
| oasis     | edge    |  256   |    1.75 |       2 | black-box |
| oasis     | edge    |  256   |    2    |       2 | black-box |
| oasis     | region  |    0.5 |    0.5  |       1 | black-box |
| oasis     | region  |    1   |    0    |       4 | black-box |
| oasis     | region  |    1   |    0.25 |       1 | black-box |
| oasis     | region  |    2   |    0    |       5 | black-box |
| oasis     | region  |    2   |    0.25 |       1 | black-box |
| oasis     | region  |    2   |    0.5  |       1 | black-box |
| oasis     | region  |    2   |    0.75 |       1 | black-box |
| oasis     | region  |    2   |    2    |       2 | black-box |
| oasis     | region  |    4   |    0    |       6 | black-box |
| oasis     | region  |    4   |    0.25 |       1 | black-box |
| oasis     | region  |    4   |    1.25 |       1 | black-box |
| oasis     | region  |    8   |    0    |       4 | black-box |
| oasis     | region  |    8   |    0.25 |       1 | black-box |
| oasis     | region  |    8   |    0.75 |       1 | black-box |
| oasis     | region  |    8   |    1.75 |       1 | black-box |
| oasis     | region  |    8   |    2    |       2 | black-box |
| oasis     | region  |   16   |    0    |       2 | black-box |
| oasis     | region  |   32   |    0    |       1 | black-box |
| oasis     | region  |   64   |    0    |       1 | black-box |
| oasis     | region  |   64   |    0.5  |       1 | black-box |
| oasis     | region  |  256   |    0.25 |       1 | black-box |
| oasis     | region  |  256   |    1    |       1 | black-box |
| polyps    | edge    |    0.5 |    0    |       3 | black-box |
| polyps    | edge    |    0.5 |    0.25 |       2 | black-box |
| polyps    | edge    |    0.5 |    0.75 |       3 | black-box |
| polyps    | edge    |    0.5 |    1    |       2 | black-box |
| polyps    | edge    |    0.5 |    1.5  |       2 | black-box |
| polyps    | edge    |    0.5 |    1.75 |       1 | black-box |
| polyps    | edge    |    0.5 |    2    |       2 | black-box |
| polyps    | edge    |    1   |    0    |       2 | black-box |
| polyps    | edge    |    1   |    0.25 |       2 | black-box |
| polyps    | edge    |    1   |    0.5  |       4 | black-box |
| polyps    | edge    |    1   |    0.75 |       1 | black-box |
| polyps    | edge    |    1   |    1    |       2 | black-box |
| polyps    | edge    |    1   |    1.75 |       3 | black-box |
| polyps    | edge    |    2   |    0    |       2 | black-box |
| polyps    | edge    |    2   |    0.25 |       1 | black-box |
| polyps    | edge    |    2   |    0.5  |       3 | black-box |
| polyps    | edge    |    2   |    0.75 |       3 | black-box |
| polyps    | edge    |    2   |    1    |       5 | black-box |
| polyps    | edge    |    2   |    1.25 |       1 | black-box |
| polyps    | edge    |    2   |    1.5  |       1 | black-box |
| polyps    | edge    |    2   |    1.75 |       1 | black-box |
| polyps    | edge    |    2   |    2    |       1 | black-box |
| polyps    | edge    |    4   |    0    |       3 | black-box |
| polyps    | edge    |    4   |    0.25 |       2 | black-box |
| polyps    | edge    |    4   |    0.5  |       5 | black-box |
| polyps    | edge    |    4   |    0.75 |       3 | black-box |
| polyps    | edge    |    4   |    1    |       4 | black-box |
| polyps    | edge    |    4   |    1.25 |       1 | black-box |
| polyps    | edge    |    4   |    1.5  |       1 | black-box |
| polyps    | edge    |    4   |    1.75 |       1 | black-box |
| polyps    | edge    |    8   |    0    |       1 | black-box |
| polyps    | edge    |    8   |    0.25 |       4 | black-box |
| polyps    | edge    |    8   |    0.5  |       1 | black-box |
| polyps    | edge    |    8   |    0.75 |       4 | black-box |
| polyps    | edge    |    8   |    1.25 |       1 | black-box |
| polyps    | edge    |    8   |    1.5  |       1 | black-box |
| polyps    | edge    |    8   |    1.75 |       3 | black-box |
| polyps    | edge    |    8   |    2    |       1 | black-box |
| polyps    | edge    |   16   |    0    |       1 | black-box |
| polyps    | edge    |   16   |    0.25 |       3 | black-box |
| polyps    | edge    |   16   |    0.5  |       2 | black-box |
| polyps    | edge    |   16   |    0.75 |       3 | black-box |
| polyps    | edge    |   16   |    1    |       2 | black-box |
| polyps    | edge    |   16   |    1.25 |       2 | black-box |
| polyps    | edge    |   16   |    1.5  |       2 | black-box |
| polyps    | edge    |   16   |    1.75 |       1 | black-box |
| polyps    | edge    |   16   |    2    |       2 | black-box |
| polyps    | edge    |   32   |    0    |       1 | black-box |
| polyps    | edge    |   32   |    0.5  |       1 | black-box |
| polyps    | edge    |   32   |    0.75 |       1 | black-box |
| polyps    | edge    |   32   |    1.25 |       2 | black-box |
| polyps    | edge    |   32   |    1.5  |       2 | black-box |
| polyps    | edge    |   32   |    1.75 |       1 | black-box |
| polyps    | edge    |   32   |    2    |       6 | black-box |
| polyps    | edge    |   64   |    0    |       1 | black-box |
| polyps    | edge    |   64   |    1    |       2 | black-box |
| polyps    | edge    |   64   |    1.25 |       3 | black-box |
| polyps    | edge    |   64   |    1.5  |       1 | black-box |
| polyps    | edge    |   64   |    2    |       2 | black-box |
| polyps    | edge    |  128   |    0    |       3 | black-box |
| polyps    | edge    |  128   |    0.5  |       1 | black-box |
| polyps    | edge    |  128   |    0.75 |       1 | black-box |
| polyps    | edge    |  128   |    1.5  |       1 | black-box |
| polyps    | edge    |  128   |    2    |       3 | black-box |
| polyps    | edge    |  256   |    0    |       1 | black-box |
| polyps    | edge    |  256   |    0.5  |       1 | black-box |
| polyps    | edge    |  256   |    1    |       1 | black-box |
| polyps    | edge    |  256   |    1.5  |       3 | black-box |
| polyps    | edge    |  256   |    2    |       1 | black-box |
| polyps    | region  |    0.5 |    0    |       3 | black-box |
| polyps    | region  |    0.5 |    0.5  |       2 | black-box |
| polyps    | region  |    0.5 |    0.75 |       1 | black-box |
| polyps    | region  |    0.5 |    1    |       2 | black-box |
| polyps    | region  |    0.5 |    1.25 |       6 | black-box |
| polyps    | region  |    0.5 |    1.75 |       2 | black-box |
| polyps    | region  |    0.5 |    2    |       2 | black-box |
| polyps    | region  |    1   |    0.25 |       2 | black-box |
| polyps    | region  |    1   |    0.5  |       1 | black-box |
| polyps    | region  |    1   |    1    |       1 | black-box |
| polyps    | region  |    1   |    1.25 |       5 | black-box |
| polyps    | region  |    1   |    1.5  |       1 | black-box |
| polyps    | region  |    1   |    1.75 |       2 | black-box |
| polyps    | region  |    1   |    2    |       4 | black-box |
| polyps    | region  |    2   |    0.5  |       1 | black-box |
| polyps    | region  |    2   |    1    |       1 | black-box |
| polyps    | region  |    2   |    1.25 |       1 | black-box |
| polyps    | region  |    2   |    1.5  |       1 | black-box |
| polyps    | region  |    2   |    1.75 |       1 | black-box |
| polyps    | region  |    2   |    2    |       1 | black-box |
| polyps    | region  |    4   |    0.25 |       1 | black-box |
| polyps    | region  |    4   |    1.25 |       1 | black-box |
| polyps    | region  |    4   |    1.5  |       2 | black-box |
| polyps    | region  |    4   |    2    |       4 | black-box |
| polyps    | region  |    8   |    0.5  |       1 | black-box |
| polyps    | region  |    8   |    0.75 |       1 | black-box |
| polyps    | region  |    8   |    2    |       2 | black-box |
| polyps    | region  |   16   |    1.5  |       1 | black-box |
| polyps    | uniform |    0   |    0    |       4 | black-box |
| polyps    | uniform |    0   |    0.25 |       3 | black-box |
| polyps    | uniform |    0   |    0.5  |       2 | black-box |
| polyps    | uniform |    0   |    0.75 |       4 | black-box |
| polyps    | uniform |    0   |    1    |       2 | black-box |
| polyps    | uniform |    0   |    1.5  |       6 | black-box |
| polyps    | uniform |    0   |    1.75 |       1 | black-box |
| polyps    | uniform |    0   |    2    |       1 | black-box |
| wbc       | edge    |    0.5 |    1.25 |       1 | black-box |
| wbc       | edge    |    1   |    1.75 |       1 | black-box |
| wbc       | edge    |    8   |    2    |       1 | black-box |
| wbc       | region  |    0.5 |    0    |       6 | black-box |
| wbc       | region  |    0.5 |    2    |       2 | black-box |
| wbc       | region  |    1   |    0.5  |       1 | black-box |
| wbc       | region  |    1   |    0.75 |       2 | black-box |
| wbc       | region  |    1   |    1.25 |       1 | black-box |
| wbc       | region  |    1   |    1.5  |       1 | black-box |
| wbc       | region  |    2   |    0.25 |       2 | black-box |
| wbc       | region  |    2   |    2    |       1 | black-box |
| wbc       | region  |    4   |    1    |       1 | black-box |
| wbc       | region  |    4   |    1.75 |       1 | black-box |
| wbc       | region  |    4   |    2    |       1 | black-box |
| wbc       | region  |    8   |    0    |       1 | black-box |
| wbc       | region  |    8   |    1.5  |       1 | black-box |
| wbc       | region  |    8   |    2    |       1 | black-box |
| wbc       | region  |   16   |    0    |       4 | black-box |
| wbc       | region  |   16   |    0.75 |       2 | black-box |
| wbc       | region  |   16   |    1    |       1 | black-box |
| wbc       | region  |   16   |    1.5  |       3 | black-box |
| wbc       | region  |   16   |    1.75 |       4 | black-box |
| wbc       | region  |   16   |    2    |       5 | black-box |
| wbc       | region  |   32   |    0    |       1 | black-box |
| wbc       | region  |   32   |    0.25 |       1 | black-box |
| wbc       | region  |   32   |    0.5  |       2 | black-box |
| wbc       | region  |   32   |    0.75 |       1 | black-box |
| wbc       | region  |   32   |    1    |       3 | black-box |
| wbc       | region  |   32   |    1.5  |       1 | black-box |
| wbc       | region  |   32   |    1.75 |       2 | black-box |
| wbc       | region  |   32   |    2    |       6 | black-box |
| wbc       | region  |   64   |    0    |       3 | black-box |
| wbc       | region  |   64   |    0.25 |       3 | black-box |
| wbc       | region  |   64   |    0.5  |       2 | black-box |
| wbc       | region  |   64   |    1    |       1 | black-box |
| wbc       | region  |   64   |    1.5  |       3 | black-box |
| wbc       | region  |   64   |    1.75 |       3 | black-box |
| wbc       | region  |   64   |    2    |       5 | black-box |
| wbc       | region  |  128   |    0    |       1 | black-box |
| wbc       | region  |  128   |    0.25 |       1 | black-box |
| wbc       | region  |  128   |    0.5  |       2 | black-box |
| wbc       | region  |  128   |    0.75 |       2 | black-box |
| wbc       | region  |  128   |    1    |       3 | black-box |
| wbc       | region  |  128   |    1.25 |       3 | black-box |
| wbc       | region  |  128   |    1.5  |       2 | black-box |
| wbc       | region  |  128   |    1.75 |       2 | black-box |
| wbc       | region  |  128   |    2    |       6 | black-box |
| wbc       | region  |  256   |    0    |      14 | black-box |
| wbc       | region  |  256   |    0.25 |       7 | black-box |
| wbc       | region  |  256   |    0.5  |       4 | black-box |
| wbc       | region  |  256   |    0.75 |       5 | black-box |
| wbc       | region  |  256   |    1    |      11 | black-box |
| wbc       | region  |  256   |    1.25 |       8 | black-box |
| wbc       | region  |  256   |    1.5  |       9 | black-box |
| wbc       | region  |  256   |    1.75 |      15 | black-box |
| wbc       | region  |  256   |    2    |      29 | black-box |
| wbc       | uniform |    0   |    0    |      10 | black-box |
| wbc       | uniform |    0   |    1.5  |       1 | black-box |
| oasis     | edge    |    8   |    0    |       2 | gray-box  |
| oasis     | edge    |   16   |    0    |       2 | gray-box  |
| oasis     | edge    |   32   |    0    |      23 | gray-box  |
| oasis     | edge    |   32   |    0.25 |      10 | gray-box  |
| oasis     | edge    |   32   |    0.5  |      13 | gray-box  |
| oasis     | edge    |   32   |    0.75 |       4 | gray-box  |
| oasis     | edge    |   32   |    1    |      10 | gray-box  |
| oasis     | edge    |   32   |    1.25 |       4 | gray-box  |
| oasis     | edge    |   32   |    1.5  |       4 | gray-box  |
| oasis     | edge    |   32   |    1.75 |       2 | gray-box  |
| oasis     | edge    |   32   |    2    |      10 | gray-box  |
| oasis     | edge    |   64   |    0    |      14 | gray-box  |
| oasis     | edge    |   64   |    0.25 |       2 | gray-box  |
| oasis     | edge    |   64   |    0.5  |       2 | gray-box  |
| oasis     | edge    |   64   |    0.75 |       1 | gray-box  |
| oasis     | edge    |   64   |    1    |       1 | gray-box  |
| oasis     | edge    |   64   |    1.25 |       4 | gray-box  |
| oasis     | edge    |   64   |    1.5  |       3 | gray-box  |
| oasis     | edge    |   64   |    1.75 |       1 | gray-box  |
| oasis     | edge    |   64   |    2    |       2 | gray-box  |
| oasis     | edge    |  128   |    0    |      15 | gray-box  |
| oasis     | edge    |  128   |    0.25 |       4 | gray-box  |
| oasis     | edge    |  128   |    0.5  |       1 | gray-box  |
| oasis     | edge    |  128   |    0.75 |       2 | gray-box  |
| oasis     | edge    |  256   |    0    |      21 | gray-box  |
| oasis     | edge    |  256   |    0.25 |       4 | gray-box  |
| oasis     | edge    |  256   |    0.5  |       1 | gray-box  |
| oasis     | edge    |  256   |    0.75 |       3 | gray-box  |
| oasis     | edge    |  256   |    1    |       2 | gray-box  |
| oasis     | edge    |  256   |    1.25 |       4 | gray-box  |
| oasis     | edge    |  256   |    1.5  |       1 | gray-box  |
| oasis     | edge    |  256   |    1.75 |       2 | gray-box  |
| oasis     | edge    |  256   |    2    |       2 | gray-box  |
| oasis     | region  |    2   |    0.25 |       1 | gray-box  |
| oasis     | region  |    2   |    0.75 |       1 | gray-box  |
| oasis     | region  |    4   |    0    |       4 | gray-box  |
| oasis     | region  |    4   |    0.25 |       1 | gray-box  |
| oasis     | region  |    4   |    1.25 |       1 | gray-box  |
| oasis     | region  |    8   |    0    |       2 | gray-box  |
| oasis     | region  |    8   |    0.25 |       1 | gray-box  |
| oasis     | region  |    8   |    0.75 |       1 | gray-box  |
| oasis     | region  |    8   |    1.75 |       1 | gray-box  |
| oasis     | region  |    8   |    2    |       1 | gray-box  |
| oasis     | region  |   16   |    0    |       2 | gray-box  |
| oasis     | region  |   32   |    0    |       1 | gray-box  |
| oasis     | region  |   64   |    0    |       1 | gray-box  |
| oasis     | region  |   64   |    0.5  |       1 | gray-box  |
| oasis     | region  |  256   |    0.25 |       1 | gray-box  |
| oasis     | region  |  256   |    1    |       1 | gray-box  |
| oasis     | sigmoid |    4   |    1.5  |       1 | gray-box  |
| oasis     | sigmoid |   16   |    0    |       1 | gray-box  |
| oasis     | sigmoid |  128   |    0.25 |       1 | gray-box  |
| oasis     | sigmoid |  128   |    1.5  |       1 | gray-box  |
| oasis     | sigmoid |  256   |    0    |       6 | gray-box  |
| oasis     | sigmoid |  256   |    0.25 |       1 | gray-box  |
| oasis     | sigmoid |  256   |    0.75 |       1 | gray-box  |
| oasis     | sigmoid |  256   |    1    |       2 | gray-box  |
| oasis     | sigmoid |  256   |    1.75 |       1 | gray-box  |
| oasis     | sigmoid |  256   |    2    |       4 | gray-box  |
| polyps    | edge    |    0.5 |    0    |       2 | gray-box  |
| polyps    | edge    |    0.5 |    0.75 |       1 | gray-box  |
| polyps    | edge    |    4   |    0    |       1 | gray-box  |
| polyps    | edge    |    4   |    0.5  |       1 | gray-box  |
| polyps    | edge    |    4   |    0.75 |       2 | gray-box  |
| polyps    | edge    |    8   |    0.25 |       2 | gray-box  |
| polyps    | edge    |   16   |    0.25 |       1 | gray-box  |
| polyps    | edge    |   16   |    2    |       1 | gray-box  |
| polyps    | edge    |   32   |    0    |       1 | gray-box  |
| polyps    | edge    |   32   |    0.5  |       1 | gray-box  |
| polyps    | edge    |   32   |    1.5  |       1 | gray-box  |
| polyps    | edge    |   32   |    2    |       5 | gray-box  |
| polyps    | edge    |  128   |    0    |       1 | gray-box  |
| polyps    | edge    |  128   |    0.5  |       1 | gray-box  |
| polyps    | edge    |  128   |    0.75 |       1 | gray-box  |
| polyps    | edge    |  128   |    1.5  |       1 | gray-box  |
| polyps    | edge    |  128   |    2    |       3 | gray-box  |
| polyps    | edge    |  256   |    0.5  |       1 | gray-box  |
| polyps    | edge    |  256   |    1.5  |       2 | gray-box  |
| polyps    | region  |    0.5 |    0    |       1 | gray-box  |
| polyps    | region  |    2   |    1.75 |       1 | gray-box  |
| polyps    | region  |    4   |    0.25 |       1 | gray-box  |
| polyps    | region  |    4   |    2    |       3 | gray-box  |
| polyps    | region  |    8   |    2    |       1 | gray-box  |
| polyps    | sigmoid |    0.5 |    0    |       3 | gray-box  |
| polyps    | sigmoid |    0.5 |    0.5  |       1 | gray-box  |
| polyps    | sigmoid |    0.5 |    2    |       1 | gray-box  |
| polyps    | sigmoid |    1   |    0    |       3 | gray-box  |
| polyps    | sigmoid |    1   |    0.75 |       1 | gray-box  |
| polyps    | sigmoid |    2   |    0    |       1 | gray-box  |
| polyps    | sigmoid |    2   |    0.5  |       1 | gray-box  |
| polyps    | sigmoid |    2   |    0.75 |       2 | gray-box  |
| polyps    | sigmoid |    2   |    1    |       2 | gray-box  |
| polyps    | sigmoid |    2   |    2    |       2 | gray-box  |
| polyps    | sigmoid |    4   |    0    |       2 | gray-box  |
| polyps    | sigmoid |    4   |    0.25 |       5 | gray-box  |
| polyps    | sigmoid |    4   |    0.5  |       1 | gray-box  |
| polyps    | sigmoid |    4   |    0.75 |       4 | gray-box  |
| polyps    | sigmoid |    4   |    1    |       2 | gray-box  |
| polyps    | sigmoid |    4   |    1.5  |       1 | gray-box  |
| polyps    | sigmoid |    4   |    2    |       2 | gray-box  |
| polyps    | sigmoid |    8   |    0    |       2 | gray-box  |
| polyps    | sigmoid |    8   |    0.25 |       1 | gray-box  |
| polyps    | sigmoid |    8   |    0.75 |       3 | gray-box  |
| polyps    | sigmoid |    8   |    1    |       1 | gray-box  |
| polyps    | sigmoid |    8   |    1.25 |       3 | gray-box  |
| polyps    | sigmoid |    8   |    1.5  |       6 | gray-box  |
| polyps    | sigmoid |   16   |    0    |       4 | gray-box  |
| polyps    | sigmoid |   16   |    0.5  |       1 | gray-box  |
| polyps    | sigmoid |   16   |    0.75 |       3 | gray-box  |
| polyps    | sigmoid |   16   |    1    |       3 | gray-box  |
| polyps    | sigmoid |   16   |    1.25 |       2 | gray-box  |
| polyps    | sigmoid |   16   |    1.5  |       3 | gray-box  |
| polyps    | sigmoid |   16   |    1.75 |       1 | gray-box  |
| polyps    | sigmoid |   32   |    0    |       2 | gray-box  |
| polyps    | sigmoid |   32   |    0.5  |       4 | gray-box  |
| polyps    | sigmoid |   32   |    1.25 |       2 | gray-box  |
| polyps    | sigmoid |   32   |    2    |       1 | gray-box  |
| polyps    | sigmoid |   64   |    0    |       2 | gray-box  |
| polyps    | sigmoid |   64   |    0.25 |       4 | gray-box  |
| polyps    | sigmoid |   64   |    0.5  |       1 | gray-box  |
| polyps    | sigmoid |   64   |    0.75 |       1 | gray-box  |
| polyps    | sigmoid |   64   |    2    |       2 | gray-box  |
| polyps    | sigmoid |  128   |    0.5  |       1 | gray-box  |
| polyps    | sigmoid |  128   |    0.75 |       1 | gray-box  |
| polyps    | sigmoid |  128   |    1.25 |       1 | gray-box  |
| polyps    | sigmoid |  256   |    0    |       7 | gray-box  |
| polyps    | sigmoid |  256   |    0.25 |       4 | gray-box  |
| polyps    | sigmoid |  256   |    0.5  |      10 | gray-box  |
| polyps    | sigmoid |  256   |    0.75 |       8 | gray-box  |
| polyps    | sigmoid |  256   |    1    |      10 | gray-box  |
| polyps    | sigmoid |  256   |    1.25 |       5 | gray-box  |
| polyps    | sigmoid |  256   |    1.5  |      11 | gray-box  |
| polyps    | sigmoid |  256   |    1.75 |       9 | gray-box  |
| polyps    | sigmoid |  256   |    2    |      22 | gray-box  |
| polyps    | uniform |    0   |    0    |       4 | gray-box  |
| polyps    | uniform |    0   |    2    |       1 | gray-box  |
| wbc       | edge    |    0.5 |    1.25 |       1 | gray-box  |
| wbc       | edge    |    1   |    1.75 |       1 | gray-box  |
| wbc       | edge    |    8   |    2    |       1 | gray-box  |
| wbc       | region  |    0.5 |    0    |       6 | gray-box  |
| wbc       | region  |    0.5 |    2    |       2 | gray-box  |
| wbc       | region  |    1   |    0.5  |       1 | gray-box  |
| wbc       | region  |    1   |    0.75 |       2 | gray-box  |
| wbc       | region  |    1   |    1.25 |       1 | gray-box  |
| wbc       | region  |    1   |    1.5  |       1 | gray-box  |
| wbc       | region  |    2   |    0.25 |       2 | gray-box  |
| wbc       | region  |    2   |    2    |       1 | gray-box  |
| wbc       | region  |    4   |    1.75 |       1 | gray-box  |
| wbc       | region  |    4   |    2    |       1 | gray-box  |
| wbc       | region  |    8   |    0    |       1 | gray-box  |
| wbc       | region  |    8   |    1.5  |       1 | gray-box  |
| wbc       | region  |    8   |    2    |       1 | gray-box  |
| wbc       | region  |   16   |    0    |       4 | gray-box  |
| wbc       | region  |   16   |    0.75 |       2 | gray-box  |
| wbc       | region  |   16   |    1    |       1 | gray-box  |
| wbc       | region  |   16   |    1.5  |       3 | gray-box  |
| wbc       | region  |   16   |    1.75 |       4 | gray-box  |
| wbc       | region  |   16   |    2    |       5 | gray-box  |
| wbc       | region  |   32   |    0    |       1 | gray-box  |
| wbc       | region  |   32   |    0.25 |       1 | gray-box  |
| wbc       | region  |   32   |    0.5  |       2 | gray-box  |
| wbc       | region  |   32   |    0.75 |       1 | gray-box  |
| wbc       | region  |   32   |    1    |       3 | gray-box  |
| wbc       | region  |   32   |    1.5  |       1 | gray-box  |
| wbc       | region  |   32   |    1.75 |       2 | gray-box  |
| wbc       | region  |   32   |    2    |       6 | gray-box  |
| wbc       | region  |   64   |    0    |       3 | gray-box  |
| wbc       | region  |   64   |    0.25 |       3 | gray-box  |
| wbc       | region  |   64   |    0.5  |       2 | gray-box  |
| wbc       | region  |   64   |    1    |       1 | gray-box  |
| wbc       | region  |   64   |    1.5  |       3 | gray-box  |
| wbc       | region  |   64   |    1.75 |       3 | gray-box  |
| wbc       | region  |   64   |    2    |       5 | gray-box  |
| wbc       | region  |  128   |    0    |       1 | gray-box  |
| wbc       | region  |  128   |    0.25 |       1 | gray-box  |
| wbc       | region  |  128   |    0.5  |       2 | gray-box  |
| wbc       | region  |  128   |    0.75 |       2 | gray-box  |
| wbc       | region  |  128   |    1    |       3 | gray-box  |
| wbc       | region  |  128   |    1.25 |       3 | gray-box  |
| wbc       | region  |  128   |    1.5  |       2 | gray-box  |
| wbc       | region  |  128   |    1.75 |       2 | gray-box  |
| wbc       | region  |  128   |    2    |       6 | gray-box  |
| wbc       | region  |  256   |    0    |      14 | gray-box  |
| wbc       | region  |  256   |    0.25 |       7 | gray-box  |
| wbc       | region  |  256   |    0.5  |       4 | gray-box  |
| wbc       | region  |  256   |    0.75 |       5 | gray-box  |
| wbc       | region  |  256   |    1    |      11 | gray-box  |
| wbc       | region  |  256   |    1.25 |       8 | gray-box  |
| wbc       | region  |  256   |    1.5  |       9 | gray-box  |
| wbc       | region  |  256   |    1.75 |      15 | gray-box  |
| wbc       | region  |  256   |    2    |      29 | gray-box  |
| wbc       | sigmoid |    8   |    0.25 |       1 | gray-box  |
| wbc       | uniform |    0   |    0    |      10 | gray-box  |
| wbc       | uniform |    0   |    1.5  |       1 | gray-box  |