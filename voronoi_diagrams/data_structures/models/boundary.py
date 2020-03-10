"""Boundary representation."""

# Standard Library
from typing import Callable
from math import sqrt

# Models
from .point import Point
from .bisector import Bisector, PointBisector


class Boundary:
    """Bisector that is * mapped."""

    left: Point
    right: Point
    bisector: Bisector
    sign: bool

    def __init__(
        self,
        left: Point,
        right: Point,
        bisector: Bisector,
        sign: bool,
    ):
        """Construct Boundary."""
        self.left = left
        self.right = right
        self.bisector = bisector
        self.sign = sign

    def star(self, point: Point) -> Point:
        """Map a bisector."""
        raise NotImplementedError


class PointBoundary(Boundary):
    """Boundary of a site point."""

    def __init__(self, left: Point, right: Point, bisector: PointBisector, sign: bool):
        """Construct Boundary of a site point."""
        super(PointBoundary, self).__init__(left, right, bisector, sign)

    def distance_to_site(self, point: Point) -> float:
        """Get distance to any of the sites because it is a boundary."""
        return sqrt((self.left.x - point.x)**2 + (self.left.y - point.y)**2)

    def star(self, point: Point) -> Point:
        """Map a bisector."""
        return Point(point.x, point.y+self.distance_to_site(point))
