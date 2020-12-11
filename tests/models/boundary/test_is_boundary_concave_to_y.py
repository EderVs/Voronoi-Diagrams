"""Test is_boundary_not_x_monotone method in WeightedPointBoundary."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.models import (
    WeightedSite,
    WeightedPointBisector,
    WeightedPointBoundary,
)

# Math
from decimal import Decimal


class TestWeightedPointBoundaryIsBoundaryConcaveToY:
    """Test formula."""

    def test_with_concave_to_y_boundary(self):
        """Test with a boundary that is concave to y."""
        p = WeightedSite(Decimal(-20), Decimal(10), Decimal(2))
        # q is the one in the top.
        q = WeightedSite(Decimal(-5), Decimal(10), Decimal(7))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)
        assert not boundary_plus.is_boundary_not_x_monotone()
        assert boundary_minus.is_boundary_not_x_monotone()

    def test_with_normal_boundary(self):
        """Test with a boundary that is not concave to y."""
        p = WeightedSite(Decimal(-20), Decimal(10), Decimal(2))
        # q is the one in the top.
        q = WeightedSite(Decimal(-8), Decimal(18), Decimal(7))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)
        assert not boundary_plus.is_boundary_not_x_monotone()
        assert not boundary_minus.is_boundary_not_x_monotone()

    def test_with_stopped_boundary(self):
        """Test with a boundary that is not concave to y."""
        p = WeightedSite(Decimal(-20), Decimal(10), Decimal(2))
        # q is the one in the top.
        q = WeightedSite(Decimal(-5), Decimal(15), Decimal(7))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)
        assert not boundary_plus.is_boundary_not_x_monotone()
        assert not boundary_minus.is_boundary_not_x_monotone()
