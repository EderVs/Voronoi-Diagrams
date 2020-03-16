"""Site Representation."""


class Site:
    """Site to handle in Fortune's Algorithm."""

    x: float
    y: float

    def __init__(self, x, y):
        """Construct point."""
        self.x = x
        self.y = y


class Point(Site):
    """Point to handle in Fortune's Algorithm."""

    def __init__(self, x, y):
        """Construct point."""
        super(Point, self).__init__(x, y)

    def __str__(self):
        """Get String representation."""
        return f"P({self.x}, {self.y})"

    def __repr__(self):
        """Get object representation."""
        return self.__str__()


# TODO: Weighted point
