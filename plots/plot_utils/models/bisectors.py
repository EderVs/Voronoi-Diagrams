"""Bisectors representations in plots."""
# Standard Library.
from typing import Iterable, Tuple

# Models.
from voronoi_diagrams.models import WeightedPointBisector

# Utils.
from .sites import create_weighted_site, plot_point

# Plot.
from matplotlib import pyplot as plt
import numpy as np

# Math
from decimal import Decimal


def create_weighted_point_bisector(
    x1: Decimal, y1: Decimal, w1: Decimal, x2: Decimal, y2: Decimal, w2: Decimal
) -> WeightedPointBisector:
    """Get bisector to work."""
    p = create_weighted_site(x1, y1, w1)
    q = create_weighted_site(x2, y2, w2)
    return WeightedPointBisector(sites=(p, q))


def plot_weighted_point_bisector(
    bisector: WeightedPointBisector, x_range: Iterable,
) -> None:
    """Plot a WeightedPointBisector.

    x_range: values of xs that will be plotted.
    xlim: Limits of x in the plot.
    ylim: Limits of y in the plot.
    """
    y_list_plus = [bisector.formula_y(x)[0] for x in x_range]
    y_list_minus = [bisector.formula_y(x)(1) for x in x_range]
    plt.plot(x_range, y_list_plus, "k")
    plt.plot(x_range, y_list_minus, "k")


def plot_intersections(
    bisector1: WeightedPointBisector, bisector2: WeightedPointBisector
) -> None:
    """Plot intersections between 2 bisectors."""
    intersections = bisector1.get_intersection_points(bisector2)
    for intersection in intersections:
        plot_point(intersection[0], intersection[1][0])
