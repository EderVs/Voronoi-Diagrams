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


def get_point_trace(
    x: Decimal,
    y: Decimal,
    color: str = "",
    marker: str = "",
    name: str = "",
    symbol: str = "",
) -> go.Scatter:
    """Get point trace."""
    marker_properties = {}
    if color != "":
        marker_properties["color"] = color
    if symbol != "":
        marker_properties["symbol"] = symbol
    return go.Scatter(x=[x], y=[y], mode="markers", name=name, marker=marker_properties)


def plot_point(
    figure: go.Figure,
    x: Decimal,
    y: Decimal,
    color: str = "",
    marker: str = "",
    name: str = "",
    symbol: str = "",
) -> None:
    """Plot a Point."""
    figure.add_trace(get_point_trace(x, y, color, marker, name, symbol))
    # plt.plot(x, y, f"{color}{marker}", markersize=5)
