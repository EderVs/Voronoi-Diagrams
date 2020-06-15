"""Bisector representation."""

# Standard Library
from typing import Callable, Tuple, Optional, Any, List
from abc import ABCMeta, abstractmethod

# Models
from .events import Site, WeightedSite
from .points import Point

# Conic Sections
from conic_sections.models import ConicSection

# Math
from decimal import Decimal

# Utils
from general_utils.numbers import are_close


class Bisector:
    """Bisector representation.

    It has its formula(function) associated.
    """

    __metaclass__ = ABCMeta

    sites: Tuple[Site, Site]

    def __init__(self, sites: Tuple[Site, Site]):
        """Construct bisector."""
        if sites[0].point.y < sites[1].point.y or (
            sites[0].point.y == sites[1].point.y
            and sites[0].point.x <= sites[1].point.x
        ):
            sites = (sites[1], sites[0])
        self.sites = sites

    def __eq__(self, bisector: Any) -> bool:
        """Equality between bisectors."""
        return self.sites == bisector.sites

    @abstractmethod
    def formula_x(self, y: Decimal) -> List[Decimal]:
        """Get x coordinate given the y coordinate."""
        raise NotImplementedError

    @abstractmethod
    def formula_y(self, y: Decimal) -> List[Decimal]:
        """Get y coordinate given the x coordinate."""
        raise NotImplementedError

    def __str__(self):
        """Get bisector string representation."""
        return f"Bisector({self.sites[0]}, {self.sites[1]})"

    def __repr__(self):
        """Get Bisector representation."""
        return self.__str__()

    @abstractmethod
    def get_intersection_points(self, bisector: Any) -> List[Point]:
        """Get the point of intersection between two bisectors."""
        raise NotImplementedError

    @abstractmethod
    def is_same_slope(self, bisector: Any) -> bool:
        """Compare if the given bisector slope is the same as the slope of this bisector."""
        raise NotImplementedError

    def get_middle_between_sites(self) -> Point:
        """Get Middle point between sites."""
        site1, site2 = self.sites
        point_x = (
            site1.get_x_frontier_pointing_to_point(site2.point)
            - (
                site1.get_x_frontier_pointing_to_point(site2.point)
                - site2.get_x_frontier_pointing_to_point(site1.point)
            )
            / 2
        )
        point_y = (
            site1.get_y_frontier_pointing_to_point(site2.point)
            - (
                site1.get_y_frontier_pointing_to_point(site2.point)
                - site2.get_y_frontier_pointing_to_point(site1.point)
            )
            / 2
        )
        return Point(point_x, point_y)


