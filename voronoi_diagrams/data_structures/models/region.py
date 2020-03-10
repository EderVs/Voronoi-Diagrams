"""Region representation."""

# Standard Library
from typing import Callable, Optional
from math import sqrt

# Models
from .boundary import Boundary
from .point import Point


class Region:
    """Voronoi Cell that is * mapped."""

    left: Optional[Boundary]
    right: Optional[Boundary]
    site: Point

    def __init__(
        self,
        left: Optional[Boundary],
        right: Optional[Boundary],
        site: Point,
    ):
        """Construct Boundary."""
        self.left = left
        self.right = left
        self.site = site

    def star(self, point: Point) -> Point:
        """Map a bisector."""
        raise NotImplementedError


class PointRegion(Region):
    """Region of a Point site."""

    def __init__(self, left: Boundary, right: Boundary, site: Point):
        """Construct Point Region."""
        super(PointRegion, self).__init__(left, right, site)

    def distance_to_site(self, point: Point) -> float:
        """Get distance to the site."""
        return sqrt((self.site.x - point.x)**2 + (self.site.y - point.y)**2)

    def star(self, point: Point) -> Point:
        """Map a bisector."""
        return Point(point.x, point.y+self.distance_to_site(point))
