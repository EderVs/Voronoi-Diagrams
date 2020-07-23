"""Voronoi Diagram representation in plot"""

# Standard Library.
from typing import Any, Tuple, List, Type, Union
from decimal import Decimal

# Voronoi diagrams.
from voronoi_diagrams.fortunes_algorithm import VoronoiDiagram
from voronoi_diagrams.models import (
    Site,
    WeightedSite,
    Bisector,
    PointBisector,
    WeightedPointBisector,
    VoronoiDiagramBisector,
    VoronoiDiagramVertex,
    Point,
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


SiteToUse = Union[Point, Tuple[Point, Decimal]]
Limit = Tuple[Decimal, Decimal]


def is_a_limit_bisector(
    vd_bisector: VoronoiDiagramBisector,
    limit_sites: List[SiteToUse],
    bisector_class: Type[Bisector],
) -> None:
    """Check if current bisector is a bisector with a limit site."""
    for site in vd_bisector.bisector.get_sites_tuple():
        for limit_site in limit_sites:
            if is_equal_limit_site(site, limit_site, bisector_class=bisector_class):
                return True
    return False


def is_equal_limit_site(
    site: SiteToUse, limit_site: SiteToUse, bisector_class: Type[Bisector]
) -> None:
    """Check if site is a limit site."""
    if bisector_class == PointBisector:
        return site.point.x == limit_site.x and site.point.y == limit_site.y
    elif bisector_class == WeightedPointBisector:
        return (
            site.point.x == limit_site[0].x
            and site.point.y == limit_site[0].y
            and site.weight == limit_site[1]
        )


def plot_vertices_and_bisectors(
    voronoi_diagram: VoronoiDiagram,
    limit_sites: List[SiteToUse],
    xlim: Limit,
    ylim: Limit,
    bisector_class: Type[Bisector],
) -> None:
    """Plot bisectors in diagram."""
    if len(voronoi_diagram.vertices) == 0:
        print(voronoi_diagram.bisectors)  # Debugging
        if len(voronoi_diagram.bisectors) == 1:
            plot_voronoi_diagram_bisector(
                voronoi_diagram.bisectors[0],
                xlim=xlim,
                ylim=ylim,
                bisector_class=bisector_class,
            )
        return

    vertices_passed = set()
    for vd_bisector in voronoi_diagram.bisectors:
        print(vd_bisector)  # Debugging
        if not is_a_limit_bisector(
            vd_bisector, limit_sites, bisector_class=bisector_class
        ):
            for bisector_vertex in vd_bisector.vertices:
                if id(bisector_vertex) in vertices_passed:
                    continue
                vertices_passed.add(id(bisector_vertex))
                plot_vertex(bisector_vertex)
            plot_voronoi_diagram_bisector(
                vd_bisector, xlim=xlim, ylim=ylim, bisector_class=bisector_class
            )


def plot_voronoi_diagram(
    voronoi_diagram: VoronoiDiagram,
    limit_sites: List[SiteToUse],
    xlim: Limit,
    ylim: Limit,
    site_class: Type[Site] = Site,
) -> None:
    """Plot voronoi diagram."""
    plt.figure(figsize=(12, 10))
    plt.gca().set_aspect("equal", adjustable="box")

    if site_class == Site:
        bisector_class = PointBisector
    elif site_class == WeightedSite:
        bisector_class = WeightedPointBisector

    # Sites.
    for site in voronoi_diagram.sites:
        for limit_site in limit_sites:
            if is_equal_limit_site(site, limit_site, bisector_class=bisector_class):
                break
        else:
            plot_site(site, site_class)

    # Diagram.
    plot_vertices_and_bisectors(
        voronoi_diagram, limit_sites, xlim, ylim, bisector_class
    )

    plt.xlim(*xlim)
    plt.ylim(*ylim)
    plt.show()
