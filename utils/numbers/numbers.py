"""Numbers utils."""


def are_close(a, b, epsilon):
    """Check if a and b are relative (to epsilon) close."""
    return (a - epsilon) <= b and (a + epsilon) >= b
