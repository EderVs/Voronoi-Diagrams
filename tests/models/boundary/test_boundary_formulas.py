"""Boundary Formulas Tests."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.models import PointBisector, PointBoundary, Site


class TestBoundaryFormulas:
    """Test formula."""

    def test_point_formulas_positive_fixed_values(self):
        """Test point formula with 2 positive fixed sites."""
        p = Site(0, 0)
        q = Site(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)
        y = 3
        x = boundary_plus.formula_x(y)
        assert (y - boundary_plus.formula_y(x)) < 0.00000000001
        x = boundary_minus.formula_x(y)
        assert (y - boundary_minus.formula_y(x)) < 0.00000000001

    def test_point_formulas_negative_fixed_values(self):
        """Test point formula with 2 positive fixed sites."""
        p = Site(0, 0)
        q = Site(-2, -2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)
        y = 3
        x = boundary_plus.formula_x(y)
        assert (y - boundary_plus.formula_y(x)) < 0.00000000001
        x = boundary_minus.formula_x(y)
        assert (y - boundary_minus.formula_y(x)) < 0.00000000001

    def test_point_formulas_random_values(self):
        """Test point formula with 2 random sites."""
        p = Site(randint(-100, 100), randint(-100, 100))
        q = Site(randint(-100, 100), randint(-100, 100))
        while q.point.x == p.point.x or q.point.y == p.point.y:
            q = Site(randint(-100, 100), randint(-100, 100))
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)
        delta = randint(0, 10)
        if p.point.y > q.point.y:
            max_site = p
        else:
            max_site = q
        y = max_site.point.y + delta
        x = boundary_plus.formula_x(y)
        assert (y - boundary_plus.formula_y(x)) < 0.00000000001
        x = boundary_minus.formula_x(y)
        assert (y - boundary_minus.formula_y(x)) < 0.00000000001
