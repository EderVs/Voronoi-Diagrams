"""Bisector representation."""

# Standard Library
from typing import Callable, Tuple

# Models
from . import Site, Point


class Bisector:
    """Bisector representation.

    It has its formula(function) associated.
    """

    sites: Tuple[Site, Site]

    def __init__(self, sites: Tuple[Site, Site]):
        """Construct bisector."""
        self.sites = sites

    def formula_x(self, y: float) -> float:
        """Get x coordinate given the y coordinate."""
        raise NotImplementedError

    def formula_y(self, y: float) -> float:
        """Get y coordinate given the x coordinate."""
        raise NotImplementedError

    def __str__(self):
        """Get bisector string representation."""
        return f"Bisector({self.sites[0]}, {self.sites[1]})"

    def __repr__(self):
        """Get Bisector representation."""
        return self.__str__()


class PointBisector(Bisector):
    """Bisector defined by point sites."""

    def __init__(self, sites: Tuple[Point, Point]):
        """Construct bisector of Point sites Bisector."""
        super(PointBisector, self).__init__(sites)

    def formula_x(self, y: float) -> float:
        """Get x coordinate given the y coordinate.

        In this case is a line.
        """
        p = self.sites[0]
        q = self.sites[1]
        a = (2 * q.y - 2 * p.y) * y + (p.y ** 2 - q.y ** 2) - (q.x ** 2 - p.x ** 2)
        b = 2 * p.x - 2 * q.x
        return a / b

    def formula_y(self, x: float) -> float:
        """Get y coordinate given the x coordinate.

        In this case is a line.
        """
        p = self.sites[0]
        q = self.sites[1]
        a = -((q.x - p.x) / (q.y - p.y))
        b = (q.x ** 2 - p.x ** 2 + q.y ** 2 - p.y ** 2) / (2 * (q.y - p.y))
        return a * x + b
