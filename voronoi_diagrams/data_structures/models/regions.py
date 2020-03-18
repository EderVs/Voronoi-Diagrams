"""Region representation."""

# Standard Library
from typing import Callable, Optional, Any, Union
from math import sqrt

# Models
from .boundaries import Boundary
from .points import Point
from .events import Site


class Region:
    """Voronoi Cell that is * mapped."""

    left: Optional[Boundary]
    right: Optional[Boundary]
    site: Site

    def __init__(
        self,
        site: Site,
        left: Optional[Boundary] = None,
        right: Optional[Boundary] = None,
    ):
        """Construct Boundary."""
        self.left = left
        self.right = right
        self.site = site

    def star(self, point: Point) -> Point:
        """Map a bisector."""
        raise NotImplementedError

    def is_contained(self, point: Point, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        if point.y < self.site.point.y:
            return False

        is_left_contained = True
        is_right_contained = True
        if self.left is None and self.right is None:
            return True
        if self.left is not None:
            is_left_contained = self.left.get_point_comparison(point) >= 0
        if self.right is not None:
            is_right_contained = self.right.get_point_comparison(point) <= 0
        return is_left_contained and is_right_contained

    def is_left(self, point: Point, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        if point.y < self.site.point.y:
            return False

        if self.left is None:
            return False
        return self.left.get_point_comparison(point) < 0

    def is_right(self, point: Point, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        if point.y < self.site.point.y:
            return False

        if self.right is None:
            return False
        return self.right.get_point_comparison(point) > 0

    def __str__(self):
        """Get Region string representation."""
        return f"Region({self.site}, {self.left}, {self.right})"

    def __repr__(self):
        """Get Region representation."""
        return self.__str__()


class PointRegion(Region):
    """Region of a Point site."""

    def __init__(self, site: Site, left: Boundary, right: Boundary):
        """Construct Point Region."""
        super(PointRegion, self).__init__(site, left, right)

    def distance_to_site(self, point: Point) -> float:
        """Get distance to the site."""
        return sqrt(
            (self.site.point.x - point.x) ** 2 + (self.site.point.y - point.y) ** 2
        )

    def star(self, point: Point) -> Point:
        """Map a bisector."""
        return Point(point.x, point.y + self.distance_to_site(point))
