"""Event representation."""

# Standar Library
from typing import Union

# Models
from .points import Point


class Event:
    """Event Representation. It can be a Site or an Interception."""

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

    def __init__(self, x, y):
        """Construct point."""
        super(Intersection, self).__init__(x, y, False)


# TODO: Weighted point