class PointBisector(Bisector):
    """Bisector defined by point sites."""

    def __init__(self, sites: Tuple[Site, Site]):
        """Construct bisector of Point sites Bisector."""
        super(PointBisector, self).__init__(sites)

    def formula_x(self, y: Decimal) -> List[Decimal]:
        """Get x coordinate given the y coordinate.

        In this case is a line.
        """
        p = self.sites[0].point
        q = self.sites[1].point
        a = (2 * q.y - 2 * p.y) * y + (p.y ** 2 - q.y ** 2) - (q.x ** 2 - p.x ** 2)
        b = 2 * p.x - 2 * q.x
        return [a / b]

    def formula_y(self, x: Decimal) -> Decimal:
        """Get y coordinate given the x coordinate.

        In this case is a line.
        """
        p = self.sites[0].point
        q = self.sites[1].point
        a = Decimal(-((q.x - p.x) / (q.y - p.y)))
        b = Decimal((q.x ** 2 - p.x ** 2 + q.y ** 2 - p.y ** 2) / (2 * (q.y - p.y)))
        return [a * x + b]

    def get_intersection_points(self, bisector: Bisector) -> List[Point]:
        """Get the point of intersection between two bisectors."""
        # No blank spaces after docstring.
        def f_aux_1(xi: Decimal, xj: Decimal, yi: Decimal, yj: Decimal) -> Decimal:
            """Auxiliar function."""
            return (xj ** 2 - xi ** 2 + yj ** 2 - yi ** 2) / (2 * (yj - yi))

        def f_aux_2(xi: Decimal, xj: Decimal, yi: Decimal, yj: Decimal) -> Decimal:
            """Auxiliar function."""
            return (xj - xi) / (yj - yi)

        def get_x(
            xi: Decimal,
            xj: Decimal,
            xk: Decimal,
            xl: Decimal,
            yi: Decimal,
            yj: Decimal,
            yk: Decimal,
            yl: Decimal,
        ) -> Decimal:
            return (f_aux_1(xk, xl, yk, yl) - f_aux_1(xi, xj, yi, yj)) / (
                f_aux_2(xk, xl, yk, yl) - f_aux_2(xi, xj, yi, yj)
            )

        x1 = self.sites[0].point.x
        x2 = self.sites[1].point.x
        y1 = self.sites[0].point.y
        y2 = self.sites[1].point.y

        x3 = bisector.sites[0].point.x
        x4 = bisector.sites[1].point.x
        y3 = bisector.sites[0].point.y
        y4 = bisector.sites[1].point.y

        if y1 == y2:
            # Case where self is a vertical line.
            x = self.get_middle_between_sites().x
            return [Point(x, bisector.formula_y(x)[0])]
        if y3 == y4:
            # Case where bisector is a vertical line.
            x = bisector.get_middle_between_sites().x
        else:
            x = get_x(x1, x2, x3, x4, y1, y2, y3, y4)
        return [Point(x, self.formula_y(x)[0])]

    def is_same_slope(self, bisector: Any) -> bool:
        """Compare if the given bisector slope is the same as the slope of this bisector."""
        p_1 = self.sites[0].point
        p_2 = self.sites[1].point
        q_1 = bisector.sites[0].point
        q_2 = bisector.sites[1].point
        delta_y_is_zero = p_1.y - p_2.y == 0 and q_1.y - q_2.y == 0
        delta_x_is_zero = p_1.x - p_2.x == 0 and q_1.x - q_2.x == 0
        both_deltas_are_the_same = (
            p_1.y - p_2.y == q_1.y - q_2.y and p_1.x - p_2.x == q_1.x - q_2.x
        )
        return delta_y_is_zero or delta_x_is_zero or both_deltas_are_the_same


