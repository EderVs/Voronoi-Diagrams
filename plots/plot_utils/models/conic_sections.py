"""Conic sections representations in plot."""

# Standard Library.
from typing import List, Any, Tuple, Iterable

# Plot
# from matplotlib import pyplot as plt

# Conic sections
from conic_sections.utils.circle import get_circle_formula_y

# Math
from decimal import Decimal

import numpy as np


def get_circle_ranges(
    h: Decimal, k: Decimal, r: Decimal, color
) -> Tuple[Iterable, Iterable]:
    """Plot a circle."""
    y_lists: List[List[Any]] = [[], []]
    step = Decimal("0.01")
    x_range = np.arange(h - r, h + r + step, step)
    for x in x_range:
        ys = get_circle_formula_y(h, k, r, x)
        if ys is None:
            y_lists[0].append(None)
            y_lists[1].append(None)
            continue
        y_lists[0].append(ys[0])
        y_lists[1].append(ys[1])
    return (
        np.concatenate((x_range, x_range[::-1])),
        np.concatenate((y_lists[0], y_lists[1][::-1])),
    )
    # plt.plot(x_range, y_lists[0], f"{color}-")
    # plt.plot(x_range, y_lists[1], f"{color}-")
