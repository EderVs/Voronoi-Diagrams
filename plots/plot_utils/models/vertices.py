"""Plot Vertices utils."""

# Models.
from voronoi_diagrams.models import Vertex

# Plot Models.
from .points import plot_point


def plot_vertex(vertex: Vertex):
    """Plot vertex."""
    return plot_point(
        vertex.point.x,
        vertex.point.y,
        name=str(vertex),
        symbol="star-dot",
        size=10,
        group="vertices",
    )
