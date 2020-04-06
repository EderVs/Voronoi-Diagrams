"""Fortune's Algorithm to calculate Voronoi Diagrams.

General Solution.
"""
# Standard Library
from typing import Iterable, List, Any

# Data structures
from data_structures import LList, QQueue

# Models
from data_structures.models import (
    Site,
    Point,
    Bisector,
    Event,
    Intersection,
    PointBisector,
    PointBoundary,
    PointRegion,
)


class VoronoiDiagram:
    """Voronoi Diagram representation."""

    vertex: List[Point] = []
    bisectors: List[Bisector] = []
    sites: List[Site] = []

    def add_vertex(self, point: Point) -> None:
        """Add point in the vertex list."""
        self.vertex.append(point)

    def add_bisector(self, bisector: Bisector) -> None:
        """Add point in the vertex list."""
        self.bisectors.append(Bisector)


class FortunesAlgorithm:
    """Fortune's Algorithm implementation."""

    @classmethod
    def calculate_voronoi_diagram(
        sites: Iterable[Point], site_class: Any = Site
    ) -> VoronoiDiagram:
        """Calculate Voronoi Diagram."""
        if site_class == Site:
            BISECTOR_CLASS = PointBisector
            REGION_CLASS = PointRegion
            BOUNDARY_CLASS = PointBoundary

        # Step 1.
        q_queue = QQueue()
        for site in sites:
            q_queue.enqueue(site)

        # Step 2.
        p = q_queue.dequeue()

        # Step 3.
        r_p = REGION_CLASS(p, None, None)
        l_list = LList(r_p)

        return VoronoiDiagram()
