"""Event representation."""

# Standar Library
from typing import Union, Any, Optional, Tuple
from abc import ABCMeta, abstractmethod

# Models
from .points import Point

# Data Structures
from ..data_structures.avl_tree import AVLNode

# Math
from math import tan, atan, sin, cos
from decimal import Decimal

# Conic Sections
from conic_sections.utils.circle import get_circle_formula_x, get_circle_formula_y


class Event:
    """Event Representation. It can be a Site or an Interception."""

    __metaclass__ = ABCMeta

    is_site: bool
    point: Point
    name: str

    def __init__(self, x: Decimal, y: Decimal, is_site: bool, name: str = ""):
        """Construct Event."""
        self.point = Point(x, y)
        self.is_site = is_site
        self.name = name

    def __str__(self):
        """Get String representation."""
        if self.is_site:
            letter = "S"
        else:
            letter = "I"
        return f"{self.name} {letter}({self.point.x}, {self.point.y})"

    def __repr__(self):
        """Get object representation."""
        return self.__str__()


class Site(Event):
    """Site to handle in Fortune's Algorithm."""

    def __init__(self, x: Decimal, y: Decimal, name: str = ""):
        """Construct point."""
        super(Site, self).__init__(x, y, True, name=name)

    def __eq__(self, site: Any) -> bool:
        """Get equality between sites."""
        return self.point.x == site.point.x and self.point.y == site.point.y

    def get_x_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the last point of the site pointing to given point."""
        return self.point.x

    def get_y_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the last point of the site pointing to given point."""
        return self.point.y

    def get_y_frontier_formula(self, x: Decimal) -> Tuple[Decimal, Decimal]:
        """Get the frontier's y coordinates given x coordinate."""
        return (self.point.y, self.point.y)

    def get_x_frontier_formula(self, x: Decimal) -> Tuple[Decimal, Decimal]:
        """Get the frontier's x coordinates given y coordinate."""
        return (self.point.x, self.point.x)

    def get_distance_to_site_point_from_point(self, x: Decimal, y: Decimal):
        """Get distance to site point from another point."""
        return (
            ((self.point.x - x) ** Decimal(2)) + ((self.point.y - y) ** Decimal(2))
        ).sqrt()

    def get_distance_to_site_frontier_from_point(
        self, x: Decimal, y: Decimal
    ) -> Decimal:
        """Get distance to site frontier from point."""
        return self.get_distance_to_site_point_from_point(x, y)

    def get_distance_to_site_farthest_frontier_from_point(
        self, x: Decimal, y: Decimal
    ) -> Decimal:
        """Get distance to site frontier from point.

        The frontier in this case is the site point itself.
        """
        return self.get_distance_to_site_point_from_point(x, y)

    def get_highest_site_point(self) -> Point:
        """Get lowest point in the site."""
        return self.point

    def get_rightest_site_point(self) -> Point:
        """Get rightest point in the site."""
        return self.point

    def get_lowest_site_point(self) -> Point:
        """Get lowest point in the site."""
        return self.point


class IntersectionEvent(Event):
    """Intersection to handle in Fortune's Algorithm."""

    vertex: Point
    region_node: AVLNode

    def __init__(self, event: Point, vertex: Point, region_node: AVLNode):
        """Construct point."""
        super(IntersectionEvent, self).__init__(event.x, event.y, False)
        self.vertex = vertex
        self.region_node = region_node


class WeightedSite(Site):
    """Weighted Site to handle in Fortune's Algorithm.

    Is like a site but with a weight.
    """

    weight: Decimal

    def __init__(self, x: Decimal, y: Decimal, weight: Decimal, name: str = ""):
        """Construct point."""
        super(WeightedSite, self).__init__(x, y, name=name)
        self.weight = weight

    def __eq__(self, wsite: Any) -> bool:
        """Get equality between weighted sites."""
        return (
            self.point.x == wsite.point.x
            and self.point.y == wsite.point.y
            and self.weight == wsite.weight
        )

    def get_x_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the last point of the site pointing to given point."""
        if point.x >= self.point.x:
            sign = Decimal(1)
        else:
            sign = Decimal(-1)

        if point.x == self.point.x:
            return self.point.x

        angle = abs(atan((point.y - self.point.y) / (point.x - self.point.x)))
        x = self.weight * Decimal(cos(angle))
        return self.point.x + sign * x

    def get_y_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the last point of the site pointing to given point."""
        if point.y >= self.point.y:
            sign = Decimal(1)
        else:
            sign = Decimal(-1)

        if point.x == self.point.x:
            return self.point.y + sign * self.weight

        angle = abs(atan((point.y - self.point.y) / (point.x - self.point.x)))
        y = self.weight * Decimal(sin(angle))
        return self.point.y + sign * y

    def get_y_frontier_formula(self, x: Decimal) -> Optional[Tuple[Decimal, Decimal]]:
        """Get the frontier's y coordinates given x coordinate."""
        return get_circle_formula_y(self.point.x, self.point.y, self.weight, x)

    def get_x_frontier_formula(self, y: Decimal) -> Optional[Tuple[Decimal, Decimal]]:
        """Get the frontier's x coordinates given y coordinate."""
        return get_circle_formula_x(self.point.x, self.point.y, self.weight, y)

    def get_distance_to_site_frontier_from_point(
        self, x: Decimal, y: Decimal
    ) -> Decimal:
        """Get distance to site frontier from point.

        The frontier in this case is the circle given by the weight as radius.
        """
        return (
            super(WeightedSite, self).get_distance_to_site_point_from_point(x, y)
            - self.weight
        )

    def get_distance_to_site_farthest_frontier_from_point(
        self, x: Decimal, y: Decimal
    ) -> Decimal:
        """Get distance to site frontier from point.

        The frontier in this case is the circle given by the weight as radius.
        """
        return (
            super(WeightedSite, self).get_distance_to_site_point_from_point(x, y)
            + self.weight
        )

    def get_highest_site_point(self) -> Point:
        """Get highest point in the site."""
        return Point(self.point.x, self.point.y + self.weight)

    def get_rightest_site_point(self) -> Point:
        """Get rightest point in the site."""
        return Point(self.point.x + self.weight, self.point.y)

    def get_lowest_site_point(self) -> Point:
        """Get lowest point in the site."""
        return Point(self.point.x, self.point.y - self.weight)

    def __str__(self):
        """Get String representation."""
        return f"{self.name} WS({self.point.x}, {self.point.y}, {self.weight})"
