"""Event representation."""

# Standar Library
from typing import Union

# Models
from . import Point, Site


class Event:
    """Event Representation. It can be a Site or an Interception."""

    is_site: bool
    point: Union[Site, Point]

    def __init__(self, point: Point, is_site: bool):
        """Construct Event."""
        self.point = point
        self.is_site = is_site
