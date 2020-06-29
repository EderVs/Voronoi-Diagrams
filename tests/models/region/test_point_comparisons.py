"""Test the comparisons in Point Region."""

# Data Structures
from voronoi_diagrams.data_structures.l import LNode

# Models
from voronoi_diagrams.models import (
    Site,
    WeightedSite,
    Point,
    PointBisector,
    PointBisector,
    WeightedPointBisector,
    Region,
    WeightedPointBoundary,
    PointBoundary,
)

# Math
from decimal import Decimal


class TestIsContainedPointSite:
    """Test that a point is contained in the Region."""

    def test_point_contained(self):
        """Test point is contained in a region with both boundaries."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = Region(q, boundary_minus, boundary_plus)

        # Point Inside
        point = Point(Decimal(2), Decimal(3))
        assert region.is_contained(point)

        # Point Outside
        point = Point(Decimal(6), Decimal(3))
        assert not region.is_contained(point)
        point = Point(Decimal(0), Decimal(3))
        assert not region.is_contained(point)
        point = Point(Decimal(2), Decimal(1.5))
        assert not region.is_contained(point)

    def test_points_in_boundaries(self):
        """Test points in both boundaries."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = Region(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_right = Point(Decimal(5.449489742783178), Decimal(3))
        assert region.is_contained(point_right)
        point_left = Point(Decimal(0.5505102572168221), Decimal(3))
        assert region.is_contained(point_left)

    def test_point_in_site(self):
        """Test point in site."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = Region(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_site = Point(Decimal(2), Decimal(2))
        assert region.is_contained(point_site)

    def test_without_boundaries(self):
        """Test point is contained in a region with both boundaries."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Region without left
        region_no_left = Region(q, None, boundary_plus)

        # Points inside
        point = Point(Decimal(2), Decimal(3))
        assert region_no_left.is_contained(point)
        point = Point(Decimal(-100), Decimal(2))
        assert region_no_left.is_contained(point)
        # Points outside
        point = Point(Decimal(100), Decimal(2))
        assert not region_no_left.is_contained(point)
        point = Point(Decimal(-100), Decimal(1))
        assert not region_no_left.is_contained(point)

        # Region without right
        region_no_right = Region(q, boundary_minus, None)

        # Points inside
        point = Point(Decimal(2), Decimal(3))
        assert region_no_right.is_contained(point)
        point = Point(Decimal(100), Decimal(2))
        assert region_no_right.is_contained(point)
        # Points outside
        point = Point(Decimal(-100), Decimal(2))
        assert not region_no_right.is_contained(point)
        point = Point(Decimal(100), Decimal(1))
        assert not region_no_right.is_contained(point)

        # Region without any
        region_no_boundaries = Region(q, None, None)

        # Points inside
        point = Point(Decimal(2), Decimal(3))
        assert region_no_boundaries.is_contained(point)
        point = Point(Decimal(100), Decimal(2))
        assert region_no_boundaries.is_contained(point)
        point = Point(Decimal(-100), Decimal(2))
        assert region_no_boundaries.is_contained(point)
        # Points outside
        point = Point(Decimal(100), Decimal(1))
        assert not region_no_boundaries.is_contained(point)


