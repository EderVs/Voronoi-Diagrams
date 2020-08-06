"""Sites representations in plot."""

from typing import Iterable
from random import randint

# Models.
from voronoi_diagrams.models import Site, WeightedSite, Event

# Plot.
from plotly import graph_objects as go

# Numpy.
import numpy as np

# Math
from decimal import Decimal

# Plot Models.
from .points import plot_point

# Conic sections.
from .conic_sections import get_circle_ranges


def create_weighted_site(x: Decimal, y: Decimal, w: Decimal) -> WeightedSite:
    """Get site to work."""
    return WeightedSite(x, y, w)


def plot_site(figure: go.Figure, site: Site, site_class=Site):
    """Plot site."""
    color = f"rgb({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})"
    if site_class == WeightedSite:
        x_range, y_range = get_circle_ranges(
            site.point.x, site.point.y, site.weight, "r"
        )
        line_properties = {"width": 2.5, "color": color}
        figure.add_trace(
            go.Scatter(
                x=x_range,
                y=y_range,
                mode="lines",
                name=f"Weight {str(site)}",
                line=line_properties,
            )
        )
    plot_point(figure, site.point.x, site.point.y, name=f"{str(site)}", color=color)


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
    line_properties = {"width": 3.5}
    figure.add_trace(
        go.Scatter(
            x=x_range, y=y_range, mode="lines", name="Sweep line", line=line_properties
        )
    )
