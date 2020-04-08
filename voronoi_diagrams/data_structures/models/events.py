"""Event representation."""

# Standar Library
from typing import Union, Any
from abc import ABCMeta, abstractmethod

# Models
from .points import Point
from ..avl_tree import AVLNode


class Event:
    """Event Representation. It can be a Site or an Interception."""

    __metaclass__ = ABCMeta

    is_site: bool
    point: Point

    def __init__(self, x: float, y: float, is_site: bool):
        """Construct Event."""
        self.point = Point(x, y)
        self.is_site = is_site

    def __str__(self):
        """Get String representation."""
        if self.is_site:
            letter = "S"
        else:
            letter = "I"
        return f"{letter}({self.point.x}, {self.point.y})"

    def __repr__(self):
        """Get object representation."""
        return self.__str__()


class Site(Event):
    """Site to handle in Fortune's Algorithm."""

    def __init__(self, x, y):
        """Construct point."""
        super(Site, self).__init__(x, y, True)


class Intersection(Event):
    """Intersection to handle in Fortune's Algorithm."""

    LEFT_PLACE = 1
    RIGHT_PLACE = 2

    region_node: AVLNode

    def __init__(
        self, x, y, region_node: AVLNode,
    ):
        """Construct point."""
        super(Intersection, self).__init__(x, y, False)
        self.region_node = region_node


# TODO: Weighted point
