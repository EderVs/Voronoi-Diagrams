"""Vertices in Voronoi Diagram."""

# Standard Library
from typing import List, Any, Optional

# Models
from .points import Point
from .edges import Edge


class Vertex:
    """Vertex representation in the Voronoi diagram."""

    point: Point
    bisectors: List[Edge]

    def __init__(self, point: Point, bisectors: Optional[List[Edge]] = None) -> None:
        """Constructor."""
        self.point = point
        if bisectors is None:
            bisectors = []
        self.bisectors = bisectors

    def __eq__(self, other: "Vertex") -> bool:
        """Equallity between Vertices."""
        return self.point == other.vertex

    def __str__(self) -> str:
        """Return string representation."""
        return f"V({str(self.point)})"

    def __repr__(self) -> str:
        """Return string representation."""
        return self.__str__()

    def add_bisector(self, bisector: Edge) -> List[Edge]:
        """Add bisector adjacent to this vertex."""
        self.bisectors.append(bisector)
        return self.bisectors
