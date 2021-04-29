"""Sites representations in plot."""

from typing import Iterable, Union, Tuple, Type
from random import randint

# Models.
from voronoi_diagrams.models import Site, WeightedSite, Event, Point
from voronoi_diagrams.data_structures.q import QStructure

# Plot.
from plotly import graph_objects as go

# Numpy.
import numpy as np

# Math
from decimal import Decimal

# Plot Models.
from .points import get_point_trace

# Conic sections.
from .conic_sections import get_circle_ranges


SiteToUse = Union[Point, Tuple[Point, Decimal]]


def create_weighted_site(x: Decimal, y: Decimal, w: Decimal) -> WeightedSite:
    """Get site to work."""
    return WeightedSite(x, y, w)


def get_site_traces(site: Site, site_class=Site):
    """Get site traces."""
    color = f"rgb({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})"
    traces = []
    traces.append(
        get_point_trace(
            site.point.x,
            site.point.y,
            name=f"{site.get_display_str()}",
            color=color,
            group="sites",
        )
    )
    if site_class == WeightedSite and site.weight > 0:
        x_range, y_range = get_circle_ranges(
            site.point.x, site.point.y, site.weight, "r"
        )
        line_properties = {"width": 1, "color": color}
        traces.append(
            go.Scatter(
                x=x_range,
                y=y_range,
                mode="lines",
                name=f"{str(site.name)} weight: {'{0:.4f}'.format(site.weight)}",
                line=line_properties,
                connectgaps=True,
                legendgroup="sites",
                hoverinfo="name",
            )
        )
    return traces


def plot_site(figure: go.Figure, site: Site, site_class=Site):
    """Plot site."""
    for trace in get_site_traces(site, site_class):
        figure.add_trace(trace)


def plot_sites(figure: go.Figure, sites: Iterable[Site], site_class=Site):
    """Plot collection of sites."""
    for site in sites:
        plot_site(figure, site, site_class)


def plot_sweep_line(figure: go.Figure, xlim, ylim, event: Event):
    """Plot event sweep line."""
    y = event.get_event_point().y
    if y < ylim[0] or y > ylim[1]:
        return
    step = Decimal("1")
    x_range = np.arange(xlim[0], xlim[1], step)
    y_range = [y for _ in x_range]
    line_properties = {"width": 3.5, "dash": "dash"}
    figure.add_trace(
        go.Scatter(
            x=x_range,
            y=y_range,
            mode="lines",
            name="Sweep line",
            line=line_properties,
            legendgroup="sweepline",
        )
    )


def is_equal_limit_site(
    site: SiteToUse, limit_site: SiteToUse, site_class: Type[Site]
) -> None:
    """Check if site is a limit site."""
    if site_class == Site:
        return site.point.x == limit_site.x and site.point.y == limit_site.y
    elif site_class == WeightedSite:
        return (
            site.point.x == limit_site[0].x
            and site.point.y == limit_site[0].y
            and site.weight == limit_site[1]
        )


def plot_events_traces(figure: go.Figure, q_queue: QStructure):
    """Get events traces."""
    for event in q_queue.get_all_events():
        color = f"rgb({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})"
        figure.add_trace(
            get_point_trace(
                event.get_event_point().x,
                event.get_event_point().y,
                name=f"{event.get_event_str()}",
                color=color,
                symbol="diamond",
                size=8,
                group="events",
            )
        )
