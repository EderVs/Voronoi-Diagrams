"""Boundary representation."""

# Standard Library
from typing import Callable, Optional, Any, Tuple, List
from abc import ABCMeta, abstractmethod

# Models
from .points import Point
from .bisectors import Bisector, PointBisector, WeightedPointBisector
from .events import Intersection, Site

# Math
from decimal import Decimal

# Generaal utils
from general_utils.numbers import are_close


class Boundary:
    """Bisector that is * mapped."""

    __metaclass__ = ABCMeta

    bisector: Bisector
    sign: bool
    left_intersection: Optional[Intersection]
    right_intersection: Optional[Intersection]
    # active says if this boundary is the current added to the LList.
    active: bool
    is_to_be_deleted: bool

    def __init__(self, bisector: Bisector, sign: bool, active: bool = False):
        """Construct Boundary."""
        self.bisector = bisector
        self.sign = sign
        self.left_intersection = None
        self.right_intersection = None
        self.active = active
        self.is_to_be_deleted = False

    def get_site(self) -> Site:
        """Get the site that is highest or more to the right.

        This is the site that defines the region of the 2 boundary sibling.
        """
        return self.bisector.get_site()

    def star(self, point: Point) -> Point:
        """Map a bisector to build the region to work in."""
        return Point(point.x, point.y + self.distance_to_site(point))

    @abstractmethod
    def get_point_comparison(self, point: Point) -> Optional[Decimal]:
        """Get the y comparison of a point based on the line y coordinate of the point.

        This comparison is based on this boundary with its sign.
        Return 0 if the point is in the boundary based on l.
        Return > 0 if the point is to the right of the boundary based on l.
        Return < 0 if the point is to the left of the boundary based on l.
        """
        raise NotImplementedError

    def formula_x(self, y: Decimal) -> List[Decimal]:
        """Return the x coordinate of the boundary given the y coordinate.

        This method is not implemented in all Boundaries.
        """
        raise NotImplementedError

    def formula_y_without_sign(self, x: Decimal) -> List[Decimal]:
        """Return the y coordinates in all the boundary given the x coordinate.

        This is the the formula of the bisector mapped with the star map.
        This can also be viewed as the projection of x in all the boundary without
        taking care of the sign.
        """
        ys = [
            self.star(Point(x, y_bisector)).y
            for y_bisector in self.bisector.formula_y(x)
        ]
        return ys

    def formula_y(self, x: Decimal) -> List[Decimal]:
        """Return the y coordinate given the x coordinate taking care of the sign.

        This is the the formula of the bisector mapped with the star map.
        This can also be viewed as the projection of x in the boundary taking care of
        the sign.
        """
        raise NotImplementedError

    def __str__(self):
        """Get boundary string representation."""
        if self.sign:
            sign_str = "+"
        else:
            sign_str = "-"
        return f"B*{sign_str}{self.bisector.get_sites_names()}"

    def __repr__(self):
        """Get boundary representation."""
        return self.__str__()

    @abstractmethod
    def distance_to_site(self, point: Point) -> Decimal:
        """Get distance to any of the sites.

        This method is used in star.
        The distance will be taken to to the site given in get_site because the distance to any of
        the sites is the same.
        """
        raise NotImplementedError

    @abstractmethod
    def get_intersections(self, boundary: Any) -> List[Tuple[Point, Point]]:
        """Get intersections between two boundaries.

        The return values are is a list of the intersection without the star map (the
        bisectors of the boundaries intersections) and the intersection with the star map (the
        boundaries intersection).
        """
        raise NotImplementedError

    def get_side_where_point_belongs(self, point: Point) -> int:
        """Get where point belongs."""
        raise NotImplementedError


