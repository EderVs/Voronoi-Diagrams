"""Bisectors representations in plots."""
# Standard Library.
from typing import Iterable, Tuple, Optional, Any, List, Type

# Models.
from voronoi_diagrams.models import (
    Bisector,
    PointBisector,
    WeightedPointBisector,
    VoronoiDiagramBisector,
)

# Utils.
from .events import create_weighted_site, is_equal_limit_site, SiteToUse
from .vertices import plot_vertex
from .points import plot_point

# Plot.
# from matplotlib import pyplot as plt
from plotly import graph_objects as go
import numpy as np

# Math
from decimal import Decimal

Limit = Tuple[Decimal, Decimal]


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
    vd_bisector: VoronoiDiagramBisector,
    xlim,
    ylim,
    bisector_class: Any = PointBisector,
) -> List[go.Scatter]:
    """Plot Bisector in a Voronoi Diagram.

    This bisector has 2 vertices.
    """
    x_range, y_range = vd_bisector.get_ranges(xlim, ylim)
    return plot_bisector(
        vd_bisector.bisector,
        xlim,
        ylim,
        x_range=x_range,
        y_range=y_range,
        bisector_class=bisector_class,
    )


def plot_bisector(
    bisector: Bisector,
    xlim: Tuple[Decimal, Decimal],
    ylim: Tuple[Decimal, Decimal],
    x_range: Optional[Iterable] = None,
    y_range: Optional[Iterable] = None,
    bisector_class: Any = PointBisector,
) -> List[go.Scatter]:
    """Plot a WeightedPointBisector.

    x_range: values of xs that will be plotted.
    """
    traces = []
    if x_range is None and y_range is None:
        # error
        return

    if bisector_class == PointBisector:
        num_lists = 1
    elif bisector_class == WeightedPointBisector:
        num_lists = 2
    else:
        return

    if y_range is None:
        y_lists = [[] for _ in range(num_lists)]
        for x in x_range:
            if x < xlim[0] or x > xlim[1]:
                for i in range(num_lists):
                    y_lists[i].append(None)
                continue
            ys = bisector.formula_y(x)
            num_y = len(ys)
            for i in range(num_y):
                if ys[i] >= ylim[0] and ys[i] <= ylim[1]:
                    y_lists[i].append(ys[i])
                else:
                    y_lists[i].append(None)
            for i in range(num_y, num_lists):
                y_lists[i].append(None)

        for i in range(num_lists):
            traces.append(
                go.Scatter(
                    x=x_range,
                    y=y_lists[i],
                    mode="lines",
                    name=bisector.small_str(),
                    connectgaps=True,
                    legendgroup="bisectors",
                    hoverinfo="name",
                )
            )
            # plt.plot(x_range, y_lists[i], "k")
    elif x_range is None:
        x_lists = [[] for _ in range(num_lists)]
        for y in y_range:
            if y < ylim[0] or y > ylim[1]:
                for i in range(num_lists):
                    x_lists[i].append(None)
                continue
            xs = bisector.formula_x(y)
            num_x = len(xs)
            for i in range(num_x):
                if xs[i] >= xlim[0] and xs[i] <= xlim[1]:
                    x_lists[i].append(xs[i])
                else:
                    x_lists[i].append(None)
            for i in range(num_x, num_lists):
                x_lists[i].append(None)

        for i in range(num_lists):
            traces.append(
                go.Scatter(
                    x=x_lists[i],
                    y=y_range,
                    name=bisector.small_str(),
                    mode="lines",
                    connectgaps=True,
                    legendgroup="bisectors",
                    hoverinfo="name",
                )
            )
            # plt.plot(x_lists[i], y_range, "k")
    else:
        traces.append(
            go.Scatter(
                x=x_range,
                y=y_range,
                mode="lines",
                name=bisector.small_str(),
                connectgaps=True,
                legendgroup="bisectors",
                hoverinfo="name",
            )
        )
    return traces


def plot_intersections(
    figure: go.Figure,
    bisector1: WeightedPointBisector,
    bisector2: WeightedPointBisector,
) -> None:
    """Plot intersections between 2 bisectors."""
    intersections = bisector1.get_intersections(bisector2)
    for intersection in intersections:
        trace = plot_point(intersection[0], intersection[1][0])
        figure.add_trace(trace)


def is_a_limit_bisector(
    vd_bisector: VoronoiDiagramBisector,
    limit_sites: List[SiteToUse],
    bisector_class: Type[Bisector],
) -> None:
    """Check if current bisector is a bisector with a limit site."""
    for site in vd_bisector.bisector.get_sites_tuple():
        for limit_site in limit_sites:
            if is_equal_limit_site(site, limit_site, bisector_class=bisector_class):
                return True
    return False


def plot_vertices_and_bisectors(
    bisectors: List[VoronoiDiagramBisector],
    limit_sites: List[SiteToUse],
    xlim: Limit,
    ylim: Limit,
    bisector_class: Type[Bisector],
) -> List[go.Scatter]:
    """Plot bisectors in diagram."""
    vertices_passed = set()
    traces = []
    for vd_bisector in bisectors:
        # For debuging.
        # print("//////////////////////////////////////////////////")
        # print(vd_bisector)  # Debugging
        # print("-", vd_bisector.ranges_b_minus)
        # print("+", vd_bisector.ranges_b_plus)
        # print("|", vd_bisector.ranges_vertical)
        if not is_a_limit_bisector(
            vd_bisector, limit_sites, bisector_class=bisector_class
        ):
            for bisector_vertex in vd_bisector.vertices:
                if id(bisector_vertex) in vertices_passed:
                    continue
                vertices_passed.add(id(bisector_vertex))
                traces.append(plot_vertex(bisector_vertex))
            traces += plot_voronoi_diagram_bisector(
                vd_bisector, xlim=xlim, ylim=ylim, bisector_class=bisector_class,
            )

        # For debuging.
        # print("-", vd_bisector.ranges_b_minus)
        # print("+", vd_bisector.ranges_b_plus)
        # print("|", vd_bisector.ranges_vertical)
    return traces
