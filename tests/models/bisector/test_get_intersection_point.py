"""Test get bisectors intersection point."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.data_structures.models import PointBisector, Point, Site


class TestGetBisectorIntersectionPoint:
    """Test formula."""

    def test_two_bisectors(self):
        """Test point formula with 3 positive fixed sites."""
        p = Site(0, 0)
        q = Site(2, 2)
        r = Site(2, -2)
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(p, r))
        intersection = bisector_pq.get_intersection_point(bisector_pr)
        assert intersection.x == 2
        assert intersection.y == 0
        intersection2 = bisector_pr.get_intersection_point(bisector_pq)
        assert intersection2.x == 2
        assert intersection2.y == 0