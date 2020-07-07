"""Test frontier methods in WeightedSite."""

# Math
from decimal import Decimal

# Models
from voronoi_diagrams.models import WeightedSite, Point

# General Utils
from general_utils.numbers import are_close


class TestGetFrontierPointingToPoint:
    """Test x and y formula of the frontier."""

    def test_up_right(self):
        """Test in the up right corner."""
        p = WeightedSite(Decimal(1), Decimal(1), Decimal(2).sqrt())
        point = Point(Decimal(3), Decimal(3))

        x = p.get_x_frontier_pointing_to_point(point)
        y = p.get_y_frontier_pointing_to_point(point)
        epsilon = Decimal(0.00001)
        assert are_close(x, Decimal(2), epsilon)
        assert are_close(y, Decimal(2), epsilon)

    def test_up_left(self):
        """Test in the up left corner."""
        p = WeightedSite(Decimal(1), Decimal(1), Decimal(2).sqrt())
        point = Point(Decimal(-1), Decimal(3))

        x = p.get_x_frontier_pointing_to_point(point)
        y = p.get_y_frontier_pointing_to_point(point)
        epsilon = Decimal(0.00001)
        assert are_close(x, Decimal(0), epsilon)
        assert are_close(y, Decimal(2), epsilon)

    def test_down_right(self):
        """Test in the down right corner."""
        p = WeightedSite(Decimal(1), Decimal(1), Decimal(2).sqrt())
        point = Point(Decimal(3), Decimal(-1))

        x = p.get_x_frontier_pointing_to_point(point)
        y = p.get_y_frontier_pointing_to_point(point)
        epsilon = Decimal(0.00001)
        assert are_close(x, Decimal(2), epsilon)
        assert are_close(y, Decimal(0), epsilon)

    def test_down_left(self):
        """Test in the down left corner."""
        p = WeightedSite(Decimal(1), Decimal(1), Decimal(2).sqrt())
        point = Point(Decimal(-1), Decimal(-1))

        x = p.get_x_frontier_pointing_to_point(point)
        y = p.get_y_frontier_pointing_to_point(point)
        epsilon = Decimal(0.00001)
        assert are_close(x, Decimal(0), epsilon)
        assert are_close(y, Decimal(0), epsilon)

    def test_right(self):
        """Test in the down left corner."""
        p = WeightedSite(Decimal(1), Decimal(1), Decimal(1))
        point = Point(Decimal(3), Decimal(1))

        x = p.get_x_frontier_pointing_to_point(point)
        y = p.get_y_frontier_pointing_to_point(point)
        epsilon = Decimal(0.00001)
        assert are_close(x, Decimal(2), epsilon)
        assert are_close(y, Decimal(1), epsilon)

    def test_left(self):
        """Test in the down left corner."""
        p = WeightedSite(Decimal(1), Decimal(1), Decimal(1))
        point = Point(Decimal(-1), Decimal(1))

        x = p.get_x_frontier_pointing_to_point(point)
        y = p.get_y_frontier_pointing_to_point(point)
        epsilon = Decimal(0.00001)
        assert are_close(x, Decimal(0), epsilon)
        assert are_close(y, Decimal(1), epsilon)

    def test_up(self):
        """Test in the down left corner."""
        p = WeightedSite(Decimal(1), Decimal(1), Decimal(1))
        point = Point(Decimal(1), Decimal(3))

        x = p.get_x_frontier_pointing_to_point(point)
        y = p.get_y_frontier_pointing_to_point(point)
        epsilon = Decimal(0.00001)
        assert are_close(x, Decimal(1), epsilon)
        assert are_close(y, Decimal(2), epsilon)

    def test_down(self):
        """Test in the down left corner."""
        p = WeightedSite(Decimal(1), Decimal(1), Decimal(1))
        point = Point(Decimal(1), Decimal(-1))

        x = p.get_x_frontier_pointing_to_point(point)
        y = p.get_y_frontier_pointing_to_point(point)
        epsilon = Decimal(0.00001)
        assert are_close(x, Decimal(1), epsilon)
        assert are_close(y, Decimal(0), epsilon)


class TestGetFrontier:
    """Test get frontier point given a coordinate."""

    def test_right_middle(self):
        """Test in the up right corner."""
        p = WeightedSite(Decimal(0), Decimal(0), Decimal(2).sqrt())
        fx = Decimal(1)
        fy = Decimal(1)

        x1, x2 = p.get_x_frontier_formula(fy)
        y1, y2 = p.get_y_frontier_formula(fx)
        epsilon = Decimal(0.00001)
        assert are_close(x1, fx, epsilon)
        assert are_close(x2, -fx, epsilon)
        assert are_close(y1, fy, epsilon)
        assert are_close(y2, -fy, epsilon)

    def test_left_middle(self):
        """Test in the up left corner."""
        p = WeightedSite(Decimal(0), Decimal(0), Decimal(2).sqrt())
        fx = Decimal(-1)
        fy = Decimal(1)

        x1, x2 = p.get_x_frontier_formula(fy)
        y1, y2 = p.get_y_frontier_formula(fx)
        epsilon = Decimal(0.00001)
        assert are_close(x1, -fx, epsilon)
        assert are_close(x2, fx, epsilon)
        assert are_close(y1, fy, epsilon)
        assert are_close(y2, -fy, epsilon)

    def test_right_one(self):
        """Test in the down left corner."""
        p = WeightedSite(Decimal(0), Decimal(0), Decimal(1))
        fx = Decimal(1)
        fy = Decimal(0)

        x1, x2 = p.get_x_frontier_formula(fy)
        y1, y2 = p.get_y_frontier_formula(fx)
        epsilon = Decimal(0.00001)
        assert are_close(x1, fx, epsilon)
        assert are_close(x2, -fx, epsilon)
        assert are_close(y1, fy, epsilon)
        assert are_close(y2, -fy, epsilon)

    def test_sides(self):
        """Test in the down left corner."""
        p = WeightedSite(Decimal(0), Decimal(0), Decimal(1))
        fx = Decimal(-1)
        fy = Decimal(0)

        x1, x2 = p.get_x_frontier_formula(fy)
        y1, y2 = p.get_y_frontier_formula(fx)
        epsilon = Decimal(0.00001)
        assert are_close(x1, -fx, epsilon)
        assert are_close(x2, fx, epsilon)
        assert are_close(y1, fy, epsilon)
        assert are_close(y2, fy, epsilon)

    def test_middle(self):
        """Test in the down left corner."""
        p = WeightedSite(Decimal(0), Decimal(0), Decimal(1))
        fx = Decimal(0)
        fy = Decimal(-1)

        x1, x2 = p.get_x_frontier_formula(fy)
        y1, y2 = p.get_y_frontier_formula(fx)
        epsilon = Decimal(0.00001)
        assert are_close(x1, fx, epsilon)
        assert are_close(x2, fx, epsilon)
        assert are_close(y1, -fy, epsilon)
        assert are_close(y2, fy, epsilon)

    def test_not_in_limit(self):
        """Test in the down left corner."""
        p = WeightedSite(Decimal(0), Decimal(0), Decimal(1))
        fx = Decimal(2)
        fy = Decimal(2)

        result_x = p.get_x_frontier_formula(fy)
        result_y = p.get_y_frontier_formula(fx)
        assert result_x is None
        assert result_y is None
