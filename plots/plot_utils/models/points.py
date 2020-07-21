"""Points representations in plot."""

# Standard Library.
from typing import List

# Plot
from matplotlib import pyplot as plt

# Conic sections
from conic_sections.utils.circle import get_circle_formula_y

# Math
from decimal import Decimal


def plot_point(x: Decimal, y: Decimal, color, marker) -> None:
    """Plot a Point."""
    plt.plot(x, y, f"{color}{marker}", markersize=5)
