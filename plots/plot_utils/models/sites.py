"""Sites representations in plot."""

# Models.
from voronoi_diagrams.models import Site, WeightedSite

# Plot.
from matplotlib import pyplot as plt

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


def plot_site(site: Site, site_class=Site):
    """Plot site."""
    if site_class == WeightedSite:
        plot_circle(site.point.x, site.point.y, site.weight)
    plot_point(site.point.x, site.point.y)
