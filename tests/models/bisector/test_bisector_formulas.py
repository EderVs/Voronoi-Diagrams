"""Bisector Formulas Tests."""
# Standard
from typing import List, Any
from random import randint

# Math
from decimal import Decimal

# Models
from voronoi_diagrams.models import (
    PointBisector,
    Point,
    Site,
    WeightedPointBisector,
    WeightedSite,
)

# Utils
from general_utils.numbers import are_close


class TestBisectorFormulas:
    """Test formula."""

    def test_point_formulas_positive_fixed_values(self):
        """Test point formula with 2 positive fixed sites."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        bisector = PointBisector(sites=(p, q))
        assert bisector.formula_x(1)[0] == 1
        assert bisector.formula_y(1)[0] == 1

    def test_point_formulas_negative_fixed_values(self):
        """Test point formula with 2 negative fixed sites."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(-2), Decimal(-2))
        bisector = PointBisector(sites=(p, q))
        assert bisector.formula_x(-1)[0] == -1
        assert bisector.formula_y(-1)[0] == -1

    def test_point_formulas_random_values(self):
        """Test point formula with 2 random sites."""
        p = Site(Decimal(randint(-100, 100)), Decimal(randint(-100, 100)))
        q = Site(Decimal(randint(-100, 100)), Decimal(randint(-100, 100)))
        while q.point.x == p.point.x or q.point.y == p.point.y:
            q = Site(Decimal(randint(-100, 100)), Decimal(randint(-100, 100)))
        bisector = PointBisector(sites=(p, q))
        x = Decimal(randint(-100, 100))
        y = bisector.formula_y(x)[0]
        assert (x - bisector.formula_x(y)[0]) < 0.00000000001


class TestWeightedPointBisectorFormulas:
    """Test formula in WeightedPointBisector."""

    def test_limit_in_x(self):
        """Test point formula with 2 positive fixed sites."""
        p = WeightedSite(Decimal(2), Decimal(2), Decimal(2.5))
        q = WeightedSite(Decimal(9), Decimal(2), Decimal(1.5))
        bisector = WeightedPointBisector(sites=(p, q))
        epsilon = Decimal(0.00001)
        x = Decimal(5)
        y = Decimal(2)
        values_y = bisector.formula_y(x)
        assert len(values_y) == 1
        assert are_close(values_y[0], y, epsilon)
        values_x = bisector.formula_x(y)
        assert len(values_x) == 1
        assert are_close(values_x[0], x, epsilon)

    def test_limit_in_y(self):
        """Test point formula with 2 positive fixed sites."""
        p = WeightedSite(Decimal(4), Decimal(9), Decimal(2.5))
        q = WeightedSite(Decimal(4), Decimal(1), Decimal(1.5))
        bisector = WeightedPointBisector(sites=(p, q))
        epsilon = Decimal(0.00001)
        x = Decimal(4)
        y = Decimal(5.5)
        values_y = bisector.formula_y(x)
        assert len(values_y) == 1
        assert are_close(values_y[0], y, epsilon)
        values_x = bisector.formula_x(y)
        assert len(values_x) == 1
        assert are_close(values_x[0], x, epsilon)

    def test_one_value(self):
        """Test point formula with 2 positive fixed sites."""
        p = WeightedSite(Decimal(2), Decimal(5), Decimal(2.5))
        q = WeightedSite(Decimal(9), Decimal(2), Decimal(1.5))
        bisector = WeightedPointBisector(sites=(p, q))
        epsilon = Decimal(0.00001)
        x = Decimal(5)
        y = Decimal("3.603093956613265568231878402")
        values_y = bisector.formula_y(x)
        assert len(values_y) == 1
        assert are_close(values_y[0], y, epsilon)
        values_x = bisector.formula_x(y)
        assert len(values_x) == 1
        assert are_close(values_x[0], x, epsilon)

    def test_two_values_in_x(self):
        """Test point formula with 2 positive fixed sites."""
        p = WeightedSite(Decimal(4), Decimal(8), Decimal(4))
        q = WeightedSite(Decimal(4), Decimal(-5), Decimal(0.5))
        bisector = WeightedPointBisector(sites=(p, q))
        epsilon = Decimal(0.00001)
        x1 = Decimal("0.5364507410190114199498303")
        x2 = Decimal("7.4635492589809885800501697")
        y = Decimal(3.5)
        values_x = bisector.formula_x(y)
        assert len(values_x) == 2
        assert are_close(values_x[0], x1, epsilon) or are_close(
            values_x[0], x2, epsilon
        )
        assert are_close(values_x[1], x1, epsilon) or are_close(
            values_x[1], x2, epsilon
        )
        values_y = bisector.formula_y(x1)
        assert len(values_y) == 1
        assert are_close(values_y[0], y, epsilon)
        values_y = bisector.formula_y(x2)
        assert len(values_y) == 1
        assert are_close(values_y[0], y, epsilon)

    def test_two_values_in_y(self):
        """Test point formula with 2 positive fixed sites."""
        p = WeightedSite(Decimal(-18), Decimal(-5), Decimal(7))
        q = WeightedSite(Decimal(4), Decimal(-5), Decimal(0.5))
        bisector = WeightedPointBisector(sites=(p, q))
        epsilon = Decimal(0.00001)
        x = Decimal("-11")
        y1 = Decimal("2.540055757645454365868074183")
        y2 = Decimal("-12.54005575764545436586807418")
        values_y = bisector.formula_y(x)
        assert len(values_y) == 2
        assert are_close(values_y[0], y1, epsilon) or are_close(
            values_y[0], y2, epsilon
        )
        assert are_close(values_y[1], y1, epsilon) or are_close(
            values_y[1], y2, epsilon
        )
        values_x = bisector.formula_x(y1)
        assert len(values_x) == 1
        assert are_close(values_x[0], x, epsilon)
        values_x = bisector.formula_x(y2)
        assert len(values_x) == 1
        assert are_close(values_x[0], x, epsilon)