class PointBoundary(Boundary):
    """Boundary of a site point."""

    def __init__(self, bisector: PointBisector, sign: bool):
        """Construct Boundary of a site point."""
        super(PointBoundary, self).__init__(bisector, sign)

    def get_point_comparison(self, point) -> Optional[Decimal]:
        """Get the y comparison of a point based on the line y coordinate of the point.

        This comparison is based on this boundary with its sign.
        Return 0 if the point is in the boundary based on y coordinate of the point.
        Return > 0 if the point is to the right of the boundary based on the y coordinate of the
        point.
        Return < 0 if the point is to the left of the boundary based on the y coordinate of the
        point.
        """
        p1, q1 = (site.point for site in self.bisector.sites)
        if p1.y == q1.y:
            return None
        x = self.formula_x(point.y)[0]
        if x is not None:
            return point.x - x
        else:
            return point.x - self.get_site().point.x

    def distance_to_site(self, point: Point) -> Decimal:
        """Get distance to any of the sites.

        This method is used in star.
        The distance will be taken to to the site given in get_site because the distance to any of
        the sites is the same.
        """
        p = self.get_site()
        return p.get_distance_to_site_point_from_point(point.x, point.y)

    # Used in formula_x
    def _quadratic_solution(
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

    def formula_x(self, y: Decimal) -> List[Decimal]:
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
        x = self._quadratic_solution(f, g, e)
        return [x]

    def formula_y(self, x: Decimal) -> List[Decimal]:
        """Return the y coordinate given the x coordinate, taking care of the sign.

        This is the the formula of the bisector mapped with the star map.
        This can also be viewed as the projection of x in the boundary taking care of
        the sign.
        """
        if (not self.sign and x <= self.get_site().point.x) or (
            self.sign and x > self.get_site().point.x
        ):
            return self.formula_y_without_sign(x)
        return []

    def is_boundary_below(self, point: Point) -> bool:
        """Get if the given point is up the boundary."""
        is_up_minus_sign = not self.sign and self.get_site().point.x >= point.x
        is_up_plus_sign = self.sign and self.get_site().point.x <= point.x
        return is_up_minus_sign or is_up_plus_sign

    def get_intersections(self, boundary: Any) -> List[Tuple[Point, Point]]:
        """Get intersections between two boundaries.

        The return values are is a list of the intersection without the star map (the
        bisectors of the boundaries intersections) and the intersection with the star map (the
        boundaries intersection).
        """
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
            intersection_points = self.bisector.get_intersections(boundary.bisector)
            for intersection_point in intersection_points:
                intersection_point_star = self.star(intersection_point)
                if self.is_boundary_below(
                    intersection_point_star
                ) and boundary.is_boundary_below(intersection_point_star):
                    all_intersections.append(
                        (intersection_point, intersection_point_star)
                    )
        return all_intersections

    def get_side_where_point_belongs(self, point: Point) -> int:
        """Get where point belongs."""
        return 0


class WeightedPointBoundary(Boundary):
    """Boundary of a weighted site point."""

    def __init__(self, bisector: WeightedPointBisector, sign: bool):
        """Construct Boundary of a site point."""
        super(WeightedPointBoundary, self).__init__(bisector, sign)

    def distance_to_site(self, point: Point) -> Decimal:
        """Get distance to any of the sites.

        This method is used in star.
        The distance will be taken to to the site given in get_site because the distance to any of
        the sites is the same.
        """
        p = self.get_site()
        return p.get_weighted_distance(point.x, point.y)

    def is_boundary_not_x_monotone(self) -> bool:
        """Check if the boundary is concave to y."""
        sites = self.bisector.sites
        if sites[0] == self.get_site():
            max_site = sites[0]
            min_site = sites[1]
        else:
            max_site = sites[1]
            min_site = sites[0]
        if max_site.get_lowest_site_point().y < min_site.get_lowest_site_point().y:
            if max_site.point.x < min_site.point.x:
                return self.sign
            else:
                return not self.sign
        else:
            return False

    def formula_y(self, x: Decimal) -> List[Decimal]:
        """Return the y coordinate given the x coordinate taking care of the sign.

        This is the formula of the bisector mapped with the star map.
        """
        # It has at most 2 values.
        ys_without_sign = self.formula_y_without_sign(x)
        if len(ys_without_sign) == 0:
            return []
        to_return = []

        # Check when events are in the same y.
        p, q = self.bisector.sites
        p_event, q_event = p.get_event_point(), q.get_event_point()
        if p_event.y == q_event.y:
            if p.weight > q.weight:
                bigger, smaller = p, q
            else:
                bigger, smaller = q, p
            if (bigger.point.x > smaller.point.x and not self.sign) or (
                bigger.point.x < smaller.point.x and self.sign
            ):
                return ys_without_sign
            return []

        if self.is_boundary_not_x_monotone():
            to_return.append(max(ys_without_sign))
        if (not self.sign and x <= self.get_site().point.x) or (
            self.sign and self.get_site().point.x < x
        ):
            to_return.append(min(ys_without_sign))

        return to_return

    def is_point_in_boundary(self, point) -> bool:
        """Check if the point is in this boundary."""
        p, q = self.bisector.sites
        if p.point.y == q.point.y and p.weight == q.weight:
            distance = abs(p.point.x - q.point.x)
            mid_x = min(p.point.x, q.point.x) + (distance / Decimal(2))
            return are_close(point.x, mid_x, Decimal("0.0001"),) and not self.sign

        ys_in_boundary = self.formula_y(point.x)
        for y_in_boundary in ys_in_boundary:
            if are_close(y_in_boundary, point.y, Decimal("0.00001")):
                return True
        return False

    def get_point_comparison(self, point) -> Optional[Decimal]:
        """Get the y comparison of a point based on the y coordinate of the point.

        This comparison is based on this boundary with its sign.
        Return 0 if the point is in the boundary based on y coordinate of the point.
        Return > 0 if the point is to the right of the boundary based on the y coordinate of the
        point.
        Return < 0 if the point is to the left of the boundary based on the y coordinate of the
        point.
        """
        p, q = self.bisector.sites
        same_y = p.point.y == q.point.y
        same_weight = p.weight == q.weight
        if same_y and same_weight:
            if self.sign:
                return Decimal(-1)
            else:
                distance = abs(p.point.x - q.point.x)
                return point.x - (min(p.point.x, q.point.x) + (distance / Decimal(2)))

        if self.is_left_to_boundary(point):
            return Decimal(-1)
        if self.is_point_in_boundary(point):
            return Decimal(0)
        return Decimal(1)

    def is_left_to_boundary(self, point: Point) -> bool:
        """Return True if the given point is to the left of the boundary."""
        ys = self.formula_y(point.x)
        if self.is_boundary_not_x_monotone():
            if len(ys) == 0:
                return not self.sign
            if len(ys) == 1:
                if self.sign:
                    return ys[0] > point.y
                else:
                    return ys[0] < point.y
            if len(ys) == 2:
                if self.sign:
                    return max(ys) > point.y and min(ys) < point.y
                else:
                    return max(ys) < point.y or min(ys) > point.y
        else:
            if len(ys) == 0:
                return self.sign
            if self.sign:
                return ys[0] < point.y
            else:
                return ys[0] > point.y

    def get_intersections(self, boundary: Any) -> List[Tuple[Point, Point]]:
        """Get intersections between two WeightePointBoundaries."""
        all_intersections = []
        # bisector.get_intersections gives us the intersections in the bisectors.
        intersection_points = self.bisector.get_intersections(boundary.bisector)
        # Now we need to look that each mapped intersection point is in the boundary.
        for intersection_point in intersection_points:
            intersection_point_star = self.star(intersection_point)
            if self.is_point_in_boundary(
                intersection_point_star
            ) and boundary.is_point_in_boundary(intersection_point_star):
                all_intersections.append((intersection_point, intersection_point_star))
        return all_intersections

    def get_side_where_point_belongs(self, point: Point) -> int:
        """Get where point belongs."""
        if self.is_boundary_not_x_monotone():
            ys = self.formula_y(point.x)
            if are_close(point.y, max(ys), Decimal("0.0001"),):
                return 1
        return 0
