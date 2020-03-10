"""Bisector representation."""

# Standard Library
from typing import Callable, Tuple

# Models
from . import Point


class Bisector:
    """Bisector representation.

    It has its formula(function) associated.
    """

    sites: Tuple[Point, Point]

    def __init__(self, sites: Tuple[Point, Point]):
        """Construct bisector."""
        self.sites = sites

    def formula(self, y: float) -> float:
        """Receive the y coordinate and return the x coordinate of the bisector."""
        raise NotImplementedError


class PointBisector(Bisector):
    """Bisector defined by point sites."""

    def __init__(self, sites: Tuple[Point, Point]):
        """Construct bisector of Point sites Bisector."""
        super(PointBisector, self).__init__(sites)

    def formula(self, y: float) -> float:
        """Bisector formula of point sites."""
        p = self.sites[0]
        q = self.sites[1]
        a = (2*q.y - 2*p.y)*y + (p.y**2 - q.y**2) - (q.x**2 - p.x**2)
        b = 2*p.x - 2*q.x
        return a / b
