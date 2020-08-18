"""Bisectors Representations in the Voronoi Diagram."""

from typing import Tuple, Any, Optional, List
from decimal import Decimal

# Models
from .bisectors import Bisector, PointBisector, WeightedPointBisector
from .boundaries import Boundary, PointBoundary, WeightedPointBoundary

# Ranges
# Bisector side is set to be an int if there is other sides when using other type of sites.
BisectorSide = int
# Each range must have the same Bisector Side.
Range = Tuple[Optional[Decimal], Optional[Decimal], BisectorSide]


class VoronoiDiagramBisector:
    """Bisector representation in the Voronoi diagram."""

    bisector: Bisector
    vertices: List[Any]
    ranges_b_plus: List[Range]
    ranges_b_minus: List[Range]
    boundary_plus: Boundary
    boundary_minus: Boundary

    def __init__(
        self,
        bisector: Any,
        boundary_plus: Boundary,
        boundary_minus: Boundary,
        vertex1: Any = None,
        vertex2: Any = None,
    ) -> None:
        """Constructor."""
        self.bisector = bisector
        self.vertices = []
        if vertex1 is not None:
            self.vertices.append(vertex1)
        if vertex2 is not None:
            self.vertices.append(vertex2)
        self.ranges_b_plus = []
        self.ranges_b_minus = []
        self.boundary_plus = boundary_plus
        self.boundary_minus = boundary_minus

    def __eq__(self, other: Any) -> bool:
        """Equallity between VoronoiDiagramBisectors."""
        return self.bisector == other.bisector and (
            (self.vertex1 == other.vertex1 and self.vertex2 == other.vertex2)
            or (self.vertex1 == other.vertex2 and self.vertex2 == other.vertex1)
        )

    def __str__(self) -> str:
        """Return string representation."""
        return f"B({str(self.bisector)}, {str(self.vertices)})"

    def is_to_the_infinity(self) -> bool:
        """Check if the bisector doesn't have one vertex."""
        return len(self.vertices) != 2

    def get_vertices(self) -> Tuple[Any, Any]:
        """Get vertices linked to this bisector."""
        if len(self.vertices) == 0:
            vertex1 = None
            vertex2 = None
        elif len(self.vertices) == 1:
            vertex1 = self.vertices[0]
            vertex2 = None
        else:
            if self.vertices[0].vertex.y > self.vertices[1].vertex.y or (
                self.vertices[0].vertex.y == self.vertices[1].vertex.y
                and self.vertices[0].vertex.x > self.vertices[1].vertex.x
            ):
                vertex1 = self.vertices[1]
                vertex2 = self.vertices[0]
            else:
                vertex1 = self.vertices[0]
                vertex2 = self.vertices[1]

        return (vertex1, vertex2)

    def add_vertex(self, vertex: Any):
        """Add vertex."""
        if len(self.vertices) >= 2:
            return
        self.vertices.append(vertex)

    def get_ranges(
        self,
    ) -> List[Tuple[List[Optional[Decimal]], List[Optional[Decimal]]]]:
        """Get Ranges to graph in the Voronoi Diagram."""
        raise NotImplementedError

    def add_begin_range(
        self, x: Decimal, boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add new of the the bisector to be graphed."""
        if boundary_sign:
            self.ranges_b_plus.append((x, None, side))
        else:
            self.ranges_b_minus.append((x, None, side))

    def add_end_range(
        self, x: Decimal, boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add new of the the bisector to be graphed."""
        raise NotImplementedError


class VoronoiDiagramPointBisector(VoronoiDiagramBisector):
    """Point Bisector representation in Voronoi Diagram."""

    def __init__(
        self,
        bisector: PointBisector,
        boundary_plus: PointBoundary,
        boundary_minus: PointBoundary,
        vertex1: Any = None,
        vertex2: Any = None,
    ):
        """Create Voronoi Diagram Weighted Bisector."""
        super().__init__(bisector, boundary_plus, boundary_minus, vertex1, vertex2)

    def get_ranges(
        self,
    ) -> List[Tuple[List[Optional[Decimal]], List[Optional[Decimal]]]]:
        """Get Ranges to plot."""
        pass

    def add_end_range(
        self, x: Decimal, boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add new of the the bisector to be graphed."""
        if boundary_sign:
            ranges = self.ranges_b_plus
        else:
            ranges = self.ranges_b_minus

        ranges[-1] = (ranges[-1][0], x, side)


class VoronoiDiagramWeightedPointBisector(VoronoiDiagramBisector):
    """Weighted Point Bisector representation in Voronoi Diagram."""

    def __init__(
        self,
        bisector: WeightedPointBisector,
        boundary_plus: WeightedPointBoundary,
        boundary_minus: WeightedPointBoundary,
        vertex1: Any = None,
        vertex2: Any = None,
    ):
        """Create Voronoi Diagram Weighted Bisector."""
        super().__init__(bisector, boundary_plus, boundary_minus, vertex1, vertex2)

    def get_ranges(
        self,
    ) -> List[Tuple[List[Optional[Decimal]], List[Optional[Decimal]]]]:
        """Get Ranges to plot."""
        pass

    def add_end_range(
        self, x: Decimal, boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add new of the the bisector to be graphed."""
        if boundary_sign:
            ranges = self.ranges_b_plus
        else:
            ranges = self.ranges_b_minus

        last_side = ranges[-1][2]
        if last_side != side:
            changes_of_sign_in_x = self.bisector.get_changes_of_sign_in_x()[0]
            if len(changes_of_sign_in_x) >= 1:
                ranges[-1] = (
                    ranges[-1][0],
                    changes_of_sign_in_x[0],
                    last_side,
                )
                ranges.append((changes_of_sign_in_x[0], x, side))
        else:
            ranges[-1] = (ranges[-1][0], x, side)
