"""Boundaries representations in plots."""
# Standard Library.
from typing import Tuple, Type

# Models.
from voronoi_diagrams.models import (
    Boundary,
    Bisector,
    PointBisector,
    WeightedPointBisector,
)

# Plot.
# from matplotlib import pyplot as plt
from plotly import graph_objects as go
import numpy as np

# Math
from decimal import Decimal


def get_plot_scatter_boundary(
    boundary: Boundary,
    xlim: Tuple[Decimal, Decimal],
    ylim: Tuple[Decimal, Decimal],
    bisector_class: Type[Bisector],
) -> go.Scatter:
    """Get plot scatter boundary."""
    y_list = []
    x_list = []
    num_steps = Decimal("50")
    if bisector_class == PointBisector:
        if boundary.bisector.is_vertical():
            if not boundary.sign:
                return None
            step = (
                abs(boundary.get_site().get_event_point().y - Decimal(ylim[1]))
                / num_steps
            )
            if step > 0:
                y_list = np.arange(
                    boundary.get_site().get_event_point().y, Decimal(ylim[1]), step
                )
                for y in y_list:
                    x_list.append(boundary.bisector.get_middle_between_sites().x)
        elif boundary.sign:
            step = abs(boundary.get_site().point.x - Decimal(xlim[1])) / num_steps
            if step > 0:
                x_list = np.arange(boundary.get_site().point.x, Decimal(xlim[1]), step)
        else:
            step = abs(Decimal(xlim[0]) - boundary.get_site().point.x) / num_steps
            if step > 0:
                x_list = np.arange(
                    Decimal(xlim[0]), boundary.get_site().point.x - step, step
                )

        if y_list == []:
            pass_limit = False
            last = len(x_list) - 1
            for i in range(len(x_list)):
                x = x_list[i]
                if x < xlim[0] or x > xlim[1]:
                    y_list.append(None)
                    continue
                if (boundary.sign and i == 0) or (not boundary.sign and i == last):
                    y_list.append(boundary.get_site().get_highest_site_point().y)
                    continue
                ys = boundary.formula_y(Decimal(x))
                if len(ys) == 0:
                    y_list.append(None)
                elif ys[0] >= ylim[0] and ys[0] <= ylim[1]:
                    y_list.append(ys[0])
                else:
                    if pass_limit:
                        y_list.append(None)
                    else:
                        y_list.append(ys[0])
                        pass_limit = True
    elif bisector_class == WeightedPointBisector:
        x_list = []
        y_list = []

        if boundary.is_boundary_not_x_monotone():
            change_of_x = boundary.bisector.conic_section.get_vertical_tangents()[0]
            x_lists = [[], []]
            if boundary.sign:
                step = abs(boundary.get_site().point.x - change_of_x) / num_steps
                if step > 0:
                    x_lists[0] = np.arange(
                        boundary.get_site().point.x, change_of_x, step
                    )
                    step = abs(change_of_x - Decimal(xlim[0])) / num_steps
                    if step > 0:
                        x_lists[1] = np.arange(change_of_x, Decimal(xlim[0]), -step)
            else:
                step = abs(boundary.get_site().point.x - change_of_x) / num_steps
                if step > 0:
                    x_lists[0] = np.arange(
                        boundary.get_site().point.x, change_of_x, -step
                    )
                    step = abs(change_of_x - Decimal(xlim[0])) / num_steps
                    if step > 0:
                        x_lists[1] = np.arange(change_of_x, Decimal(xlim[1]), step)

            func_map = {0: min, 1: max}
            pass_limit = False
            for i, _ in enumerate(x_lists):
                for j in range(len(x_lists[i])):
                    x = x_lists[i][j]
                    if x < xlim[0] or x > xlim[1]:
                        y_list.append(None)
                        continue
                    if i == 0 and j == 0:
                        y_list.append(boundary.get_site().get_highest_site_point().y)
                        continue
                    ys = boundary.formula_y(Decimal(x))
                    if len(ys) == 0:
                        y_list.append(None)
                    else:
                        y = func_map[i](ys)
                        if y >= ylim[0] and y <= ylim[1]:
                            y_list.append(y)
                        else:
                            if pass_limit:
                                y_list.append(None)
                            else:
                                y_list.append(y)
                                pass_limit = True
            x_list = np.concatenate(x_lists)
        elif boundary.bisector.is_vertical():
            if not boundary.sign:
                return None
            step = (
                abs(boundary.get_site().get_event_point().y - Decimal(ylim[1]))
                / num_steps
            )
            if step > 0:
                y_list = np.arange(
                    boundary.get_site().get_event_point().y, Decimal(ylim[1]), step
                )
                for y in y_list:
                    x_list.append(boundary.bisector.get_middle_between_sites().x)
        elif boundary.sign:
            step = abs(boundary.get_site().point.x - Decimal(xlim[1])) / num_steps
            if step > 0:
                x_list = np.arange(boundary.get_site().point.x, Decimal(xlim[1]), step)
        else:
            step = abs(Decimal(xlim[0]) - boundary.get_site().point.x) / num_steps
            if step > 0:
                x_list = np.arange(Decimal(xlim[0]), boundary.get_site().point.x, step)

        if y_list == []:
            pass_limit = False
            last = len(x_list) - 1
            for i in range(len(x_list)):
                x = x_list[i]
                if x < xlim[0] or x > xlim[1]:
                    y_list.append(None)
                    continue
                if (boundary.sign and i == 0) or (not boundary.sign and i == last):
                    y_list.append(boundary.get_site().get_highest_site_point().y)
                    continue
                ys = boundary.formula_y(Decimal(x))
                if len(ys) == 0:
                    y_list.append(None)
                elif ys[0] >= ylim[0] and ys[0] <= ylim[1]:
                    y_list.append(ys[0])
                else:
                    if pass_limit:
                        y_list.append(None)
                    else:
                        y_list.append(ys[0])
                        pass_limit = True

    return go.Scatter(
        x=x_list,
        y=y_list,
        mode="lines",
        name=str(boundary),
        connectgaps=True,
        line={"dash": "dot"},
        legendgroup="boundaries",
        hoverinfo="name",
    )


def plot_boundary(
    figure: go.Figure,
    boundary: Boundary,
    xlim: Tuple[Decimal, Decimal],
    ylim: Tuple[Decimal, Decimal],
    bisector_class: Type[Bisector],
):
    """Plot boundary."""
    figure.add_trace(get_plot_scatter_boundary(boundary, xlim, ylim, bisector_class))
