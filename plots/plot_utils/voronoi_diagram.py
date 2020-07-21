"""Voronoi Diagram representation in plot"""

# Standard Library.
from typing import Any
from decimal import Decimal

# Voronoi diagrams.
from voronoi_diagrams.fortunes_algorithm import VoronoiDiagram
from voronoi_diagrams.models import (
    Site,
    WeightedSite,
    PointBisector,
    WeightedPointBisector,
    VoronoiDiagramBisector,
    VoronoiDiagramVertex,
)

# Plot.
from matplotlib import pyplot as plt
import numpy as np
from plots.plot_utils.models.bisectors import (
    plot_bisector,
    plot_voronoi_diagram_bisector,
)
from plots.plot_utils.models.sites import plot_site
from plots.plot_utils.models.vertices import plot_vertex
from plots.plot_utils.models.points import plot_point


def plot_vertices_and_bisectors(
    voronoi_diagram: VoronoiDiagram, xlim, ylim, bisector_class
) -> None:
    """Plot bisectors in diagram."""
    if len(voronoi_diagram.vertices) == 0:
        print(voronoi_diagram.bisectors)
        if len(voronoi_diagram.bisectors) == 1:
            plot_voronoi_diagram_bisector(
                voronoi_diagram.bisectors[0],
                xlim=xlim,
                ylim=ylim,
                bisector_class=bisector_class,
            )
        return

    vertices_queue = [voronoi_diagram.vertices[0]]
    bisectors_passed = set()
    vertices_passed = set([id(voronoi_diagram.vertices[0])])
    while vertices_queue != []:
        vertex = vertices_queue.pop(0)
        print(vertex)
        plot_vertex(vertex)

        for vd_bisector in vertex.bisectors:
            if id(vd_bisector) in bisectors_passed:
                continue
            print(vd_bisector)
            bisectors_passed.add(id(vd_bisector))

            for bisector_vertex in vd_bisector.vertices:
                if id(bisector_vertex) in vertices_passed:
                    continue
                vertices_queue.append(bisector_vertex)
                vertices_passed.add(id(bisector_vertex))
            plot_voronoi_diagram_bisector(
                vd_bisector, xlim=xlim, ylim=ylim, bisector_class=bisector_class
            )


def plot_voronoi_diagram(
    voronoi_diagram: VoronoiDiagram, site_class: Any = Site
) -> None:
    """Plot voronoi diagram."""
    ylim = (-50, 50)
    xlim = (-50, 50)

    plt.figure(figsize=(12, 10))
    plt.gca().set_aspect("equal", adjustable="box")

    if site_class == Site:
        bisector_class = PointBisector
    elif site_class == WeightedSite:
        bisector_class = WeightedPointBisector

    # Sites.
    for site in voronoi_diagram.sites:
        plot_site(site, site_class)

    # Diagram.
    plot_vertices_and_bisectors(voronoi_diagram, xlim, ylim, bisector_class)

    plt.xlim(*xlim)
    plt.ylim(*ylim)
    plt.show()