class TestIsLeftPointSite:
    """Test that a point is left to a the Region."""

    def test_point_left(self):
        """Test point is contained in a region with both boundaries."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = Region(q, boundary_minus, boundary_plus)

        # Point Inside
        point = Point(Decimal(2), Decimal(3))
        assert not region.is_right(point)

        # Point Outside
        point = Point(Decimal(6), Decimal(3))
        assert not region.is_left(point)
        point = Point(Decimal(0), Decimal(3))
        assert region.is_left(point)
        point = Point(Decimal(2), Decimal(1.5))
        assert not region.is_left(point)

    def test_points_in_boundaries(self):
        """Test points in both boundaries."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = Region(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_right = Point(Decimal(5.449489742783178), Decimal(3))
        assert not region.is_left(point_right)
        point_left = Point(Decimal(0.5505102572168221), Decimal(3))
        assert not region.is_left(point_left)

    def test_point_in_site(self):
        """Test point in site."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = Region(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_site = Point(Decimal(2), Decimal(2))
        assert not region.is_left(point_site)

    def test_without_boundaries(self):
        """Test point is contained in a region with both boundaries."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Region without left
        region_no_left = Region(q, None, boundary_plus)

        # Points inside
        point = Point(Decimal(2), Decimal(3))
        assert not region_no_left.is_left(point)
        point = Point(Decimal(-100), Decimal(2))
        assert not region_no_left.is_left(point)
        # Points outside
        point = Point(Decimal(100), Decimal(2))
        assert not region_no_left.is_left(point)
        point = Point(Decimal(-100), Decimal(1))
        assert not region_no_left.is_left(point)

        # Region without right
        region_no_right = Region(q, boundary_minus, None)

        # Points inside
        point = Point(Decimal(2), Decimal(3))
        assert not region_no_right.is_left(point)
        # Points outside
        point = Point(Decimal(-100), Decimal(2))
        assert region_no_right.is_left(point)
        point = Point(Decimal(100), Decimal(1))
        assert not region_no_right.is_left(point)

        # Region without any
        region_no_boundaries = Region(q, None, None)

        # Points inside
        point = Point(Decimal(2), Decimal(3))
        assert not region_no_boundaries.is_left(point)
        point = Point(Decimal(100), Decimal(2))
        assert not region_no_boundaries.is_left(point)
        point = Point(Decimal(-100), Decimal(2))
        assert not region_no_boundaries.is_left(point)
        # Points outside
        point = Point(Decimal(100), Decimal(1))
        assert not region_no_boundaries.is_left(point)


class TestIsRightPointSite:
    """Test that a point is right to a the Region."""

    def test_point_right(self):
        """Test point is contained in a region with both boundaries."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = Region(q, boundary_minus, boundary_plus)

        # Point Inside
        point = Point(Decimal(2), Decimal(3))
        assert not region.is_right(point)

        # Point Outside
        point = Point(Decimal(6), Decimal(3))
        assert region.is_right(point)
        point = Point(Decimal(0), Decimal(3))
        assert not region.is_right(point)
        point = Point(Decimal(2), Decimal(1.5))
        assert not region.is_right(point)

    def test_points_in_boundaries(self):
        """Test points in both boundaries."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = Region(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_right = Point(Decimal(5.449489742783178), Decimal(3))
        assert not region.is_right(point_right)
        point_left = Point(Decimal(0.5505102572168221), Decimal(3))
        assert not region.is_right(point_left)

    def test_point_in_site(self):
        """Test point in site."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Creating Region with the info above
        region = Region(q, boundary_minus, boundary_plus)

        # Points in boundaries
        point_site = Point(Decimal(2), Decimal(2))
        assert not region.is_right(point_site)

    def test_without_boundaries(self):
        """Test point is contained in a region with both boundaries."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)

        # Region without left
        region_no_left = Region(q, None, boundary_plus)

        # Points inside
        point = Point(Decimal(2), Decimal(3))
        assert not region_no_left.is_right(point)
        point = Point(Decimal(-100), Decimal(2))
        assert not region_no_left.is_right(point)
        # Points outside
        point = Point(Decimal(100), Decimal(2))
        assert region_no_left.is_right(point)
        point = Point(Decimal(-100), Decimal(1))
        assert not region_no_left.is_right(point)

        # Region without right
        region_no_right = Region(q, boundary_minus, None)

        # Points inside
        point = Point(Decimal(2), Decimal(3))
        assert not region_no_right.is_right(point)
        # Points outside
        point = Point(Decimal(-100), Decimal(2))
        assert not region_no_right.is_right(point)
        point = Point(Decimal(100), Decimal(1))
        assert not region_no_right.is_right(point)

        # Region without any
        region_no_boundaries = Region(q, None, None)

        # Points inside
        point = Point(Decimal(2), Decimal(3))
        assert not region_no_boundaries.is_right(point)
        point = Point(Decimal(100), Decimal(2))
        assert not region_no_boundaries.is_right(point)
        point = Point(Decimal(-100), Decimal(2))
        assert not region_no_boundaries.is_right(point)
        # Points outside
        point = Point(Decimal(100), Decimal(1))
        assert not region_no_boundaries.is_right(point)


