"""Boundaries representations in plots."""
# Standard Library.
from typing import Iterable, Tuple, Optional, Any, Type

# Models.
from voronoi_diagrams.models import (
    Boundary,
    Bisector,
    PointBisector,
    WeightedPointBisector,
    WeightedPointBoundary,
)

# Plot.
# from matplotlib import pyplot as plt
from plotly import graph_objects as go
import numpy as np

# Math
from decimal import Decimal


def plot_boundary(
    figure: go.Figure,
    boundary: Boundary,
    xlim: Tuple[Decimal, Decimal],
    ylim: Tuple[Decimal, Decimal],
    bisector_class: Type[Bisector],
):
    """Plot boundary."""
    y_list = []
    if bisector_class == PointBisector:
        if boundary.sign:
            x_list = np.arange(
                boundary.get_site().point.x, Decimal(xlim[1]), Decimal("0.01")
            )
        else:
            x_list = np.arange(
                Decimal(xlim[0]), boundary.get_site().point.x, Decimal("0.01")
            )
        for x in x_list:
            if x < xlim[0] or x > xlim[1]:
                y_list.append(None)
                continue
            ys = boundary.formula_y(Decimal(x))
            if ys[0] >= ylim[0] and ys[0] <= ylim[1]:
                y_list.append(ys[0])
            else:
                y_list.append(None)
    elif bisector_class == WeightedPointBisector:
        x_list = []
        y_list = []

        if boundary.is_boundary_concave_to_y():
            change_of_x = boundary.bisector.conic_section.get_changes_of_sign_in_x()[0]
            x_lists = [[], []]
            if boundary.sign:
                x_lists[0] = np.arange(
                    boundary.get_site().point.x, change_of_x, Decimal("0.01")
                )
                x_lists[1] = np.arange(change_of_x, Decimal(xlim[0]), Decimal("-0.01"))
            else:
                x_lists[0] = np.arange(
                    boundary.get_site().point.x, change_of_x, Decimal("-0.01")
                )
                x_lists[1] = np.arange(change_of_x, Decimal(xlim[1]), Decimal("0.01"))

            func_map = {0: min, 1: max}
            for i, _ in enumerate(x_lists):
                for x in x_lists[i]:
                    if x < xlim[0] or x > xlim[1]:
                        y_list.append(None)
                        continue
                    ys = boundary.formula_y(Decimal(x))
                    if len(ys) == 0:
                        y_list.append(None)
                    else:
                        y = func_map[i](ys)
                        if y >= ylim[0] and y <= ylim[1]:
                            y_list.append(func_map[i](ys))
                        else:
                            y_list.append(None)
            x_list = np.concatenate(x_lists)

        elif boundary.sign:
            x_list = np.arange(
                boundary.get_site().point.x, Decimal(xlim[1]), Decimal("0.01")
            )
        else:
            x_list = np.arange(
                Decimal(xlim[0]), boundary.get_site().point.x, Decimal("0.01")
            )

        if y_list == []:
            for x in x_list:
                if x < xlim[0] or x > xlim[1]:
                    y_list.append(None)
                    continue
                ys = boundary.formula_y(Decimal(x))
                if ys[0] >= ylim[0] and ys[0] <= ylim[1]:
                    y_list.append(ys[0])
                else:
                    y_list.append(None)

    figure.add_trace(
        go.Scatter(
            x=x_list, y=y_list, mode="lines", name=str(boundary), connectgaps=True
        )
    )
    # plt.plot(x_list, y_list, "k")
