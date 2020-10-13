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
    """Event Representation. It can be either a Site or an Interception."""

    __metaclass__ = ABCMeta

    is_site: bool
    point: Point
    name: str

    def __init__(self, x: Decimal, y: Decimal, is_site: bool, name: str = ""):
        """Construct Event."""
        self.point = Point(x, y)
        self.is_site = is_site
        self.name = name

    @abstractmethod
    def get_event_point(self) -> Point:
        """Get event point to evaluate."""
        raise NotImplementedError

    def get_str(self):
        """Get letter in str representation of event."""
        raise NotImplementedError

    def get_point_str(self):
        """Get point string representation."""
        return f"{'{0:.4f}'.format(self.point.x)}, {'{0:.4f}'.format(self.point.y)}"

    def __str__(self):
        """Get String representation."""
        event_str = self.get_str()
        return f"{self.name} {event_str}"

    def get_display_str(self):
        """Get string representation in plot."""
        return f"{self.name} S({self.get_point_str()})"

    def get_event_str(self):
        """Get event str."""
        raise NotImplementedError

    def __repr__(self):
        """Get object representation."""
        return self.__str__()

    def is_dominated(self, event: Any) -> bool:
        """Check if this event is dominated to other event."""
        raise NotImplementedError

    def get_comparison(self, event: Any) -> Decimal:
        """Get comparison between 2 events."""
        event_point = self.get_event_point()
        other_event_point = event.get_event_point()
        if other_event_point.y == event_point.y:
            return event_point.x - other_event_point.x
        return event_point.y - other_event_point.y


class Site(Event):
    """Site to handle in Fortune's Algorithm.

    By itself it is just a point.
    """

    def __init__(self, x: Decimal, y: Decimal, name: str = ""):
        """Construct point."""
        super(Site, self).__init__(x, y, True, name=name)

    def get_str(self):
        """Get string representation of Site."""
        return f"S({self.get_point_str()})"

    def __eq__(self, site: Any) -> bool:
        """Get equality between sites."""
        return self.point.x == site.point.x and self.point.y == site.point.y

    def get_display_str(self):
        """Get string representation in plot."""
        return f"{self.name} S({self.get_point_str()})"

    def get_event_str(self):
        """Get event str."""
        return f"S {self.name}"

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

    def get_distance_to_site_point_from_point(self, x: Decimal, y: Decimal) -> Decimal:
        """Get distance to site point from another point."""
        return (
            ((self.point.x - x) ** Decimal(2)) + ((self.point.y - y) ** Decimal(2))
        ).sqrt()

    def get_distance_to_site_frontier_from_point(
        self, x: Decimal, y: Decimal
    ) -> Decimal:
        """Get distance to site frontier from point."""
        return self.get_distance_to_site_point_from_point(x, y)

    def get_weighted_distance(self, x: Decimal, y: Decimal) -> Decimal:
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

    def get_event_point(self) -> Point:
        """Get event point to evaluate."""
        return self.get_highest_site_point()

    def is_dominated(self, site: Any) -> bool:
        """Check if this event is dominated to other event."""
        return False

    def get_object_to_hash(self) -> Any:
        """Get object to hash this site."""
        return (self.point.x, self.point.y)


class Intersection(Event):
    """Intersection to handle in Fortune's Algorithm."""

    vertex: Point
    region_node: AVLNode

    def __init__(self, event: Point, vertex: Point, region_node: AVLNode):
        """Construct point."""
        super(Intersection, self).__init__(event.x, event.y, False)
        self.vertex = vertex
        self.region_node = region_node

    def get_str(self):
        """Get string representation of Site."""
        return f"I({self.get_point_str()})"

    def get_event_str(self):
        """Get event str."""
        return self.get_str()

    def get_event_point(self) -> Point:
        """Get event point to evaluate."""
        return self.point

    def is_dominated(self, site: Any) -> bool:
        """Check if this event is dominated to other event."""
        return False


