"""Test get circle formula."""

# Conic Sections
from conic_sections.utils.circle import get_circle_formula_x, get_circle_formula_y

# Math
from decimal import Decimal


class TestGetCircleXFormula:
    """Test get circle formula x."""

    def test_get_circle_formula_inside(self):
        """Test get circle x formula with y inside the range."""
        h = Decimal(0)
        k = Decimal(0)
        r = Decimal(2)
        y = Decimal(0)
        points = get_circle_formula_x(h, k, r, y)
        assert points is not None
        assert points == (Decimal("2"), Decimal("-2"),)
        y = Decimal(1)
        points = get_circle_formula_x(h, k, r, y)
        assert points is not None
        assert points == (
            Decimal("1.732050807568877293527446342"),
            Decimal("-1.732050807568877293527446342"),
        )

    def test_get_circle_formula_frontier(self):
        """Test get circle x formula with y inside the range."""
        h = Decimal(0)
        k = Decimal(0)
        r = Decimal(2)
        y = Decimal(2)
        points = get_circle_formula_x(h, k, r, y)
        assert points is not None
        assert points == (Decimal("0"), Decimal("0"),)


class TestGetCircleYFormula:
    """Test get circle formula y."""

    def test_get_circle_formula_inside(self):
        """Test get circle y formula with x inside the range."""
        h = Decimal(0)
        k = Decimal(0)
        r = Decimal(2)
        x = Decimal(0)
        points = get_circle_formula_y(h, k, r, x)
        assert points is not None
        assert points == (Decimal("2"), Decimal("-2"),)
        x = Decimal(1)
        points = get_circle_formula_y(h, k, r, x)
        assert points is not None
        assert points == (
            Decimal("1.732050807568877293527446342"),
            Decimal("-1.732050807568877293527446342"),
        )

    def test_get_circle_formula_frontier(self):
        """Test get circle x formula with y inside the range."""
        h = Decimal(0)
        k = Decimal(0)
        r = Decimal(2)
        x = Decimal(2)
        points = get_circle_formula_y(h, k, r, x)
        assert points is not None
        assert points == (Decimal("0"), Decimal("0"),)
