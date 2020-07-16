"""Bisectors representations in plots."""
# Standard Library.
from typing import Iterable, Tuple, Optional, Any

# Models.
from voronoi_diagrams.models import Bisector, PointBisector, WeightedPointBisector

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


def plot_bisector(
    bisector: Bisector,
    x_range: Optional[Iterable] = None,
    y_range: Optional[Iterable] = None,
    bisector_class: Any = PointBisector,
) -> None:
    """Plot a WeightedPointBisector.

    x_range: values of xs that will be plotted.
    """
    if x_range is not None and y_range is not None:
        # error
        return

    if bisector_class == PointBisector:
        num_lists = 1
    elif bisector_class == WeightedPointBisector:
        num_lists = 2
    else:
        return

    if x_range is not None:
        y_lists = [[] for _ in range(num_lists)]
        for x in x_range:
            ys = bisector.formula_y(x)
            num_y = len(ys)
            for i in range(num_y):
                y_lists[i].append(ys[i])
            for i in range(num_y, num_lists):
                y_lists[i].append(None)

        for i in range(num_lists):
            plt.plot(x_range, y_lists[i], "k")
    else:
        x_lists = [[] for _ in range(num_lists)]
        for y in y_range:
            xs = bisector.formula_y(y)
            num_x = len(xs)
            for i in range(num_x):
                x_lists[i].append(xs[i])
            for i in range(num_x, num_lists):
                x_lists[i].append(None)

        for i in range(num_lists):
            plt.plot(x_lists[i], y_range, "k")


def plot_intersections(
    bisector1: WeightedPointBisector, bisector2: WeightedPointBisector
) -> None:
    """Plot intersections between 2 bisectors."""
    intersections = bisector1.get_intersection_points(bisector2)
    for intersection in intersections:
        plot_point(intersection[0], intersection[1][0])
