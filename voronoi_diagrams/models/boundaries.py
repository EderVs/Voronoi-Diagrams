"""Boundary representation."""

# Standard Library
from typing import Callable, Optional, Any, Tuple, List
from abc import ABCMeta, abstractmethod

# Models
from .points import Point
from .bisectors import Bisector, PointBisector
from .events import IntersectionEvent

# Math
from decimal import Decimal


class Boundary:
    """Bisector that is * mapped."""

    __metaclass__ = ABCMeta

    bisector: Bisector
    sign: bool
    left_intersection: Optional[IntersectionEvent]
    right_intersection: Optional[IntersectionEvent]

    def __init__(
        self, bisector: Bisector, sign: bool,
    ):
        """Construct Boundary."""
        self.bisector = bisector
        self.sign = sign
        self.left_intersection = None
        self.right_intersection = None

    def get_site(self):
        site1 = self.bisector.sites[0]
        site2 = self.bisector.sites[1]
        if (site1.point.y > site2.point.y) or (
            site1.point.y == site2.point.y and site1.point.x >= site2.point.x
        ):
            return site1
        else:
            return site2

    @abstractmethod
    def star(self, point: Point) -> Point:
        """Map a bisector."""
        raise NotImplementedError

    def get_point_comparison(self, point: Point) -> Optional[Decimal]:
        """Get the y comparison of a point based on the line y coordinate of the point.

        Return 0 if the point is in the boundary based on l.
        Return > 0 if the point is to the right of the boundary based on l.
        Return < 0 if the point is to the left of the boundary based on l.
        """
        p1, q1 = (site.point for site in self.bisector.sites)
        if p1.y == q1.y:
            return None
        x = self.formula_x(point.y)
        if x is not None:
            return point.x - x
        else:
            return point.x - self.get_site().point.x

    @abstractmethod
    def formula_x(self, y: Decimal) -> Optional[Decimal]:
        """Return the x coordinate given the y coordinate.

        This is the the formula of the bisector mapped with the star map.
        """
        raise NotImplementedError

    def formula_y(self, x: Decimal) -> Decimal:
        """Return the y coordinate given the x coordinate.

        This is the the formula of the bisector mapped with the star map.
        This function uses the star function because it is defined given the x coordinate.
        """
        point = self.star(Point(x, self.bisector.formula_y(x)))
        return point.y

    def __str__(self):
        """Get boundary string representation."""
        return f"Boundary({self.bisector}, {self.sign})"

    def __repr__(self):
        """Get boundary representation."""
        return self.__str__()

    @abstractmethod
    def distance_to_site(self, point: Point) -> Decimal:
        """Get distance to any of the sites because it is a boundary."""
        raise NotImplementedError

    def get_intersections(self, boundary: Any) -> List[Tuple[Point, Point]]:
        """Get intersections between two boundaries."""
        site_self = self.get_site()
        site_boundary = boundary.get_site()
        is_intersection_possible = True
        if (
            (
                site_self.point.x < site_boundary.point.x
                and (not self.sign and boundary.sign)
            )
            or (
                site_self.point.x > site_boundary.point.x
                and (self.sign and not boundary.sign)
            )
            or (
                site_self.point.x == site_boundary.point.x
                and (site_self.point.y == site_boundary.point.y)
            )
            or (self.bisector.is_same_slope(boundary.bisector))
        ):
            is_intersection_possible = False

        all_intersections = []
        if is_intersection_possible:
            intersection_points = self.bisector.get_intersection_points(
                boundary.bisector
            )
            for intersection_point in intersection_points:
                intersection_point_star = self.star(intersection_point)
                if self.is_boundary_below(
                    intersection_point_star
                ) and boundary.is_boundary_below(intersection_point_star):
                    all_intersections.append(
                        (intersection_point, intersection_point_star)
                    )
        return all_intersections

    def is_boundary_below(self, point: Point) -> bool:
        """Get if the given point is up the boundary."""
        is_up_minus_sign = not self.sign and self.get_site().point.x >= point.x
        is_up_plus_sign = self.sign and self.get_site().point.x <= point.x
        return is_up_minus_sign or is_up_plus_sign


