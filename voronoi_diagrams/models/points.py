"""Site Representation."""
# Standard Library
from typing import Tuple

# Math
from decimal import Decimal

Coordinates = Tuple[Decimal, Decimal]


class Point:
    """Point representation."""

    x: Decimal
    y: Decimal

    def __init__(self, x: Decimal, y: Decimal) -> None:
        """Construct point."""
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """Get String representation."""
        return f"{'{0:.4f}'.format(self.x)}, {'{0:.4f}'.format(self.y)}"

    def __repr__(self) -> str:
        """Get object representation."""
        return self.__str__()

    def __eq__(self, point: "Point") -> str:
        """Get equality between points."""
        return self.x == point.x and self.y == point.y

    def get_tuple(self) -> Coordinates:
        """Get tuple of coordinates (x, y)."""
        return (self.x, self.y)
