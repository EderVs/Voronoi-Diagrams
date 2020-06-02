"""Sites representations in sites."""

# Models.
from voronoi_diagrams.models import WeightedSite

# Plot.
from matplotlib import pyplot as plt


def create_weighted_site(x: float, y: float, w: float) -> WeightedSite:
    """Get site to work."""
    return WeightedSite(x, y, w)


def plot_point(x: float, y: float) -> None:
    """Plot a Point."""
    plt.plot(x, y, "ro")
