"""Event representation."""

# Standar Library
from typing import Union, Any, Optional
from abc import ABCMeta, abstractmethod

# Models
from .points import Point

# Data Structures
from ..data_structures.avl_tree import AVLNode


class Event:
    """Event Representation. It can be a Site or an Interception."""

    __metaclass__ = ABCMeta

    is_site: bool
    point: Point
    name: str

    def __init__(self, x: float, y: float, is_site: bool, name: str = ""):
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

    def __init__(self, x: float, y: float, name: str = ""):
        """Construct point."""
        super(Site, self).__init__(x, y, True, name=name)

    def __eq__(self, site: Any) -> bool:
        """Get equality between sites."""
        return self.point.x == site.point.x and self.point.y == site.point.y

    def get_x_frontier_pointing_to_point(self, point: Point) -> float:
        """Get the last point of the site pointing to given point."""
        return self.point.x

    def get_y_frontier_pointing_to_point(self, point: Point) -> float:
        """Get the last point of the site pointing to given point."""
        return self.point.y


class Intersection(Event):
    """Intersection to handle in Fortune's Algorithm."""

    vertex: Point
    region_node: AVLNode

    def __init__(self, event: Point, vertex: Point, region_node: AVLNode):
        """Construct point."""
        super(Intersection, self).__init__(event.x, event.y, False)
        self.vertex = vertex
        self.region_node = region_node


# TODO: Weighted point
