"""Sites representations in sites."""

# Models.
from voronoi_diagrams.models import WeightedSite

# Plot.
from matplotlib import pyplot as plt

# Math
from decimal import Decimal


def create_weighted_site(x: Decimal, y: Decimal, w: Decimal) -> WeightedSite:
    """Get site to work."""
    return WeightedSite(x, y, w)


def plot_point(x: Decimal, y: Decimal) -> None:
    """Plot a Point."""
    plt.plot(x, y, "ro")
