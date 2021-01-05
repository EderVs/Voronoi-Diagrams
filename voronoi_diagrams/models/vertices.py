"""Vertices in Voronoi Diagram."""

# Standard Library
from typing import List, Any, Optional

# Models
from .points import Point
from .edges import Edge


class Vertex:
    """Vertex representation in the Voronoi diagram."""

    point: Point
    edges: List[Edge]

    def __init__(self, point: Point, edges: Optional[List[Edge]] = None) -> None:
        """Constructor."""
        self.point = point
        if edges is None:
            edges = []
        self.edges = edges

    def __eq__(self, other: "Vertex") -> bool:
        """Equallity between Vertices."""
        return self.point == other.vertex

    def __str__(self) -> str:
        """Return string representation."""
        return f"V({str(self.point)})"

    def __repr__(self) -> str:
        """Return string representation."""
        return self.__str__()

    def add_edge(self, edge: Edge) -> List[Edge]:
        """Add bisector adjacent to this vertex."""
        self.edges.append(edge)
        return self.edges
