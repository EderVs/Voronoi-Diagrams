"""Test get bisectors intersection point."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.models import PointBisector, Point, Site

# Math
from decimal import Decimal


class TestGetBisectorIntersectionPoint:
    """Test formula."""

    def test_two_bisectors(self):
        """Test point formula with 3 positive fixed sites."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        r = Site(Decimal(2), Decimal(-2))
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(p, r))
        intersections = bisector_pq.get_intersection_points(bisector_pr)
        assert len(intersections) == 1
        intersection = intersections[0]
        assert intersection.x == 2
        assert intersection.y == 0
        intersections2 = bisector_pr.get_intersection_points(bisector_pq)
        assert len(intersections2) == 1
        intersection2 = intersections2[0]
        assert intersection2.x == 2
        assert intersection2.y == 0
