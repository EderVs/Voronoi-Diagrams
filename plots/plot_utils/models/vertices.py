"""Plot Vertices utils."""

# Models.
from voronoi_diagrams.models import VoronoiDiagramVertex

# Plot.
from plotly import graph_objects as go

# Plot Models.
from .points import plot_point


def plot_vertex(vertex: VoronoiDiagramVertex):
    """Plot vertex."""
    return plot_point(
        vertex.point.x, vertex.point.y, name=str(vertex), symbol="star-dot", size=10,
    )
