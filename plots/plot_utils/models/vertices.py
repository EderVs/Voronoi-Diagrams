"""Plot Vertices utils."""

# Models.
from voronoi_diagrams.models import VoronoiDiagramVertex

# Plot.
from matplotlib import pyplot as plt

# Plot Models.
from .points import plot_point


def plot_vertex(vertex: VoronoiDiagramVertex):
    """Plot vertex."""
    plot_point(vertex.point.x, vertex.point.y, "b", "o")
