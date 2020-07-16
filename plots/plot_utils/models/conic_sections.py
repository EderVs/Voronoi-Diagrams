"""Conic sections representations in plot."""

# Standard Library.
from typing import List

# Plot
from matplotlib import pyplot as plt

# Conic sections
from conic_sections.utils.circle import get_circle_formula_y

# Math
from decimal import Decimal

import numpy as np


def plot_circle(h: Decimal, k: Decimal, r: Decimal) -> None:
    """Plot a circle."""
    y_lists: List[List[Decimal]] = [[], []]
    step = Decimal("0.01")
    x_range = np.arange(h - r, h + r + step, step)
    for x in x_range:
        ys = get_circle_formula_y(h, k, r, x)
        if ys is None:
            continue
        y_lists[0].append(ys[0])
        y_lists[1].append(ys[1])
    plt.plot(x_range, y_lists[0], "k")
    plt.plot(x_range, y_lists[1], "k")