class TestIsRightWeightedPointSite:
    """Test that a point is right to a the Region using weighted point sites."""

    def test_point_right(self):
        """Test point is contained in a region with both boundaries."""
        p = WeightedSite(Decimal(-18), Decimal(10), Decimal(6))
        q = WeightedSite(Decimal(0), Decimal(0), Decimal(1.5))
        r = WeightedSite(Decimal(10), Decimal(12), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector=bisector_pq, sign=True)
        boundary_pq_minus = WeightedPointBoundary(bisector=bisector_pq, sign=False)
        boundary_qr_plus = WeightedPointBoundary(bisector=bisector_qr, sign=True)
        boundary_qr_minus = WeightedPointBoundary(bisector=bisector_qr, sign=False)

        # Normal Regions
        region = Region(p, boundary_pq_minus, boundary_pq_plus)
        # Point Inside
        point = Point(Decimal(-10), Decimal(30))
        assert not region.is_right(point)
        # Point Outside
        point = Point(Decimal(-6), Decimal(20))
        assert region.is_right(point)
        point = Point(Decimal(-30), Decimal(16))
        assert not region.is_right(point)
        point = Point(Decimal(-10), Decimal(10))
        assert not region.is_right(point)

        region = Region(r, boundary_qr_minus, boundary_qr_plus)
        # Point Inside
        point = Point(Decimal(10), Decimal(20))
        assert not region.is_right(point)
        # Point Outside
        point = Point(Decimal(64), Decimal(22))
        assert region.is_right(point)
        point = Point(Decimal(0), Decimal(20))
        assert not region.is_right(point)
        point = Point(Decimal(10), Decimal(10))
        assert not region.is_right(point)

        # Mixed Region
        region = Region(q, boundary_pq_plus, boundary_qr_minus)
        # Point Inside
        point = Point(Decimal(0), Decimal(20))
        assert not region.is_right(point)
        # Point Outside
        point = Point(Decimal(10), Decimal(20))
        assert region.is_right(point)
        point = Point(Decimal(-20), Decimal(20))
        assert not region.is_right(point)
        point = Point(Decimal(-10), Decimal(30))
        assert not region.is_right(point)

    def test_points_in_boundaries(self):
        """Test points in both boundaries."""
        p = WeightedSite(Decimal(10), Decimal(12), Decimal(2.5))
        q = WeightedSite(Decimal(0), Decimal(0), Decimal(1.5))
        r = WeightedSite(Decimal(-18), Decimal(10), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector=bisector_pq, sign=True)
        boundary_pq_minus = WeightedPointBoundary(bisector=bisector_pq, sign=False)
        boundary_qr_plus = WeightedPointBoundary(bisector=bisector_qr, sign=True)
        boundary_qr_minus = WeightedPointBoundary(bisector=bisector_qr, sign=False)

        # Normal Regions
        region = Region(q, boundary_qr_minus, boundary_qr_plus)
        # Highest point in in site.
        point = r.get_highest_site_point()
        assert not region.is_right(point)
        # Point in right boundary.
        x = Decimal(-10)
        y = region.right.formula_y(x)[0]
        point = Point(x, y)
        assert not region.is_right(point)
        # Point in left boundary.
        x = Decimal(-30)
        y = region.left.formula_y(x)[0]
        point = Point(x, y)
        assert not region.is_right(point)

        # Mixed Region
        region = Region(q, boundary_qr_plus, boundary_pq_minus)
        # Highest point in site.
        point = p.get_highest_site_point()
        assert not region.is_right(point)
        point = r.get_highest_site_point()
        assert not region.is_right(point)
        # Point in right boundary.
        x = Decimal(-0)
        y = region.right.formula_y(x)[0]
        point = Point(x, y)
        assert not region.is_right(point)
        # Point in left boundary.
        x = Decimal(-10)
        y = region.left.formula_y(x)[0]
        point = Point(x, y)
        assert not region.is_right(point)
        # Point in pq plus boundary.
        x = Decimal(30)
        y = boundary_qr_plus.formula_y(x)[0]
        point = Point(x, y)
        assert region.is_right(point)
        # Point in pq minus boundary.
        x = Decimal(-30)
        y = boundary_qr_minus.formula_y(x)[0]
        point = Point(x, y)
        assert not region.is_right(point)


