"""Plot WeightedPointBisector using parameters of general conic formula."""

# Standard Library
from math import sqrt

# Models.
from voronoi_diagrams.models import (
    WeightedPointBisector,
    Point,
    WeightedSite,
)

# Plot.
from matplotlib import pyplot as plt
import numpy as np

# Utils.
from plots.plot_utils.models.bisectors import (
    plot_weighted_point_bisector,
    plot_intersections,
)
from plots.plot_utils.models.sites import create_weighted_site, plot_point


def plot_example(
    x1: float,
    y1: float,
    w1: float,
    x2: float,
    y2: float,
    w2: float,
    x3: float,
    y3: float,
    w3: float,
) -> None:
    """Plot example of 2 bisectors and its intersections."""
    p1 = create_weighted_site(x1, y1, w1)
    p2 = create_weighted_site(x2, y2, w2)
    p3 = create_weighted_site(x3, y3, w3)
    p1_p2_bisector = WeightedPointBisector(sites=(p1, p2))
    p2_p3_bisector = WeightedPointBisector(sites=(p2, p3))

    x_range = np.arange(-30.0, 30.0, 0.1)
    ylim = (-30, 30)
    xlim = (-30, 30)

    plt.figure()
    plt.subplot(211)

    plot_weighted_point_bisector(p1_p2_bisector, x_range)
    plot_weighted_point_bisector(p2_p3_bisector, x_range)

    plot_intersections(p1_p2_bisector, p2_p3_bisector)

    plt.xlim(*xlim)
    plt.ylim(*ylim)
    plt.show()


# Example 1
x1: float = 3
y1: float = -4
w1: float = 2
x2: float = 3
y2: float = 1
w2: float = 1
x3: float = 0.5
y3: float = -1
w3: float = 1.5
plot_example(
    x1, y1, w1, x2, y2, w2, x3, y3, w3,
)
# Example 2
x1 = -3.5
y1 = 0
w1 = 2
x2 = 0
y2 = -2.5
w2 = 1
x3 = 0
y3 = 2
w3 = 1.5
plot_example(
    x1, y1, w1, x2, y2, w2, x3, y3, w3,
)
# Example 3
x1 = -3
y1 = 1
w1 = 2 * sqrt(2)
x2 = 6
y2 = 10
w2 = sqrt(2)
x3 = -4
y3 = 0
w3 = 3 * sqrt(2)
plot_example(
    x1, y1, w1, x2, y2, w2, x3, y3, w3,
)
# Example 4
x1 = 7
y1 = 1
w1 = 2 * sqrt(2)
x2 = 6
y2 = 10
w2 = sqrt(2)
x3 = -4
y3 = 0
w3 = 3 * sqrt(2)
plot_example(
    x1, y1, w1, x2, y2, w2, x3, y3, w3,
)
# Example 5
x1 = 7.1
y1 = -2.2
w1 = 2 * sqrt(2)
x2 = 6
y2 = 10
w2 = sqrt(2)
x3 = 5.9
y3 = 16.44
w3 = 3 * sqrt(2)
plot_example(
    x1, y1, w1, x2, y2, w2, x3, y3, w3,
)
