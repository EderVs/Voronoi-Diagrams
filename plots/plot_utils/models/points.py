"""Points representations in plot."""

# Standard Library.
from typing import List

# Plot
# from matplotlib import pyplot as plt
from plotly import graph_objects as go

# Conic sections
from conic_sections.utils.circle import get_circle_formula_y

# Math
from decimal import Decimal


def plot_point(figure: go.Figure, x: Decimal, y: Decimal, color, marker) -> None:
    """Plot a Point."""
    figure.add_trace(go.Scatter(x=[x], y=[y], mode="markers"))
    # plt.plot(x, y, f"{color}{marker}", markersize=5)
