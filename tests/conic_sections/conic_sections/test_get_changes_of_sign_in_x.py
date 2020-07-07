"""Test get_changes_of_sign_in_x method."""

from conic_sections.models import ConicSection
from voronoi_diagrams.models import WeightedPointBisector, WeightedSite

# Math
from decimal import Decimal

# General Utils
from general_utils.numbers import are_close


class TestGetChangesOfSignInX:
    """Test get_changes_of_sign_in_x method."""

    def test_there_is_solution(self):
        """Test where there is solution."""
        p = WeightedSite(Decimal(15), Decimal(-5), Decimal(7))
        q = WeightedSite(Decimal(-7.6), Decimal(-2.27), Decimal(2))
        bisector = WeightedPointBisector(sites=(p, q))
        epsilon = Decimal(0.00001)
        conic_section = bisector.conic_section
        xs = conic_section.get_changes_of_sign_in_x()
        xs.sort()
        expected_xs = [
            Decimal("5.794462938320943834469289868138730525970458984375"),
            Decimal("1.6055370616790567428466829369426704943180084228515625"),
        ]
        expected_xs.sort()
        assert len(expected_xs) == len(xs)
        for i in range(len(expected_xs)):
            assert are_close(expected_xs[i], xs[i], epsilon)

        p = WeightedSite(Decimal(15), Decimal(-5), Decimal(7))
        q = WeightedSite(Decimal(-6), Decimal(-5), Decimal(2))
        bisector = WeightedPointBisector(sites=(p, q))
        epsilon = Decimal(0.00001)
        conic_section = bisector.conic_section
        xs = conic_section.get_changes_of_sign_in_x()
        xs.sort()
        expected_xs = [
            Decimal("2"),
            Decimal("7"),
        ]
        expected_xs.sort()
        assert len(expected_xs) == len(xs)
        for i in range(len(expected_xs)):
            assert are_close(expected_xs[i], xs[i], epsilon)

    def test_there_is_no_solution(self):
        """Test where there is solution."""
        p = WeightedSite(Decimal(3), Decimal(-7), Decimal(7))
        q = WeightedSite(Decimal(3), Decimal(4), Decimal(2))
        bisector = WeightedPointBisector(sites=(p, q))
        conic_section = bisector.conic_section
        xs = conic_section.get_changes_of_sign_in_x()
        assert len(xs) == 0
