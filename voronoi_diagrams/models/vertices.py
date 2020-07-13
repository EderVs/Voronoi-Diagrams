"""Vertices in Voronoi Diagram."""

# Standard Library
from typing import List, Any, Optional

# Models
from .points import Point
from .bisectors import VoronoiDiagramBisector


class VoronoiDiagramVertex:
    """Vertex representation in the Voronoi diagram."""

    vertex: Point
    bisectors: List[VoronoiDiagramBisector]

    def __init__(
        self, vertex: Point, bisectors: Optional[List[VoronoiDiagramBisector]] = None
    ) -> None:
        """Constructor."""
        self.vertex = vertex
        if bisectors is None:
            bisectors = []
        self.bisectors = bisectors

    def __eq__(self, other: Any) -> bool:
        """Equallity between VoronoiDiagramBisectors."""
        return self.vertex == other.vertex

    def add_bisector(
        self, bisector: VoronoiDiagramBisector
    ) -> List[VoronoiDiagramBisector]:
        """Add bisector adjacent to this vertex."""
        self.bisectors.append(bisector)
        return self.bisectors
