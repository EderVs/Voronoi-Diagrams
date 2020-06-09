"""Bisector Formulas Tests."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.models import PointBisector, Point, Site


class TestBisectorFormulas:
    """Test formula."""

    def test_point_formulas_positive_fixed_values(self):
        """Test point formula with 2 positive fixed sites."""
        p = Site(0, 0)
        q = Site(2, 2)
        bisector = PointBisector(sites=(p, q))
        assert bisector.formula_x(1)[0] == 1
        assert bisector.formula_y(1)[0] == 1

    def test_point_formulas_negative_fixed_values(self):
        """Test point formula with 2 positive fixed sites."""
        p = Site(0, 0)
        q = Site(-2, -2)
        bisector = PointBisector(sites=(p, q))
        assert bisector.formula_x(-1)[0] == -1
        assert bisector.formula_y(-1)[0] == -1

    def test_point_formulas_random_values(self):
        """Test point formula with 2 random sites."""
        p = Site(randint(-100, 100), randint(-100, 100))
        q = Site(randint(-100, 100), randint(-100, 100))
        while q.point.x == p.point.x or q.point.y == p.point.y:
            q = Site(randint(-100, 100), randint(-100, 100))
        bisector = PointBisector(sites=(p, q))
        x = randint(-100, 100)
        y = bisector.formula_y(x)[0]
        assert (x - bisector.formula_x(y)[0]) < 0.00000000001
