"""Bisectors representations in plots."""
# Standard Library.
from typing import Iterable, Tuple, Optional, Any

# Models.
from voronoi_diagrams.models import (
    Bisector,
    PointBisector,
    WeightedPointBisector,
    VoronoiDiagramBisector,
)

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


def is_plot_in_x(
    vd_bisector: VoronoiDiagramBisector, bisector_class: Any = PointBisector
) -> bool:
    """Get if we are going to use formula_x or formula_y to plot.

    Check depending on the sites of the bisector.
    """
    if bisector_class == PointBisector:
        return True
    elif bisector_class == WeightedPointBisector:
        bisector: Bisector = vd_bisector.bisector
        sites = bisector.get_sites_tuple()
        return sites[0].get_lowest_site_point().y >= sites[1].get_lowest_site_point().y


def plot_voronoi_diagram_bisector(
    vd_bisector: VoronoiDiagramBisector, xlim, ylim, bisector_class: Any = PointBisector
):
    """Plot Bisector in a Voronoi Diagram.

    This bisector has 2 vertices.
    """
    vertices = vd_bisector.vertices
    if is_plot_in_x(vd_bisector, bisector_class=bisector_class):
        if len(vd_bisector.vertices) == 0:
            x_range = np.arange(Decimal(xlim[0]), xlim[1], Decimal("0.01"))
            plot_bisector(
                vd_bisector.bisector, x_range=x_range, bisector_class=bisector_class
            )
        elif len(vd_bisector.vertices) == 1:
            vertex = vd_bisector.vertices[0]
            x_range = np.arange(Decimal(xlim[0]), vertex.point.x, Decimal("0.01"))
            plot_bisector(
                vd_bisector.bisector, x_range=x_range, bisector_class=bisector_class
            )
            x_range = np.arange(vertex.point.x, Decimal(xlim[1]), Decimal("0.01"))
            plot_bisector(
                vd_bisector.bisector, x_range=x_range, bisector_class=bisector_class
            )
        else:
            bisector_vertices_x = [vertex.point.x for vertex in vertices]
            x_range = np.arange(
                min(bisector_vertices_x), max(bisector_vertices_x), Decimal("0.01")
            )
            plot_bisector(
                vd_bisector.bisector, x_range=x_range, bisector_class=bisector_class
            )
    else:
        if len(vd_bisector.vertices) == 0:
            y_range = np.arange(Decimal(ylim[0]), ylim[1], Decimal("0.01"))
            plot_bisector(
                vd_bisector.bisector, y_range=y_range, bisector_class=bisector_class
            )
        elif len(vd_bisector.vertices) == 1:
            vertex = vd_bisector.vertices[0]
            y_range = np.arange(Decimal(ylim[0]), vertex.point.y, Decimal("0.01"))
            plot_bisector(
                vd_bisector.bisector, y_range=y_range, bisector_class=bisector_class
            )
            y_range = np.arange(vertex.point.y, Decimal(ylim[1]), Decimal("0.01"))
            plot_bisector(
                vd_bisector.bisector, y_range=y_range, bisector_class=bisector_class
            )
        else:
            bisector_vertices_y = [vertex.point.y for vertex in vertices]
            y_range = np.arange(
                min(bisector_vertices_y), max(bisector_vertices_y), Decimal("0.01")
            )
            plot_bisector(
                vd_bisector.bisector, y_range=y_range, bisector_class=bisector_class
            )


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
            xs = bisector.formula_x(y)
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
