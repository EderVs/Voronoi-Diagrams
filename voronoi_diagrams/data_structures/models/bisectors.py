"""Bisector representation."""

# Standard Library
from typing import Callable, Tuple, Optional, Any
from abc import ABCMeta, abstractmethod

# Models
from .events import Site
from .points import Point


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
    def formula_x(self, y: float) -> float:
        """Get x coordinate given the y coordinate."""
        raise NotImplementedError

    @abstractmethod
    def formula_y(self, y: float) -> float:
        """Get y coordinate given the x coordinate."""
        raise NotImplementedError

    def __str__(self):
        """Get bisector string representation."""
        return f"Bisector({self.sites[0]}, {self.sites[1]})"

    def __repr__(self):
        """Get Bisector representation."""
        return self.__str__()

    @abstractmethod
    def get_intersection_point(self, bisector: Any) -> Optional[Point]:
        """Get the point of intersection between two bisectors."""
        raise NotImplementedError


class PointBisector(Bisector):
    """Bisector defined by point sites."""

    def __init__(self, sites: Tuple[Site, Site]):
        """Construct bisector of Point sites Bisector."""
        super(PointBisector, self).__init__(sites)

    def formula_x(self, y: float) -> float:
        """Get x coordinate given the y coordinate.

        In this case is a line.
        """
        p = self.sites[0].point
        q = self.sites[1].point
        a = (2 * q.y - 2 * p.y) * y + (p.y ** 2 - q.y ** 2) - (q.x ** 2 - p.x ** 2)
        b = 2 * p.x - 2 * q.x
        return a / b

    def formula_y(self, x: float) -> float:
        """Get y coordinate given the x coordinate.

        In this case is a line.
        """
        p = self.sites[0].point
        q = self.sites[1].point
        a = -((q.x - p.x) / (q.y - p.y))
        b = (q.x ** 2 - p.x ** 2 + q.y ** 2 - p.y ** 2) / (2 * (q.y - p.y))
        return a * x + b

    def get_intersection_point(self, bisector: Bisector) -> Point:
        """Get the point of intersection between two bisectors."""

        def f_aux_1(xi: float, xj: float, yi: float, yj: float) -> float:
            """Auxiliar function."""
            return (xj ** 2 - xi ** 2 + yj ** 2 - yi ** 2) / (2 * (yj - yi))

        def f_aux_2(xi: float, xj: float, yi: float, yj: float) -> float:
            """Auxiliar function."""
            return (xj - xi) / (yj - yi)

        def get_x(
            xi: float,
            xj: float,
            xk: float,
            xl: float,
            yi: float,
            yj: float,
            yk: float,
            yl: float,
        ) -> float:
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

        x = get_x(x1, x2, x3, x4, y1, y2, y3, y4)
        return Point(x, self.formula_y(x))
