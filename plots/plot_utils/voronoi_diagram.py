"""Voronoi Diagram representation in plot"""

# Standard Library.
from typing import Any

# Voronoi diagrams.
from voronoi_diagrams.fortunes_algorithm import (
    VoronoiDiagram,
    VoronoiDiagramBisector,
    VoronoiDiagramVertex,
)
from voronoi_diagrams.models import (
    Site,
    WeightedSite,
    PointBisector,
    WeightedPointBisector,
)

# Plot.
from matplotlib import pyplot as plt
from plots.plot_utils.models.bisectors import plot_bisector
from plots.plot_utils.models.sites import plot_site
from plots.plot_utils.models.points import plot_point


def plot_voronoi_diagram(voronoi_diagram: VoronoiDiagram, site_class: Any = Site):
    """Plot voronoi diagram."""
    ylim = (-30, 30)
    xlim = (-30, 30)

    plt.figure()
    plt.gca().set_aspect("equal", adjustable="box")

    if site_class == Site:
        bisector_class = PointBisector
    elif site_class == WeightedSite:
        bisector_class = WeightedPointBisector

    # Sites.
    for site in voronoi_diagram.sites:
        plot_site(site, site_class)

    plt.xlim(*xlim)
    plt.ylim(*ylim)
    plt.show()
