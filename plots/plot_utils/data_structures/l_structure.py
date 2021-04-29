"""L structures plots."""

from typing import Tuple, Type

# Data structures
from voronoi_diagrams.data_structures import LStructure

# Models.
from voronoi_diagrams.models import Bisector
from plots.plot_utils.models.boundaries import plot_boundary

# Plot.
# from matplotlib import pyplot as plt
from plotly import graph_objects as go

# Math
from decimal import Decimal


def plot_l_structure(
    figure: go.Figure,
    l_structure: LStructure,
    xlim: Tuple[Decimal, Decimal],
    ylim: Tuple[Decimal, Decimal],
    bisector_class: Type[Bisector],
):
    """Plot L structure."""
    node = l_structure.head.right_neighbor
    while node is not None:
        plot_boundary(figure, node.value.left, xlim, ylim, bisector_class)
        node = node.right_neighbor
