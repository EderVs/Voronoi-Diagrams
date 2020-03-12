"""Boundary representation."""

# Standard Library
from typing import Callable
from math import sqrt

# Models
from .point import Point
from .bisector import Bisector, PointBisector


class Boundary:
    """Bisector that is * mapped."""

    bisector: Bisector
    sign: bool

    def __init__(
        self, bisector: Bisector, sign: bool,
    ):
        """Construct Boundary."""
        self.bisector = bisector
        self.sign = sign

    def star(self, point: Point) -> Point:
        """Map a bisector."""
        raise NotImplementedError

    def get_point_comparison(self, point: Point) -> float:
        """Get the y comparison of a point based on the line y coordinate of the point.

        Return 0 if the point is in the boundary based on l.
        Return > 0 if the point is to the right of the boundary based on l.
        Return < 0 if the point is to the left of the boundary based on l.
        """
        return point.x - self.bisector.formula_x(point.y)

    def formula_x(self, y: float) -> float:
        """Return the x coordinate given the y coordinate.

        This is the the formula of the bisector mapped with the star map.
        """
        raise NotImplementedError

    def formula_y(self, x: float) -> float:
        """Return the y coordinate given the x coordinate.

        This is the the formula of the bisector mapped with the star map.
        This function uses the star function because it is defined given the x coordinate.
        """
        point = self.star(Point(x, self.bisector.formula_y(x)))
        return point.y


class PointBoundary(Boundary):
    """Boundary of a site point."""

    def __init__(self, bisector: PointBisector, sign: bool):
        """Construct Boundary of a site point."""
        super(PointBoundary, self).__init__(bisector, sign)

    # Used in star
    def distance_to_site(self, point: Point) -> float:
        """Get distance to any of the sites because it is a boundary."""
        p = self.bisector.sites[0]
        return sqrt((p.x - point.x) ** 2 + (p.y - point.y) ** 2)

    def star(self, point: Point) -> Point:
        """Map a bisector."""
        return Point(point.x, point.y + self.distance_to_site(point))

    # Used in formula_x
    def quadratic_solution(self, a: float, b: float, c: float) -> float:
        """Return the solution of the quadratic function based on the sign of the Boundary."""
        if self.sign:
            sign_value = 1
        else:
            sign_value = -1
        solution = (-b + (-sign_value) * sqrt(b ** 2 - 4 * a * c)) / 2 * a
        return solution

    def formula_x(self, y: float) -> float:
        """Return the x coordinate given the y coordinate.

        This is the the formula of the bisector mapped with the star map.
        In this case is an hiperbola.
        """
        p = self.bisector.sites[0]
        q = self.bisector.sites[1]
        a = -((q.x - p.x) / (q.y - p.y))
        b = (q.x ** 2 - p.x ** 2 + q.y ** 2 - p.y ** 2) / (2 * (q.y - p.y))
        c = -b + y
        d = b - p.y
        e = c ** 2 - d ** 2 - p.x ** 2
        f = -1
        g = 2 * (-a * (c + d) + p.x)
        x = self.quadratic_solution(f, g, e)
        return x