class WeightedPointBisector(Bisector):
    """Bisector defined by weighted sites."""

    sites: Tuple[WeightedSite, WeightedSite]
    a: Decimal
    b: Decimal
    c: Decimal
    d: Decimal
    e: Decimal
    conic_section: ConicSection

    def __init__(self, sites: Tuple[WeightedSite, WeightedSite]):
        """Construct bisector of weighted sites Bisector.

        In this case the Sites are WeightedSites.
        """
        super(WeightedPointBisector, self).__init__(sites)
        self._set_polynomial_parameters()
        self.conic_section = ConicSection(
            self.a, self.b, self.c, self.d, self.e, self.f
        )

    def _set_polynomial_parameters(self) -> None:
        """Set parameters of general conic formula.

        Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0
        """
        p = self.sites[0]
        q = self.sites[1]
        px = p.point.x
        py = p.point.y
        pw = p.weight
        qx = q.point.x
        qy = q.point.y
        qw = q.weight
        r = (qx ** 2) + (qy ** 2) - (px ** 2) - (py ** 2) - ((pw - qw) ** 2)
        s = 4 * ((pw - qw) ** 2)
        self.a = s - (((2 * px) - (2 * qx)) ** 2)
        self.b = (-2) * ((2 * px) - (2 * qx)) * ((2 * py) - (2 * qy))
        self.c = s - (((2 * py) - (2 * qy)) ** 2)
        self.d = (-2 * px * s) - (2 * ((2 * px) - (2 * qx)) * r)
        self.e = (-2 * py * s) - (2 * ((2 * py) - (2 * qy)) * r)
        self.f = (s * (px ** 2)) + (s * (py ** 2)) - (r ** 2)

    def _is_point_part_of_bisector(self, x: Decimal, y: Decimal) -> bool:
        """Get if the point is part of bisector.

        The bisector is the open branch towards p where p is the weighted site with more weight.
        The open branch towards p has the equality distance_to_p + w_p = distance_to_q + w_q
        where w_p is the weight of p, q is the smallest site and w_q the weight of q.
        """
        big_site_index = int(self.sites[0].weight < self.sites[1].weight)
        big_site = self.sites[big_site_index]
        small_site = self.sites[big_site_index ^ 1]
        epsilon = Decimal(0.00001)
        return are_close(
            big_site.get_distance_to_site_farthest_frontier_from_point(x, y),
            small_site.get_distance_to_site_farthest_frontier_from_point(x, y),
            epsilon,
        )

    def formula_x(self, y: Decimal) -> List[Decimal]:
        """Get x coordinate given the y coordinate.

        In this case is an hyperbola.
        """
        # One Line.
        def _get_formula_given_sign(y: Decimal, sign: bool) -> Optional[Decimal]:
            sign_one = 1 if sign else -1
            b = self.b * y + self.d
            a = self.a
            c = (self.c * (y ** 2)) + (self.e * y) + (self.f)
            if (b ** 2 - 4 * a * c) < 0:
                return None
            return (-b + (sign_one) * Decimal(b ** 2 - 4 * a * c).sqrt()) / (2 * a)

        return_values = []
        x_plus = _get_formula_given_sign(y, sign=True)
        x_minus = _get_formula_given_sign(y, sign=False)
        if x_plus is not None and self._is_point_part_of_bisector(x_plus, y):
            return_values.append(x_plus)
        if (
            x_minus is not None
            and self._is_point_part_of_bisector(x_minus, y)
            and x_minus not in return_values
        ):
            return_values.append(x_minus)
        return return_values

    def formula_y(self, x: Decimal) -> List[Decimal]:
        """Get y coordinate given the x coordinate.

        In this case is an hyperbola
        """
        # One line
        def _get_formula_given_sign(x: Decimal, sign: bool) -> Optional[Decimal]:
            sign_one = 1 if sign else -1
            b = self.b * x + self.e
            a = self.c
            c = (self.a * (x ** 2)) + (self.d * x) + (self.f)
            if (b ** 2 - 4 * a * c) < 0:
                return None
            return (-b + (sign_one) * Decimal(b ** 2 - 4 * a * c).sqrt()) / (2 * a)

        return_values = []
        y_plus = _get_formula_given_sign(x, sign=True)
        y_minus = _get_formula_given_sign(x, sign=False)
        if y_plus is not None and self._is_point_part_of_bisector(x, y_plus):
            return_values.append(y_plus)
        if (
            y_minus is not None
            and self._is_point_part_of_bisector(x, y_minus)
            and y_minus not in return_values
        ):
            return_values.append(y_minus)
        return return_values

    def get_intersection_points(self, bisector: Any) -> List[Point]:
        """Get the point of intersection between two Weighted Point Bisectors."""
        all_intersections = self.conic_section.get_intersection(bisector.conic_section)
        valid_intersections = []
        epsilon = Decimal("0.0001")
        for x, y in all_intersections:
            if self._is_point_part_of_bisector(
                x, y
            ) and bisector._is_point_part_of_bisector(x, y):
                for valid_intersection in valid_intersections:
                    if are_close(valid_intersection.x, x, epsilon) and are_close(
                        valid_intersection.y, y, epsilon
                    ):
                        break
                else:
                    valid_intersections.append(Point(x, y))
        return valid_intersections

    def is_same_slope(self, bisector: Any) -> bool:
        """Compare if the given bisector slope is the same as the slope of this bisector."""
        # TODO: Complete method.
        raise NotImplementedError
