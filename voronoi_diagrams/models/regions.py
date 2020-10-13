"""Region representation."""

# Standard Library
from typing import Callable, Optional, Any, Union
from abc import ABCMeta, abstractmethod

# Models
from .boundaries import Boundary
from .points import Point
from .events import Site

# Math
from decimal import Decimal


class Region:
    """Voronoi Cell that is * mapped."""

    __metaclass__ = ABCMeta

    left: Optional[Boundary]
    right: Optional[Boundary]
    site: Site
    active: bool
    is_to_be_deleted: bool

    def __init__(
        self,
        site: Site,
        left: Optional[Boundary] = None,
        right: Optional[Boundary] = None,
        active: bool = False,
    ):
        """Construct Boundary."""
        self.left = left
        self.right = right
        self.site = site
        self.active = active
        self.is_to_be_deleted = False

    def is_contained(self, point: Point, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        if point.y < self.site.get_highest_site_point().y:
            return False

        is_left_contained = not self.is_left(point)
        is_right_contained = not self.is_right(point)
        return is_left_contained and is_right_contained

    def is_left(self, point: Point, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        if point.y < self.site.get_highest_site_point().y:
            return False

        if self.left is None:
            return False
        comparison = self.left.get_point_comparison(point)
        if comparison is not None:
            return comparison < 0
        else:
            middle_point_x = self.left.bisector.get_middle_between_sites().x
            return (middle_point_x <= self.site.point.x) and (middle_point_x > point.x)

    def is_right(self, point: Point, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        if point.y < self.site.get_highest_site_point().y:
            return False

        if self.right is None:
            return False

        comparison = self.right.get_point_comparison(point)
        if comparison is not None:
            return comparison > 0
        else:
            middle_point_x = self.right.bisector.get_middle_between_sites().x
            return (middle_point_x >= self.site.point.x) and (middle_point_x < point.x)

    def __str__(self):
        """Get Region string representation."""
        return f"Region({self.site}, {self.left}, {self.right})"

    def __repr__(self):
        """Get Region representation."""
        return self.__str__()
