"""Sites representations in plot."""

from typing import Iterable

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
from .conic_sections import plot_circle


def create_weighted_site(x: Decimal, y: Decimal, w: Decimal) -> WeightedSite:
    """Get site to work."""
    return WeightedSite(x, y, w)


def plot_site(figure: go.Figure, site: Site, site_class=Site):
    """Plot site."""
    if site_class == WeightedSite:
        plot_circle(figure, site.point.x, site.point.y, site.weight, "r")
    plot_point(figure, site.point.x, site.point.y, "r", ".")


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
    figure.add_trace(go.Scatter(x=x_range, y=y_range, mode="lines", name="Sweep line"))
