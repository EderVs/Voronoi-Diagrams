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
        """Construct region."""
        self.left = left
        self.right = right
        self.site = site
        self.active = active
        self.is_to_be_deleted = False

    def is_contained(self, point: Point, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        if point.y < self.site.get_highest_site_point().y:
            return False

        return self.is_left_contained(point) and self.is_right_contained(point)

    def is_left_contained(self, point: Point) -> bool:
        """Return if a point is containted to the left."""
        if point.y < self.site.get_highest_site_point().y:
            return False
        if self.left is None:
            return True

        comparison = self.left.get_point_comparison(point)
        return comparison > 0

    def is_right_contained(self, point: Point) -> bool:
        """Return if a point is containted to the right."""
        if point.y < self.site.get_highest_site_point().y:
            return False
        if self.right is None:
            return True

        comparison = self.right.get_point_comparison(point)
        return comparison <= 0

    def is_left(self, point: Point, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        return not self.is_left_contained(point) and self.is_right_contained(point)

    def is_right(self, point: Point, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        return self.is_left_contained(point) and not self.is_right_contained(point)

    def __str__(self):
        """Get Region string representation."""
        return f"Region({self.site}, {self.left}, {self.right})"

    def __repr__(self):
        """Get Region representation."""
        return self.__str__()
