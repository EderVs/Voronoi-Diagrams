"""Sites representations in plot."""

from typing import Iterable

# Models.
from voronoi_diagrams.models import Site, WeightedSite

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