class WeightedSite(Site):
    """Weighted Site to handle in Fortune's Algorithm.

    Is a point with weight.
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

    def compare_weights(self, site: Any) -> int:
        """Compare weight between sites."""
        if self.weight >= 0:
            return self.weight - site.weight
        else:
            return site.weight - self.weight

    def get_x_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the last point of the site pointing to given point."""
        if point.x >= self.point.x:
            sign = Decimal(1)
        else:
            sign = Decimal(-1)

        if point.x == self.point.x:
            return self.point.x

        angle = abs(atan((point.y - self.point.y) / (point.x - self.point.x)))
        x = abs(self.weight) * Decimal(cos(angle))
        return self.point.x + sign * x

    def get_x_farthest_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the farthest point of the site pointing to given point."""
        if point.x >= self.point.x:
            sign = Decimal(-1)
        else:
            sign = Decimal(1)

        if point.x == self.point.x:
            return self.point.x

        angle = abs(atan((point.y - self.point.y) / (point.x - self.point.x)))
        x = abs(self.weight) * Decimal(cos(angle))
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
        y = abs(self.weight) * Decimal(sin(angle))
        return self.point.y + sign * y

    def get_y_farthest_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the farthest point of the site pointing to given point."""
        if point.y >= self.point.y:
            sign = Decimal(-1)
        else:
            sign = Decimal(1)

        if point.x == self.point.x:
            return self.point.y + sign * self.weight

        angle = abs(atan((point.y - self.point.y) / (point.x - self.point.x)))
        y = abs(self.weight) * Decimal(sin(angle))
        return self.point.y + sign * y

    def get_y_frontier_formula(self, x: Decimal) -> Optional[Tuple[Decimal, Decimal]]:
        """Get the frontier's y coordinates given x coordinate."""
        return get_circle_formula_y(self.point.x, self.point.y, abs(self.weight), x)

    def get_x_frontier_formula(self, y: Decimal) -> Optional[Tuple[Decimal, Decimal]]:
        """Get the frontier's x coordinates given y coordinate."""
        return get_circle_formula_x(self.point.x, self.point.y, abs(self.weight), y)

    def get_distance_to_site_frontier_from_point(
        self, x: Decimal, y: Decimal
    ) -> Decimal:
        """Get distance to site frontier from point.

        The frontier in this case is the circle given by the weight as radius.
        """
        return super(WeightedSite, self).get_distance_to_site_point_from_point(
            x, y
        ) - abs(self.weight)

    def get_weighted_distance(self, x: Decimal, y: Decimal) -> Decimal:
        """Get distance to site frontier from point.

        The frontier in this case is the circle given by the weight as radius.
        """
        return super(WeightedSite, self).get_distance_to_site_point_from_point(
            x, y
        ) + abs(self.weight)

    def get_highest_site_point(self) -> Point:
        """Get highest point in the site."""
        return Point(self.point.x, self.point.y + abs(self.weight))

    def get_rightest_site_point(self) -> Point:
        """Get rightest point in the site."""
        return Point(self.point.x + abs(self.weight), self.point.y)

    def get_lowest_site_point(self) -> Point:
        """Get lowest point in the site."""
        return Point(self.point.x, self.point.y - abs(self.weight))

    def get_str(self):
        """Get String representation."""
        return f"WS({self.get_point_str()}, {'{0:.4f}'.format(self.weight)})"

    def is_dominated(self, site: Any) -> bool:
        """Check if this event is dominated to other event."""
        if self.weight >= 0:
            return self.weight >= site.get_weighted_distance(self.point.x, self.point.y)
        else:
            return abs(site.weight) >= self.get_weighted_distance(
                site.point.x, self.point.y
            )

    def get_object_to_hash(self) -> Any:
        """Get object to hash this site."""
        return (self.point.x, self.point.y, self.weight)

    def get_comparison(self, event: Event) -> Decimal:
        """Get comparison between 2 events."""
        if not event.is_site:
            return super().get_comparison(event)

        # We now know that event is a Weighted site.
        event_point = self.get_event_point()
        other_event_point = event.get_event_point()
        if other_event_point.y == event_point.y:
            if self.weight == event.weight:
                return event_point.x - other_event_point.x
            # The smallest site will be first.
            return self.weight - event.weight
        return event_point.y - other_event_point.y