class PointBoundary(Boundary):
    """Boundary of a site point."""

    def __init__(self, bisector: PointBisector, sign: bool):
        """Construct Boundary of a site point."""
        super(PointBoundary, self).__init__(bisector, sign)

    # Used in star
    def distance_to_site(self, point: Point) -> Decimal:
        """Get distance to any of the sites because it is a boundary."""
        p = self.bisector.sites[0].point
        return Decimal((p.x - point.x) ** 2 + (p.y - point.y) ** 2).sqrt()

    def star(self, point: Point) -> Point:
        """Map a bisector."""
        return Point(point.x, point.y + self.distance_to_site(point))

    # Used in formula_x
    def quadratic_solution(
        self, a: Decimal, b: Decimal, c: Decimal
    ) -> Optional[Decimal]:
        """Return the solution of the quadratic function based on the sign of the Boundary."""
        if (b ** 2 - 4 * a * c) < 0:
            return None
        if self.sign:
            sign_value = 1
        else:
            sign_value = -1
        solution = (-b + (-sign_value) * Decimal(b ** 2 - 4 * a * c).sqrt()) / 2 * a
        return solution

    def formula_x(self, y: Decimal) -> Optional[Decimal]:
        """Return the x coordinate given the y coordinate.

        This is the the formula of the bisector mapped with the star map.
        In this case is an hiperbola.
        """
        p = self.bisector.sites[0].point
        q = self.bisector.sites[1].point
        a = Decimal(-((q.x - p.x) / (q.y - p.y)))
        b = Decimal((q.x ** 2 - p.x ** 2 + q.y ** 2 - p.y ** 2) / (2 * (q.y - p.y)))
        c = Decimal(-b + y)
        d = Decimal(b - p.y)
        e = Decimal(c ** 2 - d ** 2 - p.x ** 2)
        f = Decimal(-1)
        g = Decimal(2 * (-a * (c + d) + p.x))
        x = self.quadratic_solution(f, g, e)
        return x


class WeightedPointBoundary(Boundary):
    """Boundary of a weighted site point."""

    # TODO: Complete class

    def __init__(self, bisector: PointBisector, sign: bool):
        """Construct Boundary of a site point."""
        super(WeightedPointBoundary, self).__init__(bisector, sign)

    # Used in star
    def distance_to_site(self, point: Point) -> Decimal:
        """Get distance to any of the sites because it is a boundary."""
        p = self.bisector.sites[0].point
        return Decimal((p.x - point.x) ** 2 + (p.y - point.y) ** 2).sqrt()

    def star(self, point: Point) -> Point:
        """Map a bisector."""
        return Point(point.x, point.y + self.distance_to_site(point))

    # Used in formula_x
    def quadratic_solution(
        self, a: Decimal, b: Decimal, c: Decimal
    ) -> Optional[Decimal]:
        """Return the solution of the quadratic function based on the sign of the Boundary."""
        if (b ** 2 - 4 * a * c) < 0:
            return None
        if self.sign:
            sign_value = 1
        else:
            sign_value = -1
        solution = (-b + (-sign_value) * Decimal(b ** 2 - 4 * a * c).sqrt()) / 2 * a
        return solution

    def formula_x(self, y: Decimal) -> Optional[Decimal]:
        """Return the x coordinate given the y coordinate.

        This is the the formula of the bisector mapped with the star map.
        In this case is an hiperbola.
        """
        p = self.bisector.sites[0].point
        q = self.bisector.sites[1].point
        a = -((q.x - p.x) / (q.y - p.y))
        b = Decimal((q.x ** 2 - p.x ** 2 + q.y ** 2 - p.y ** 2) / (2 * (q.y - p.y)))
        c = Decimal(-b + y)
        d = Decimal(b - p.y)
        e = Decimal(c ** 2 - d ** 2 - p.x ** 2)
        f = Decimal(-1)
        g = Decimal(2 * (-a * (c + d) + p.x))
        x = self.quadratic_solution(f, g, e)
        return x
