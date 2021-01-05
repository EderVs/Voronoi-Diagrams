"""Regions representations in plots."""
# Standard Library.
from typing import Tuple, Type

# Models.
from voronoi_diagrams.models import (
    Boundary,
    Region,
    Bisector
)
from plots.plot_utils.models.boundaries import plot_boundary

# Plot.
from plotly import graph_objects as go
import numpy as np

# Math
from decimal import Decimal


def plot_region(
    figure: go.Figure,
    region: Region,
    xlim: Tuple[Decimal, Decimal],
    ylim: Tuple[Decimal, Decimal],
    bisector_class: Type[Bisector],
):
    """Plot Region."""
    if region.left is not None:
        plot_boundary(figure, region.left, xlim, ylim, bisector_class)
    if region.right is not None:
        plot_boundary(figure, region.right, xlim, ylim, bisector_class)