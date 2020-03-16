"""Test the comparisons in Point Region."""

# Models
from voronoi_diagrams.data_structures.l import LNode
from voronoi_diagrams.data_structures.models import (
    Point,
    PointBisector,
    PointRegion,
    PointBoundary,
)


class TestIsContained:
    """Test that a point is contained in the Region."""

    def test_point_contained(self):
        """Test point is contained in a region with both boundaries."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = PointRegion(q, boundary_minus, boundary_plus)

        # Point Inside
        point = Point(2, 3)
        assert region.is_contained(point)

        # Point Outside
        point = Point(6, 3)
        assert not region.is_contained(point)
        point = Point(0, 3)
        assert not region.is_contained(point)
        point = Point(2, 1.5)
        assert not region.is_contained(point)

    def test_points_in_boundaries(self):
        """Test points in both boundaries."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = PointRegion(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_right = Point(5.449489742783178, 3)
        assert region.is_contained(point_right)
        point_left = Point(0.5505102572168221, 3)
        assert region.is_contained(point_left)

    def test_point_in_site(self):
        """Test point in site."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = PointRegion(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_site = Point(2, 2)
        assert region.is_contained(point_site)

    def test_without_boundaries(self):
        """Test point is contained in a region with both boundaries."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Region without left
        region_no_left = PointRegion(q, None, boundary_plus)

        # Points inside
        point = Point(2, 3)
        assert region_no_left.is_contained(point)
        point = Point(-100, 2)
        assert region_no_left.is_contained(point)
        # Points outside
        point = Point(100, 2)
        assert not region_no_left.is_contained(point)
        point = Point(-100, 1)
        assert not region_no_left.is_contained(point)

        # Region without right
        region_no_right = PointRegion(q, boundary_minus, None)

        # Points inside
        point = Point(2, 3)
        assert region_no_right.is_contained(point)
        point = Point(100, 2)
        assert region_no_right.is_contained(point)
        # Points outside
        point = Point(-100, 2)
        assert not region_no_right.is_contained(point)
        point = Point(100, 1)
        assert not region_no_right.is_contained(point)

        # Region without any
        region_no_boundaries = PointRegion(q, None, None)

        # Points inside
        point = Point(2, 3)
        assert region_no_boundaries.is_contained(point)
        point = Point(100, 2)
        assert region_no_boundaries.is_contained(point)
        point = Point(-100, 2)
        assert region_no_boundaries.is_contained(point)
        # Points outside
        point = Point(100, 1)
        assert not region_no_boundaries.is_contained(point)


class TestIsLeft:
    """Test that a point is left to a the Region."""

    def test_point_left(self):
        """Test point is contained in a region with both boundaries."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = PointRegion(q, boundary_minus, boundary_plus)

        # Point Inside
        point = Point(2, 3)
        assert not region.is_right(point)

        # Point Outside
        point = Point(6, 3)
        assert not region.is_left(point)
        point = Point(0, 3)
        assert region.is_left(point)
        point = Point(2, 1.5)
        assert not region.is_left(point)

    def test_points_in_boundaries(self):
        """Test points in both boundaries."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = PointRegion(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_right = Point(5.449489742783178, 3)
        assert not region.is_left(point_right)
        point_left = Point(0.5505102572168221, 3)
        assert not region.is_left(point_left)

    def test_point_in_site(self):
        """Test point in site."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = PointRegion(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_site = Point(2, 2)
        assert not region.is_left(point_site)

    def test_without_boundaries(self):
        """Test point is contained in a region with both boundaries."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Region without left
        region_no_left = PointRegion(q, None, boundary_plus)

        # Points inside
        point = Point(2, 3)
        assert not region_no_left.is_left(point)
        point = Point(-100, 2)
        assert not region_no_left.is_left(point)
        # Points outside
        point = Point(100, 2)
        assert not region_no_left.is_left(point)
        point = Point(-100, 1)
        assert not region_no_left.is_left(point)

        # Region without right
        region_no_right = PointRegion(q, boundary_minus, None)

        # Points inside
        point = Point(2, 3)
        assert not region_no_right.is_left(point)
        # Points outside
        point = Point(-100, 2)
        assert region_no_right.is_left(point)
        point = Point(100, 1)
        assert not region_no_right.is_left(point)

        # Region without any
        region_no_boundaries = PointRegion(q, None, None)

        # Points inside
        point = Point(2, 3)
        assert not region_no_boundaries.is_left(point)
        point = Point(100, 2)
        assert not region_no_boundaries.is_left(point)
        point = Point(-100, 2)
        assert not region_no_boundaries.is_left(point)
        # Points outside
        point = Point(100, 1)
        assert not region_no_boundaries.is_left(point)


class TestIsRight:
    """Test that a point is right to a the Region."""

    def test_point_right(self):
        """Test point is contained in a region with both boundaries."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = PointRegion(q, boundary_minus, boundary_plus)

        # Point Inside
        point = Point(2, 3)
        assert not region.is_right(point)

        # Point Outside
        point = Point(6, 3)
        assert region.is_right(point)
        point = Point(0, 3)
        assert not region.is_right(point)
        point = Point(2, 1.5)
        assert not region.is_right(point)

    def test_points_in_boundaries(self):
        """Test points in both boundaries."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = PointRegion(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_right = Point(5.449489742783178, 3)
        assert not region.is_right(point_right)
        point_left = Point(0.5505102572168221, 3)
        assert not region.is_right(point_left)

    def test_point_in_site(self):
        """Test point in site."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = PointRegion(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_site = Point(2, 2)
        assert not region.is_right(point_site)

    def test_without_boundaries(self):
        """Test point is contained in a region with both boundaries."""
        p = Point(0, 0)
        q = Point(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Region without left
        region_no_left = PointRegion(q, None, boundary_plus)

        # Points inside
        point = Point(2, 3)
        assert not region_no_left.is_right(point)
        point = Point(-100, 2)
        assert not region_no_left.is_right(point)
        # Points outside
        point = Point(100, 2)
        assert region_no_left.is_right(point)
        point = Point(-100, 1)
        assert not region_no_left.is_right(point)

        # Region without right
        region_no_right = PointRegion(q, boundary_minus, None)

        # Points inside
        point = Point(2, 3)
        assert not region_no_right.is_right(point)
        # Points outside
        point = Point(-100, 2)
        assert not region_no_right.is_right(point)
        point = Point(100, 1)
        assert not region_no_right.is_right(point)

        # Region without any
        region_no_boundaries = PointRegion(q, None, None)

        # Points inside
        point = Point(2, 3)
        assert not region_no_boundaries.is_right(point)
        point = Point(100, 2)
        assert not region_no_boundaries.is_right(point)
        point = Point(-100, 2)
        assert not region_no_boundaries.is_right(point)
        # Points outside
        point = Point(100, 1)
        assert not region_no_boundaries.is_right(point)
