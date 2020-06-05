"""Test get boundaries intersection point."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.models import (
    PointBisector,
    Point,
    Site,
    PointBoundary,
)

# Math
from decimal import Decimal


class TestGetBisectorIntersectionPoint:
    """Test formula."""

    def test_two_boundaries(self):
        """Test get intersection with 3 positive fixed sites."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        r = Site(Decimal(2), Decimal(-2))
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(p, r))
        boundary_pq_plus = PointBoundary(bisector_pq, False)
        boundary_pr_minus = PointBoundary(bisector_pr, True)
        intersection = boundary_pr_minus.get_intersection(boundary_pq_plus)
        assert intersection is not None
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(2)
        assert intersection.y == Decimal(0)
        assert intersection_star.x == Decimal(2)
        assert intersection_star.y == Decimal(2)
        intersection2 = boundary_pq_plus.get_intersection(boundary_pr_minus)
        assert intersection2 is not None
        intersection2, intersection2_star = intersection2
        assert intersection2.x == Decimal(2)
        assert intersection2.y == Decimal(0)
        assert intersection2_star.x == Decimal(2)
        assert intersection2_star.y == Decimal(2)


class TestParallelBisectorsIntersectionPoint:
    """Test that there are no intersections."""

    def test_bisectors_with_slope_0(self):
        """Test when the bisectors are horizontal."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        r = Site(Decimal(2), Decimal(-2))
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(q, r))
        boundary_pq_plus = PointBoundary(bisector_pq, False)
        boundary_pr_minus = PointBoundary(bisector_pr, True)
        intersection = boundary_pr_minus.get_intersection(boundary_pq_plus)
        assert intersection is None

    def test_bisectors_with_infinity_slope(self):
        """Test when the bisectors are vertical."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(1), Decimal(0))
        r = Site(Decimal(2), Decimal(0))
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(q, r))
        boundary_pq_plus = PointBoundary(bisector_pq, False)
        boundary_pr_minus = PointBoundary(bisector_pr, True)
        intersection = boundary_pr_minus.get_intersection(boundary_pq_plus)
        assert intersection is None

    def test_parallel_bisectors(self):
        """Test when the bisectors are diagonals."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(1), Decimal(1))
        r = Site(Decimal(2), Decimal(2))
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(q, r))
        boundary_pq_plus = PointBoundary(bisector_pq, False)
        boundary_pr_minus = PointBoundary(bisector_pr, True)
        intersection = boundary_pr_minus.get_intersection(boundary_pq_plus)
        assert intersection is None
