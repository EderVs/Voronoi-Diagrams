"""Site Representation."""
# Standard Library
from typing import Any

# Math
from decimal import Decimal


class Point:
    """Point to handle in Fortune's Algorithm."""

    x: Decimal
    y: Decimal

    def __init__(self, x, y):
        """Construct point."""
        self.x = x
        self.y = y

    def __str__(self):
        """Get String representation."""
        return f"P({self.x}, {self.y})"

    def __repr__(self):
        """Get object representation."""
        return self.__str__()

    def __eq__(self, point: Any):
        """Get equality between points."""
        return self.x == point.x and self.y == point.y

    def get_tuple(self):
        """Get tuple of coordinates (x, y)."""
        return (self.x, self.y)
