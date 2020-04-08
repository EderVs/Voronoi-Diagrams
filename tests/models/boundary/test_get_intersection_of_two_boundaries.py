"""Test get boundaries intersection point."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.data_structures.models import (
    PointBisector,
    Point,
    Site,
    PointBoundary,
)


class TestGetBisectorIntersectionPoint:
    """Test formula."""

    def test_two_boundaries(self):
        """Test get intersection with 3 positive fixed sites."""
        p = Site(0, 0)
        q = Site(2, 2)
        r = Site(2, -2)
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(p, r))
        boundary_pq_plus = PointBoundary(bisector_pq, True)
        boundary_pr_minus = PointBoundary(bisector_pr, False)
        intersection = boundary_pr_minus.get_intersection(boundary_pq_plus)
        assert intersection.x == 2
        assert intersection.y == 2
        intersection2 = boundary_pq_plus.get_intersection(boundary_pr_minus)
        assert intersection2.x == 2
        assert intersection2.y == 2
