"""Circle utils."""
# Standard Library
from typing import Optional, Tuple

# Math
from decimal import Decimal


def get_circle_formula_y(
    h: Decimal, k: Decimal, r: Decimal, x: Decimal
) -> Optional[Tuple[Decimal, Decimal]]:
    """Get y coordinates of a circle given x coordinate."""
    a = (r ** 2) - ((x - h) ** 2)
    if a < 0:
        return None
    y1 = k + a.sqrt()
    y2 = k - a.sqrt()
    return (y1, y2)


def get_circle_formula_x(
    h: Decimal, k: Decimal, r: Decimal, y: Decimal
) -> Optional[Tuple[Decimal, Decimal]]:
    """Get y coordinates of a circle given x coordinate."""
    return get_circle_formula_y(k, h, r, y)
