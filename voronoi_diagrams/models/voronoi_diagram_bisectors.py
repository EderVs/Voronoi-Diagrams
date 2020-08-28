"""Bisectors Representations in the Voronoi Diagram."""

from typing import Tuple, Any, Optional, List
from decimal import Decimal
import numpy as np

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
    ranges_vertical: List[Tuple[Optional[Decimal], Optional[Decimal]]]

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
        self.ranges_vertical = []
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

    def get_x(self, y: Decimal) -> Optional[Decimal]:
        """Get x given y of the bisector.
        
        Used in vertical bisectors.
        """
        xs = self.bisector.formula_x(y)
        if len(xs) == 0:
            return None
        return xs[0]

    def get_ranges(
        self, xlim: Tuple[Decimal, Decimal], ylim: Tuple[Decimal, Decimal]
    ) -> Tuple[List[Optional[Decimal]], List[Optional[Decimal]]]:
        """Get Ranges to plot."""
        x_ranges = []
        y_ranges = []

        self.complete_ranges()
        if self.bisector.is_vertical():
            for y0, y1 in self.ranges_vertical:
                if y0 is None:
                    y0 = ylim[0]
                if y1 is None:
                    y1 = ylim[1]
                step = abs(y0 - y1) / Decimal("1000")
                y_range = np.arange(y0, y1, step)
                x_range = [self.get_x(y) for y in y_range]
                x_ranges.append(x_range)
                y_ranges.append(y_range)
        else:
            self.complete_ranges()
            for x1, x0, side in self.ranges_b_minus[::-1]:
                if x0 is None:
                    if side == 0:
                        x0 = xlim[0]
                    else:
                        x0 = xlim[1]
                step = abs(x0 - x1) / Decimal("1000")
                if side == 1:
                    x_range = np.arange(x0, x1, -step)
                else:
                    x_range = np.arange(x0, x1, step)
                y_range = []
                for x in x_range:
                    y_range.append(self.get_y_by_side(x, side))
                x_ranges.append(x_range)
                y_ranges.append(y_range)
            for x0, x1, side in self.ranges_b_plus:
                if x1 is None:
                    if side == 0:
                        x1 = xlim[1]
                    else:
                        x1 = xlim[0]
                step = abs(x0 - x1) / Decimal("1000")
                if side == 1:
                    x_range = np.arange(x0, x1, -step)
                else:
                    x_range = np.arange(x0, x1, step)
                y_range = []
                for x in x_range:
                    y_range.append(self.get_y_by_side(x, side))
                x_ranges.append(x_range)
                y_ranges.append(y_range)

        ranges = (np.concatenate(x_ranges), np.concatenate(y_ranges))
        return ranges

    def get_y_by_side(self, w: Decimal, side: BisectorSide) -> Optional[Decimal]:
        """Get y by BisectorSide."""
        raise NotImplementedError

    def add_begin_range(
        self, x: Decimal, boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add new of the the bisector to be graphed."""
        if boundary_sign:
            self.ranges_b_plus.append((x, None, side))
        else:
            self.ranges_b_minus.append((x, None, side))

    def add_begin_range_vertical(self, y: Optional[Decimal]):
        """Add new vertical range."""
        self.ranges_vertical.append((y, None))

    def add_end_range(
        self, x: Decimal, boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add end of the bisector to be ploted."""
        raise NotImplementedError

    def add_end_range_vertical(self, y: Decimal):
        """Add end of the vertical range."""
        self.ranges_vertical[-1] = (self.ranges_vertical[-1][0], y)

    def complete_ranges(self):
        """Add a new range if neccessary."""
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

    def add_end_range(
        self, x: Decimal, boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add new of the the bisector to be graphed."""
        if boundary_sign:
            ranges = self.ranges_b_plus
        else:
            ranges = self.ranges_b_minus

        ranges[-1] = (ranges[-1][0], x, side)

    def get_y_by_side(self, x: Decimal, side: BisectorSide) -> Optional[Decimal]:
        """Get y by BisectorSide."""
        ys = self.bisector.formula_y(x)
        if len(ys) == 0:
            return None
        return ys[0]

    def complete_ranges(self):
        """Add a new range if neccessary."""
        pass


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

    def add_end_range(
        self, x: Optional[Decimal], boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add new of the the bisector to be graphed."""
        if boundary_sign:
            ranges = self.ranges_b_plus
        else:
            ranges = self.ranges_b_minus

        last_side = ranges[-1][2]
        if last_side != side:
            changes_of_sign_in_x = self.bisector.get_changes_of_sign_in_x()
            if len(changes_of_sign_in_x) >= 1:
                ranges[-1] = (
                    ranges[-1][0],
                    changes_of_sign_in_x[0],
                    last_side,
                )
                ranges.append((changes_of_sign_in_x[0], x, side))
        else:
            ranges[-1] = (ranges[-1][0], x, side)

    def get_y_by_side(self, x: Decimal, side: BisectorSide) -> Optional[Decimal]:
        """Get y by BisectorSide."""
        ys = self.bisector.formula_y(x)
        if len(ys) == 0:
            return None
        elif len(ys) == 1:
            return ys[0]
        else:
            if side == 1:
                return max(ys)
            return min(ys)

    def complete_ranges(self):
        """Add a new range if neccessary."""
        if len(self.ranges_b_minus) > 0:
            x1, x0, side = self.ranges_b_minus[-1]
            if (
                x0 is None
                and side == 0
                and self.boundary_minus.is_boundary_concave_to_y()
            ):
                self.add_end_range(None, False, 1)
                return
        if len(self.ranges_b_plus) > 0:
            x0, x1, side = self.ranges_b_plus[-1]
            if (
                x1 is None
                and side == 0
                and self.boundary_plus.is_boundary_concave_to_y()
            ):
                self.add_end_range(None, True, 1)
