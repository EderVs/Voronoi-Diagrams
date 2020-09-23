"""Voronoi Diagram representation in plot"""

# Standard Library.
from typing import Any, Tuple, List, Type, Union
from decimal import Decimal

# Voronoi diagrams.
from voronoi_diagrams.fortunes_algorithm import VoronoiDiagram
from voronoi_diagrams.models import (
    Site,
    WeightedSite,
    Bisector,
    PointBisector,
    WeightedPointBisector,
    VoronoiDiagramBisector,
    VoronoiDiagramVertex,
    Point,
)

# Plot.
# from matplotlib import pyplot as plt
from plotly import graph_objects as go
import plotly.offline as py
import numpy as np
from plots.plot_utils.models.bisectors import plot_bisector, plot_vertices_and_bisectors
from plots.plot_utils.models.events import plot_site, is_equal_limit_site
from plots.plot_utils.models.vertices import plot_vertex


SiteToUse = Union[Point, Tuple[Point, Decimal]]
Limit = Tuple[Decimal, Decimal]


def get_vd_figure(
    voronoi_diagram: VoronoiDiagram,
    limit_sites: List[SiteToUse],
    xlim: Limit,
    ylim: Limit,
    site_class: Type[Site] = Site,
) -> go.Figure:
    """Get figure of voronoi diagram."""
    figure = go.Figure()
    layout = go.Layout(height=745, width=815,)
    template = dict(layout=layout)
    figure.update_layout(title="VD", template=template)
    figure.update_xaxes(range=list(xlim))
    figure.update_yaxes(range=list(ylim), scaleanchor="x", scaleratio=1)
    # plt.figure(figsize=(12, 10))
    # plt.gca().set_aspect("equal", adjustable="box")

    if site_class == Site:
        bisector_class = PointBisector
    elif site_class == WeightedSite:
        bisector_class = WeightedPointBisector

    # Sites.
    for site in voronoi_diagram.sites:
        for limit_site in limit_sites:
            if is_equal_limit_site(site, limit_site, site_class=site_class):
                break
        else:
            plot_site(figure, site, site_class)

    # Diagram.
    traces = plot_vertices_and_bisectors(
        voronoi_diagram.bisectors,
        limit_sites,
        xlim,
        ylim,
        bisector_class=bisector_class,
    )
    for trace in traces:
        figure.add_trace(trace)

    # plt.xlim(*xlim)
    # plt.ylim(*ylim)
    # plt.show()
    return figure


def get_vd_html(
    voronoi_diagram: VoronoiDiagram,
    limit_sites: List[SiteToUse],
    xlim: Limit,
    ylim: Limit,
) -> None:
    """Plot voronoi diagram."""
    figure = get_vd_figure(
        voronoi_diagram, limit_sites, xlim, ylim, voronoi_diagram.SITE_CLASS
    )
    html = figure.to_html()
    return html


def plot_voronoi_diagram(
    voronoi_diagram: VoronoiDiagram,
    limit_sites: List[SiteToUse],
    xlim: Limit,
    ylim: Limit,
    site_class: Type[Site] = Site,
) -> None:
    """Plot voronoi diagram."""
    figure = get_vd_figure(voronoi_diagram, limit_sites, xlim, ylim, site_class)
    figure.show()
