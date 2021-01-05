"""Points representations in plot."""

# Standard Library.
from typing import List, Optional, Dict, Any

# Plot
from plotly import graph_objects as go

# Math
from decimal import Decimal


def get_point_trace(
    x: Decimal,
    y: Decimal,
    color: str = "",
    marker: str = "",
    name: str = "",
    symbol: str = "",
    size: Optional[int] = None,
    group: str = "",
) -> go.Scatter:
    """Get point trace."""
    marker_properties: Dict[str, Any] = {}
    if color != "":
        marker_properties["color"] = color
    if symbol != "":
        marker_properties["symbol"] = symbol
    if size is not None:
        marker_properties["size"] = size
    return go.Scatter(
        x=[x],
        y=[y],
        mode="markers",
        legendgroup=group,
        name=name,
        marker=marker_properties,
        hoverinfo="name",
    )


def plot_point(
    x: Decimal,
    y: Decimal,
    color: str = "",
    marker: str = "",
    name: str = "",
    symbol: str = "",
    size: Optional[int] = None,
    group: str = "",
) -> go.Scatter:
    """Plot a Point."""
    return get_point_trace(x, y, color, marker, name, symbol, size, group)
    # plt.plot(x, y, f"{color}{marker}", markersize=5)