class TestIsLeftWeightedPointSite:
    """Test that a point is left to a the Region using weighted point sites."""

    def test_point_left(self):
        """Test point is contained in a region with both boundaries."""
        p = WeightedSite(Decimal(10), Decimal(12), Decimal(2.5))
        q = WeightedSite(Decimal(0), Decimal(0), Decimal(1.5))
        r = WeightedSite(Decimal(-18), Decimal(10), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector=bisector_pq, sign=True)
        boundary_pq_minus = WeightedPointBoundary(bisector=bisector_pq, sign=False)
        boundary_qr_plus = WeightedPointBoundary(bisector=bisector_qr, sign=True)
        boundary_qr_minus = WeightedPointBoundary(bisector=bisector_qr, sign=False)

        # Normal Regions
        region = Region(p, boundary_pq_minus, boundary_pq_plus)
        # Point Inside
        point = Point(Decimal(10), Decimal(20))
        assert not region.is_left(point)
        # Point Outside
        point = Point(Decimal(64), Decimal(22))
        assert not region.is_left(point)
        point = Point(Decimal(0), Decimal(20))
        assert region.is_left(point)
        point = Point(Decimal(10), Decimal(10))
        assert not region.is_left(point)

        region = Region(r, boundary_qr_minus, boundary_qr_plus)
        # Point Inside
        point = Point(Decimal(-10), Decimal(30))
        assert not region.is_left(point)
        # Point Outside
        point = Point(Decimal(-6), Decimal(20))
        assert not region.is_left(point)
        point = Point(Decimal(-30), Decimal(16))
        assert region.is_left(point)
        point = Point(Decimal(-10), Decimal(10))
        assert not region.is_left(point)

        # Mixed Region
        region = Region(q, boundary_qr_plus, boundary_pq_minus)
        # Point Inside
        point = Point(Decimal(0), Decimal(20))
        assert not region.is_left(point)
        # Point Outside
        point = Point(Decimal(10), Decimal(20))
        assert not region.is_left(point)
        point = Point(Decimal(-20), Decimal(20))
        assert region.is_left(point)
        point = Point(Decimal(-10), Decimal(30))
        assert region.is_left(point)

    def test_points_in_boundaries(self):
        """Test points in both boundaries."""
        p = WeightedSite(Decimal(10), Decimal(12), Decimal(2.5))
        q = WeightedSite(Decimal(0), Decimal(0), Decimal(1.5))
        r = WeightedSite(Decimal(-18), Decimal(10), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector=bisector_pq, sign=True)
        boundary_pq_minus = WeightedPointBoundary(bisector=bisector_pq, sign=False)
        boundary_qr_plus = WeightedPointBoundary(bisector=bisector_qr, sign=True)
        boundary_qr_minus = WeightedPointBoundary(bisector=bisector_qr, sign=False)

        # Normal Regions
        region = Region(q, boundary_qr_minus, boundary_qr_plus)
        # Highest point in in site.
        point = r.get_highest_site_point()
        assert not region.is_left(point)
        # Point in right boundary.
        x = Decimal(-10)
        y = region.right.formula_y(x)[0]
        point = Point(x, y)
        assert not region.is_left(point)
        # Point in left boundary.
        x = Decimal(-30)
        y = region.left.formula_y(x)[0]
        point = Point(x, y)
        assert not region.is_left(point)

        # Mixed Region
        region = Region(q, boundary_qr_plus, boundary_pq_minus)
        # Highest point in site.
        point = p.get_highest_site_point()
        assert not region.is_left(point)
        point = r.get_highest_site_point()
        assert not region.is_left(point)
        # Point in right boundary.
        x = Decimal(-0)
        y = region.right.formula_y(x)[0]
        point = Point(x, y)
        assert not region.is_left(point)
        # Point in left boundary.
        x = Decimal(-10)
        y = region.left.formula_y(x)[0]
        point = Point(x, y)
        assert not region.is_left(point)
        # Point in pq plus boundary.
        x = Decimal(30)
        y = boundary_qr_plus.formula_y(x)[0]
        point = Point(x, y)
        assert not region.is_left(point)
        # Point in pq minus boundary.
        x = Decimal(-30)
        y = boundary_qr_minus.formula_y(x)[0]
        point = Point(x, y)
        assert region.is_left(point)
