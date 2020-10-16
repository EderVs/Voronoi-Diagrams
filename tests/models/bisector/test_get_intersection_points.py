"""Test get bisectors intersection point."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.models import (
    PointBisector,
    Point,
    Site,
    WeightedSite,
    WeightedPointBisector,
)

# Math
from decimal import Decimal

# Utils
from general_utils.numbers import are_close


class TestGetPointBisectorIntersectionPoint:
    """Test formula."""

    def test_two_bisectors(self):
        """Test point formula with 3 positive fixed sites."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        r = Site(Decimal(2), Decimal(-2))
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(p, r))
        intersections = bisector_pq.get_intersections(bisector_pr)
        assert len(intersections) == 1
        intersection = intersections[0]
        assert intersection.x == 2
        assert intersection.y == 0
        intersections2 = bisector_pr.get_intersections(bisector_pq)
        assert len(intersections2) == 1
        intersection2 = intersections2[0]
        assert intersection2.x == 2
        assert intersection2.y == 0


class TestGetWeightedPointBisectorIntersectionPoints:
    """Test formula."""

    def test_one_intersection(self):
        """Test get one intersection."""
        p = WeightedSite(Decimal("-17"), Decimal("-5"), Decimal("7"))
        q = WeightedSite(Decimal("4"), Decimal("-5"), Decimal("0.5"))
        r = WeightedSite(Decimal("5"), Decimal("15"), Decimal("3"))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        intersection_x = Decimal("-11.900690721142641592678046436049044132232666015625")
        intersection_y = Decimal("8.251082711903089118684342994")
        epsilon = Decimal(0.00001)
        intersections = bisector_pq.get_intersections(bisector_qr)
        assert len(intersections) == 1
        intersection = intersections[0]
        assert are_close(intersection.x, intersection_x, epsilon)
        assert are_close(intersection.y, intersection_y, epsilon)
        # Test in both bisectors
        # X
        x_values_pq = bisector_pq.formula_x(intersection_y)
        assert any(
            [are_close(x_value, intersection_x, epsilon) for x_value in x_values_pq]
        )
        x_values_qr = bisector_qr.formula_x(intersection_y)
        assert any(
            [are_close(x_value, intersection_x, epsilon) for x_value in x_values_qr]
        )
        # Y
        y_values_pq = bisector_pq.formula_y(intersection_x)
        assert any(
            [are_close(y_value, intersection_y, epsilon) for y_value in y_values_pq]
        )
        y_values_qr = bisector_qr.formula_y(intersection_x)
        assert any(
            [are_close(y_value, intersection_y, epsilon) for y_value in y_values_qr]
        )

    def test_two_intersections(self):
        """Test get two intersection."""
        p = WeightedSite(Decimal("-17"), Decimal("-5"), Decimal("7"))
        q = WeightedSite(Decimal("4"), Decimal("-5"), Decimal("0.5"))
        r = WeightedSite(Decimal("-44"), Decimal("-5"), Decimal("3"))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        intersection_x1 = Decimal("-22.856457178973670352206681855022907257080078125")
        intersection_x2 = Decimal("-22.856457178973670352206681855022907257080078125")
        intersection_y1 = Decimal("44.24693546822346538098926893")
        intersection_y2 = Decimal("-54.24693546822346538098926893")
        epsilon = Decimal("0.0001")
        intersections = bisector_pq.get_intersections(bisector_qr)
        assert len(intersections) == 2
        first = 0
        for i in range(len(intersections)):
            if are_close(intersections[i].x, intersection_x1, epsilon) and are_close(
                intersections[i].y, intersection_y1, epsilon
            ):
                first = i
                break
        else:
            assert False
        assert are_close(intersections[first ^ 1].x, intersection_x2, epsilon)
        assert are_close(intersections[first ^ 1].y, intersection_y2, epsilon)
        # Test in both bisectors
        # X
        x_values_pq = bisector_pq.formula_x(intersection_y1)
        assert any(
            [are_close(x_value, intersection_x1, epsilon) for x_value in x_values_pq]
        )
        x_values_qr = bisector_qr.formula_x(intersection_y1)
        assert any(
            [are_close(x_value, intersection_x1, epsilon) for x_value in x_values_qr]
        )
        x_values_pq = bisector_pq.formula_x(intersection_y2)
        assert any(
            [are_close(x_value, intersection_x2, epsilon) for x_value in x_values_pq]
        )
        x_values_qr = bisector_qr.formula_x(intersection_y2)
        assert any(
            [are_close(x_value, intersection_x2, epsilon) for x_value in x_values_qr]
        )
        # Y
        y_values_pq = bisector_pq.formula_y(intersection_x1)
        assert any(
            [are_close(y_value, intersection_y1, epsilon) for y_value in y_values_pq]
        )
        y_values_qr = bisector_qr.formula_y(intersection_x1)
        assert any(
            [are_close(y_value, intersection_y1, epsilon) for y_value in y_values_qr]
        )
        y_values_pq = bisector_pq.formula_y(intersection_x2)
        assert any(
            [are_close(y_value, intersection_y2, epsilon) for y_value in y_values_pq]
        )
        y_values_qr = bisector_qr.formula_y(intersection_x2)
        assert any(
            [are_close(y_value, intersection_y2, epsilon) for y_value in y_values_qr]
        )
