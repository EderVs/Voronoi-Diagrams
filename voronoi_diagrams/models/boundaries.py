"""Boundary representation."""

# Standard Library
from typing import Callable, Optional, Any, Tuple, List
from abc import ABCMeta, abstractmethod

# Models
from .points import Point
from .bisectors import Bisector, PointBisector, WeightedPointBisector
from .events import IntersectionEvent

# Math
from decimal import Decimal

# Generaal utils
from general_utils.numbers import are_close


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
        """Get the site that is highest or more to the right.

        This is the site that defines the region of the 2 boundary sibling.
        """
        site1 = self.bisector.sites[0]
        site2 = self.bisector.sites[1]
        if (site1.get_highest_site_point().y > site2.get_highest_site_point().y) or (
            site1.get_highest_site_point().y == site2.get_highest_site_point().y
            and site1.get_rightest_site_point().x >= site2.get_rightest_site_point().x
        ):
            return site1
        else:
            return site2

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

    def formula_y(self, x: Decimal) -> List[Decimal]:
        """Return the y coordinate given the x coordinate.

        This is the the formula of the bisector mapped with the star map.
        This can also be viewed as the projection of x in the boundary.
        """
        ys = [
            self.star(Point(x, y_bisector)).y
            for y_bisector in self.bisector.formula_y(x)
        ]
        return ys

    def __str__(self):
        """Get boundary string representation."""
        return f"Boundary({self.bisector}, {self.sign})"

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

    @abstractmethod
    def is_boundary_below(self, point: Point) -> bool:
        """Get if the given point is above the boundary."""
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
        x = self.quadratic_solution(f, g, e)
        return [x]

    def is_boundary_below(self, point: Point) -> bool:
        """Get if the given point is up the boundary."""
        is_up_minus_sign = not self.sign and self.get_site().point.x >= point.x
        is_up_plus_sign = self.sign and self.get_site().point.x <= point.x
        return is_up_minus_sign or is_up_plus_sign


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
        return p.get_distance_to_site_farthest_frontier_from_point(point.x, point.y)

    def is_boundary_concave_to_y(self) -> bool:
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
        """Return the y coordinate given the x coordinate.

        This is the the formula of the bisector mapped with the star map.
        """
        # It has at most 2 values.
        ys_in_all_boundary = super(WeightedPointBoundary, self).formula_y(x)
        if len(ys_in_all_boundary) == 0:
            return []
        to_return = []
        if self.is_boundary_concave_to_y():
            to_return.append(max(ys_in_all_boundary))
        if (not self.sign and x <= self.get_site().point.x) or (
            self.sign and self.get_site().point.x <= x
        ):
            to_return.append(min(ys_in_all_boundary))

        return to_return

    def is_point_in_boundary(self, point) -> bool:
        """Check if the point is in this boundary."""
        ys_in_boundary = self.formula_y(point.x)
        for y_in_boundary in ys_in_boundary:
            if are_close(y_in_boundary, point.y, Decimal("0.0000001")):
                if self.is_boundary_concave_to_y() and y_in_boundary == max(
                    ys_in_boundary
                ):
                    return True
                if not self.sign:
                    return point.x <= self.get_site().point.x
                else:
                    return self.get_site().point.x <= point.x

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
        site = self.get_site()
        if self._is_point_in_all_region(point):
            # The point is in the boundary or inside.
            if self.is_point_in_boundary(point):
                # In the boundary.
                return 0
            # The point is inside.
            if self.sign:
                # It's left to Boundary+.
                return -1
            else:
                # It's right to Boundary-.
                return 1

        # The point is outside of all the region.
        ys_in_all_boundary = super(WeightedPointBoundary, self).formula_y(point.x)
        if len(ys_in_all_boundary) > 1 and max(ys_in_all_boundary) < point.y:
            # The projection to the boundary is below. This is only possible when one of the
            # boundaries concave to y.
            if self.is_boundary_concave_to_y():
                if self.sign:
                    return 1
                else:
                    return -1
            else:
                # The sibling Boundary is the one that is concave to y.
                if self.sign:
                    return -1
                else:
                    return 1

        # The point doesn't have a x projection in the boundary or the projection is above the
        # point.
        if point.x < site.point.x:
            # It's left to the site that defines the region.
            return -1
        else:
            # It's right to the site that defines the region.
            return 1

    def _is_point_in_all_region(self, point: Point) -> bool:
        """Return True if the given point is in the region where the boundary is described."""
        # Get the projection of x in the boundary.
        ys_in_boundary = super(WeightedPointBoundary, self).formula_y(point.x)
        if len(ys_in_boundary) == 0:
            # There is no point in boundary to compare
            return False
        elif len(ys_in_boundary) == 1:
            # First we check that the projection in the boundary is where there is a change of sign
            # of the whole boundary function.
            changes_of_sign_in_x = self.bisector.get_changes_of_sign_in_x()
            for change_of_sign_in_x in changes_of_sign_in_x:
                if are_close(change_of_sign_in_x, point.x, Decimal(0.0000001)):
                    return are_close(
                        super(WeightedPointBoundary, self).formula_y(
                            change_of_sign_in_x
                        )[0],
                        point.y,
                        Decimal(0.0000001),
                    )
            else:
                # If the the projection in the boundary is not a change of sign then we just check
                # that the projection is below the point.
                y_in_boundary = ys_in_boundary[0]
                return y_in_boundary <= point.y
        elif len(ys_in_boundary) == 2:
            # there are two projection in the boundary then we one must be in above and the other
            # below.
            y_in_boundary_max = max(ys_in_boundary)
            y_in_boundary_min = min(ys_in_boundary)
            return y_in_boundary_max >= point.y and y_in_boundary_min <= point.y

        return False

    def get_intersections(self, boundary: Any) -> List[Tuple[Point, Point]]:
        """Get intersections between two WeightePointBoundaries."""
        all_intersections = []
        # bisector.get_intersection_points gives us the intersections in the bisectors.
        intersection_points = self.bisector.get_intersection_points(boundary.bisector)
        # Now we need to look that each mapped intersection point is in the boundary.
        for intersection_point in intersection_points:
            intersection_point_star = self.star(intersection_point)
            if self.is_point_in_boundary(
                intersection_point_star
            ) and boundary.is_point_in_boundary(intersection_point_star):
                all_intersections.append((intersection_point, intersection_point_star))
        return all_intersections
