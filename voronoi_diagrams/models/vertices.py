"""Vertices in Voronoi Diagram."""

# Standard Library
from typing import List, Any, Optional

# Models
from .points import Point
from .voronoi_diagram_bisectors import VoronoiDiagramBisector


class VoronoiDiagramVertex:
    """Vertex representation in the Voronoi diagram."""

    point: Point
    bisectors: List[VoronoiDiagramBisector]

    def __init__(
        self, vertex: Point, bisectors: Optional[List[VoronoiDiagramBisector]] = None
    ) -> None:
        """Constructor."""
        self.point = vertex
        if bisectors is None:
            bisectors = []
        self.bisectors = bisectors

    def __eq__(self, other: Any) -> bool:
        """Equallity between VoronoiDiagramBisectors."""
        return self.point == other.vertex

    def __str__(self) -> str:
        """Return string representation."""
        return f"V({str(self.point)})"

    def __repr__(self) -> str:
        """Return string representation."""
        return self.__str__()

    def add_bisector(
        self, bisector: VoronoiDiagramBisector
    ) -> List[VoronoiDiagramBisector]:
        """Add bisector adjacent to this vertex."""
        self.bisectors.append(bisector)
        return self.bisectors
