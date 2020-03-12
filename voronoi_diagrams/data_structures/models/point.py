"""Site Representation."""


class Point:
    """Point to handle in Fortune's Algorithm."""

    x: float
    y: float

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


# TODO: Weighted point
