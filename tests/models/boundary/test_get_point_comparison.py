"""Test get_point_comparison method."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.models import (
    WeightedSite,
    WeightedPointBisector,
    WeightedPointBoundary,
    Point,
)

# Math
from decimal import Decimal


class TestWeightedPointBoundaryIsPointInAllRegion:
    """Test get_point_comparison method in WeightedPointBoundary."""

    def test_with_concave_to_y_boundary(self):
        """Test with a boundary that is concave to y."""
        p = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        # q is the one in the top.
        q = WeightedSite(Decimal(40), Decimal(10), Decimal(6))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)

        # Points in boundary
        # Point in event point.
        point = Point(Decimal("40"), Decimal("16"))
        assert boundary_plus.get_point_comparison(point) == 0
        assert boundary_minus.get_point_comparison(point) > 0
        # Point in Boundary-
        point = Point(Decimal("36"), Decimal("16.17424305044159994757531098"))
        assert boundary_minus.get_point_comparison(point) == 0
        assert boundary_plus.get_point_comparison(point) < 0
        point = Point(Decimal("36"), Decimal("107.8257569495584071586485307"))
        assert boundary_minus.get_point_comparison(point) == 0
        assert boundary_plus.get_point_comparison(point) < 0
        point = Point(Decimal("45"), Decimal("215.8749217771908888306107530"))
        assert boundary_minus.get_point_comparison(point) == 0
        assert boundary_plus.get_point_comparison(point) < 0
        # Point in Boundary+
        point = Point(Decimal("45"), Decimal("16.12507822280910540692058362"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) == 0

        # Point inside
        point = Point(Decimal("45"), Decimal("25"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) < 0

        # Points outside
        point = Point(Decimal("70"), Decimal("17"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) > 0
        point = Point(Decimal("31"), Decimal("17"))
        assert boundary_minus.get_point_comparison(point) < 0
        assert boundary_plus.get_point_comparison(point) < 0
        point = Point(Decimal("0"), Decimal("40"))
        assert boundary_minus.get_point_comparison(point) < 0
        assert boundary_plus.get_point_comparison(point) < 0
        point = Point(Decimal("50"), Decimal("300"))
        assert boundary_minus.get_point_comparison(point) < 0
        assert boundary_plus.get_point_comparison(point) < 0

        # No Weight
        p = WeightedSite(Decimal(40), Decimal(0), Decimal(0))
        # q is the one in the top.
        q = WeightedSite(Decimal(20), Decimal(0), Decimal(0))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)

        # Right.
        point = Point(Decimal("38"), Decimal("2"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) > 0

        # Left.
        point = Point(Decimal("25"), Decimal("5"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) < 0

        # In middle
        point = Point(Decimal("30"), Decimal("5"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) == 0

    def test_with_normal_boundary(self):
        """Test with a boundary that is not concave to y."""
        p = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        # q is the one in the top.
        q = WeightedSite(Decimal(40), Decimal(30), Decimal(6))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)

        # Points in boundary
        # Point in event point.
        point = Point(Decimal("40"), Decimal("36"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) == 0
        # Point in Boundary+
        point = Point(Decimal("70"), Decimal("44.51646544245032821756886326"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) == 0
        # Point in Boundary-
        point = Point(Decimal("24"), Decimal("50.49390153191919183928135506"))
        assert boundary_minus.get_point_comparison(point) == 0
        assert boundary_plus.get_point_comparison(point) < 0

        # Point inside
        point = Point(Decimal("30"), Decimal("70"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) < 0

        # Points outside
        point = Point(Decimal("90"), Decimal("50"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) > 0
        point = Point(Decimal("10"), Decimal("50"))
        assert boundary_minus.get_point_comparison(point) < 0
        assert boundary_plus.get_point_comparison(point) < 0

    def test_with_stopped_boundary(self):
        """Test with a boundary that is not concave to y."""
        p = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        # q is the one in the top.
        q = WeightedSite(Decimal(30), Decimal(14), Decimal(6))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)

        # Points in boundary
        # Point in event point.
        point = Point(Decimal("30"), Decimal("20"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) == 0
        # Point in Boundary+
        point = Point(Decimal("60"), Decimal("26.94980694980695009479400205"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) == 0
        # Point in Boundary-
        point = Point(Decimal("24"), Decimal("30.28571428571428495693446374"))
        assert boundary_minus.get_point_comparison(point) == 0
        assert boundary_plus.get_point_comparison(point) < 0

        # Point inside
        point = Point(Decimal("30"), Decimal("70"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) < 0

        # Points outside
        point = Point(Decimal("40"), Decimal("21"))
        assert boundary_minus.get_point_comparison(point) > 0
        assert boundary_plus.get_point_comparison(point) > 0
        point = Point(Decimal("25"), Decimal("21"))
        assert boundary_minus.get_point_comparison(point) < 0
        assert boundary_plus.get_point_comparison(point) < 0


# TestWeightedPointBoundaryIsPointInAllRegion().test_with_stopped_boundary()
