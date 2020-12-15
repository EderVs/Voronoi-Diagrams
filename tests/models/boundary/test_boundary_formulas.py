"""Boundary Formulas Tests."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.models import (
    PointBisector,
    PointBoundary,
    Site,
    WeightedSite,
    WeightedPointBisector,
    WeightedPointBoundary,
)

# Math
from decimal import Decimal

# General Utils
from general_utils.numbers import are_close


class TestPointBoundaryFormulas:
    """Test formula."""

    def test_point_formulas_positive_fixed_values(self):
        """Test point formula with 2 positive fixed sites."""
        p = Site(0, 0)
        q = Site(2, 2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)
        y = 3
        x = boundary_plus.formula_x(y)[0]
        assert (y - boundary_plus.formula_y(x)[0]) < 0.00000000001
        x = boundary_minus.formula_x(y)[0]
        assert (y - boundary_minus.formula_y(x)[0]) < 0.00000000001

    def test_point_formulas_negative_fixed_values(self):
        """Test point formula with 2 positive fixed sites."""
        p = Site(0, 0)
        q = Site(-2, -2)
        bisector = PointBisector(sites=(p, q))
        boundary_plus = PointBoundary(bisector=bisector, sign=True)
        boundary_minus = PointBoundary(bisector=bisector, sign=False)
        y = 3
        x = boundary_plus.formula_x(y)[0]
        assert (y - boundary_plus.formula_y(x)[0]) < 0.00000000001
        x = boundary_minus.formula_x(y)[0]
        assert (y - boundary_minus.formula_y(x)[0]) < 0.00000000001

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
        x = boundary_plus.formula_x(y)[0]
        if (boundary_plus.formula_y(x)) == 1:
            assert (y - boundary_plus.formula_y(x)[0]) < 0.00000000001
        x = boundary_minus.formula_x(y)[0]
        if (boundary_minus.formula_y(x)) == 1:
            assert (y - boundary_minus.formula_y(x)[0]) < 0.00000000001


class TestWeightedPointBoundaryFormulas:
    """Test formula."""

    def test_formula_y_concave_to_y_boundary(self):
        """Test point formula with 2 positive fixed sites."""
        p = WeightedSite(Decimal(-4), Decimal(10), Decimal(7))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)

        # In the middle.
        x = -4

        ys_in_boundary = boundary_plus.formula_y(x)
        assert len(ys_in_boundary) == 1
        assert are_close(max(ys_in_boundary), Decimal("92"), Decimal("0.000000001"))

        ys_in_boundary = boundary_minus.formula_y(x)
        assert len(ys_in_boundary) == 1
        assert are_close(ys_in_boundary[0], Decimal("17"), Decimal("0.000000001"))

        # To the right.
        x = 3

        ys_in_boundary = boundary_plus.formula_y(x)
        assert len(ys_in_boundary) == 2
        assert are_close(
            max(ys_in_boundary),
            Decimal("32.92261628933256451005844924"),
            Decimal("0.000000001"),
        )
        assert are_close(
            min(ys_in_boundary),
            Decimal("20.07738371066743548994155076"),
            Decimal("0.000000001"),
        )

        ys_in_boundary = boundary_minus.formula_y(x)
        assert len(ys_in_boundary) == 0

        # To the left.
        x = -5

        ys_in_boundary = boundary_plus.formula_y(x)
        assert len(ys_in_boundary) == 1
        assert are_close(
            ys_in_boundary[0],
            Decimal("99.98795005781799289501023424"),
            Decimal("0.000000001"),
        )

        ys_in_boundary = boundary_minus.formula_y(x)
        assert len(ys_in_boundary) == 1
        assert are_close(
            ys_in_boundary[0],
            Decimal("17.01204994218200710498976573"),
            Decimal("0.000000001"),
        )

        p = WeightedSite(Decimal(-3.28), Decimal(0.823), Decimal(0.8))
        # q is the one in the top.
        q = WeightedSite(Decimal(-2.49), Decimal(1.24), Decimal(0.2))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)

        # Points in boundary
        # Point in event point
        x = p.point.x - Decimal(1)
        assert len(boundary_plus.formula_y(x)) == 1
        assert len(boundary_minus.formula_y(x)) == 1
        # Point in Boundary-
        x = p.point.x + Decimal(0.1)
        assert len(boundary_plus.formula_y(x)) == 2
        assert len(boundary_minus.formula_y(x)) == 0

    def test_formula_y_normal_boundary(self):
        """Test point formula with 2 positive fixed sites."""
        p = WeightedSite(Decimal(14), Decimal(26), Decimal(7))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)

        # In the middle.
        x = 14

        ys_in_boundary = boundary_plus.formula_y(x)
        assert len(ys_in_boundary) == 0

        ys_in_boundary = boundary_minus.formula_y(x)
        assert len(ys_in_boundary) == 1
        assert are_close(ys_in_boundary[0], Decimal("33"), Decimal("0.000000001"))

        # To the right.
        x = 20

        ys_in_boundary = boundary_plus.formula_y(x)
        assert len(ys_in_boundary) == 1
        assert are_close(
            ys_in_boundary[0],
            Decimal("36.08634652366914366118554424"),
            Decimal("0.000000001"),
        )

        ys_in_boundary = boundary_minus.formula_y(x)
        assert len(ys_in_boundary) == 0

        # To the left.
        x = 10

        ys_in_boundary = boundary_plus.formula_y(x)
        assert len(ys_in_boundary) == 0

        ys_in_boundary = boundary_minus.formula_y(x)
        assert len(ys_in_boundary) == 1
        assert are_close(
            ys_in_boundary[0],
            Decimal("34.26816470548732547936736242"),
            Decimal("0.000000001"),
        )

    def test_formula_y_stopped_boundary(self):
        """Test point formula with 2 positive fixed sites."""
        p = WeightedSite(Decimal(30), Decimal(14), Decimal(6))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        bisector = WeightedPointBisector(sites=(p, q))
        boundary_plus = WeightedPointBoundary(bisector=bisector, sign=True)
        boundary_minus = WeightedPointBoundary(bisector=bisector, sign=False)

        # In the middle.
        x = 30

        ys_in_boundary = boundary_plus.formula_y(x)
        assert len(ys_in_boundary) == 0

        ys_in_boundary = boundary_minus.formula_y(x)
        assert len(ys_in_boundary) == 1
        assert are_close(ys_in_boundary[0], Decimal("20"), Decimal(0))

        # To the right.
        x = 55

        ys_in_boundary = boundary_plus.formula_y(x)
        assert len(ys_in_boundary) == 1
        assert are_close(
            ys_in_boundary[0], Decimal("25.58035714285714266444389536"), Decimal(0)
        )

        ys_in_boundary = boundary_minus.formula_y(x)
        assert len(ys_in_boundary) == 0

        # To the left.
        x = 26

        ys_in_boundary = boundary_plus.formula_y(x)
        assert len(ys_in_boundary) == 0

        ys_in_boundary = boundary_minus.formula_y(x)
        assert len(ys_in_boundary) == 1
        assert are_close(
            ys_in_boundary[0], Decimal("21.52380952380952402392614375"), Decimal(0)
        )
