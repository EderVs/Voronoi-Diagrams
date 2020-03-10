"""Event representation."""

# Models
from . import Point


class Event:
    """Event Representation. It can be a Site or an Interception."""

    is_site: bool
    point: Point

    def __init__(self, point: Point, is_site: bool):
        """Construct Event."""
        self.point = point
        self.is_site = is_site
