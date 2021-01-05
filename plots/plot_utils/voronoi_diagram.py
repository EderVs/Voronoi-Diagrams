"""Voronoi Diagram representation in plot"""

# Standard Library.
from typing import Tuple, List, Type, Union
from decimal import Decimal

# Voronoi diagrams.
from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm
from voronoi_diagrams.models import (
    Site,
    WeightedSite,
    PointBisector,
    WeightedPointBisector,
    Point,
)

# Plot.
# from matplotlib import pyplot as plt
from plotly import graph_objects as go
from plots.plot_utils.models.bisectors import plot_vertices_and_edges
from plots.plot_utils.models.events import plot_site, is_equal_limit_site


SiteToUse = Union[Point, Tuple[Point, Decimal]]
Limit = Tuple[Decimal, Decimal]


def get_vd_figure(
    voronoi_diagram: FortunesAlgorithm,
    limit_sites: List[SiteToUse],
    xlim: Limit,
    ylim: Limit,
    site_class: Type[Site] = Site,
) -> go.Figure:
    """Get figure of voronoi diagram."""
    figure = go.Figure()
    layout = go.Layout(
        height=745,
        width=815,
        hovermode="closest",
        legend={"itemclick": "toggleothers", "itemdoubleclick": "toggle"},
    )
    template = dict(layout=layout)
    figure.update_layout(title="VD", template=template)
    figure.update_xaxes(range=list(xlim))
    figure.update_yaxes(range=list(ylim), scaleanchor="x", scaleratio=1)

    bisector_class = PointBisector
    if site_class == WeightedSite:
        bisector_class = WeightedPointBisector

    # Sites.
    for site in voronoi_diagram.sites:
        for limit_site in limit_sites:
            if is_equal_limit_site(site, limit_site, site_class=site_class):
                break
        else:
            plot_site(figure, site, site_class)

    # Diagram.
    traces = plot_vertices_and_edges(
        voronoi_diagram.edges, limit_sites, xlim, ylim, bisector_class=bisector_class,
    )
    for trace in traces:
        figure.add_trace(trace)

    return figure


def get_html(figure: go.Figure):
    """Get html of the Figure."""
    config = {
        "modeBarButtonsToRemove": ["toggleSpikelines", "hoverCompareCartesian"],
        "modeBarButtonsToAdd": ["drawopenpath", "drawclosedpath", "eraseshape"],
    }
    return figure.to_html(config=config)


def get_vd_html(
    voronoi_diagram: FortunesAlgorithm,
    limit_sites: List[SiteToUse],
    xlim: Limit,
    ylim: Limit,
) -> None:
    """Plot voronoi diagram."""
    figure = get_vd_figure(
        voronoi_diagram, limit_sites, xlim, ylim, voronoi_diagram.SITE_CLASS
    )
    html = get_html(figure)
    return html


def plot_voronoi_diagram(
    voronoi_diagram: FortunesAlgorithm,
    limit_sites: List[SiteToUse],
    xlim: Limit,
    ylim: Limit,
    site_class: Type[Site] = Site,
) -> None:
    """Plot voronoi diagram."""
    figure = get_vd_figure(voronoi_diagram, limit_sites, xlim, ylim, site_class)
    figure.show()
