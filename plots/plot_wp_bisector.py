"""Plot WeightedPointBisector using parameters of general conic formula."""

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

# Math
from decimal import Decimal


def plot_example(
    x1: Decimal,
    y1: Decimal,
    w1: Decimal,
    x2: Decimal,
    y2: Decimal,
    w2: Decimal,
    x3: Decimal,
    y3: Decimal,
    w3: Decimal,
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
x1: Decimal = Decimal(3)
y1: Decimal = Decimal(-4)
w1: Decimal = Decimal(2)
x2: Decimal = Decimal(3)
y2: Decimal = Decimal(1)
w2: Decimal = Decimal(1)
x3: Decimal = Decimal(0.5)
y3: Decimal = Decimal(-1)
w3: Decimal = Decimal(1.5)
plot_example(
    x1, y1, w1, x2, y2, w2, x3, y3, w3,
)
# Example 2
x1 = Decimal(-3.5)
y1 = Decimal(0)
w1 = Decimal(2)
x2 = Decimal(0)
y2 = Decimal(-2.5)
w2 = Decimal(1)
x3 = Decimal(0)
y3 = Decimal(2)
w3 = Decimal(1.5)
plot_example(
    x1, y1, w1, x2, y2, w2, x3, y3, w3,
)
# Example 3
x1 = Decimal(-3)
y1 = Decimal(1)
w1 = Decimal(2) * Decimal(2).sqrt()
x2 = Decimal(6)
y2 = Decimal(10)
w2 = Decimal(2).sqrt()
x3 = Decimal(-4)
y3 = Decimal(0)
w3 = Decimal(3) * Decimal(2).sqrt()
plot_example(
    x1, y1, w1, x2, y2, w2, x3, y3, w3,
)
# Example 4
x1 = Decimal(7)
y1 = Decimal(1)
w1 = Decimal(2) * Decimal(2).sqrt()
x2 = Decimal(6)
y2 = Decimal(10)
w2 = Decimal(2).sqrt()
x3 = Decimal(-4)
y3 = Decimal(0)
w3 = Decimal(3) * Decimal(2).sqrt()
plot_example(
    x1, y1, w1, x2, y2, w2, x3, y3, w3,
)
# Example 5
x1 = Decimal(7.1)
y1 = Decimal(-2.2)
w1 = Decimal(2) * Decimal(2).sqrt()
x2 = Decimal(6)
y2 = Decimal(10)
w2 = Decimal(2).sqrt()
x3 = Decimal(5.9)
y3 = Decimal(16.44)
w3 = Decimal(3) * Decimal(2).sqrt()
plot_example(
    x1, y1, w1, x2, y2, w2, x3, y3, w3,
)
