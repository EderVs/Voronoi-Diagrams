"""Plot voronoi diagram."""

from typing import List, Any

from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm
from voronoi_diagrams.models import Point, WeightedSite

from plots.plot_utils.voronoi_diagram import plot_voronoi_diagram

from decimal import Decimal


def get_limit_sites(xlim, ylim, type_vd) -> List[Any]:
    """Get limit sites."""
    x0, x1 = xlim
    mid_x = (x0 + x1) / Decimal("2")
    y0, y1 = ylim
    mid_y = (y0 + y1) / Decimal("2")
    if type_vd == 1:
        return [
            Point(x0, mid_y),
            Point(x1, mid_y),
            Point(mid_x, y0),
            Point(mid_x, y1),
        ]
    elif type_vd == 2:
        return [
            (Point(x0, mid_y), Decimal(0)),
            (Point(x1, mid_y), Decimal(0)),
            (Point(mid_x, y0), Decimal(0)),
            (Point(mid_x, y1), Decimal(0)),
        ]


if __name__ == "__main__":
    print("1) Voronoi Diagram")
    print("2) AW Voronoi Diagram")
    type_vd = int(input())
    n = int(input("Insert number of sites: "))
    sites = []
    if type_vd not in [1, 2]:
        print("bye, bye")
    else:
        if type_vd == 1:
            print("Insert site this way: x y")
        elif type_vd == 2:
            print("Insert site this way: x y w")
        for i in range(n):
            if type_vd == 1:
                x, y = list(map(Decimal, input().split()))
                site_point = Point(x, y)
                sites.append(site_point)
            elif type_vd == 2:
                x, y, w = list(map(Decimal, input().split()))
                site_point = Point(x, y)
                sites.append((site_point, w))
        ylim = (Decimal(-100), Decimal(100))
        xlim = (Decimal(-100), Decimal(100))
        sites += get_limit_sites(xlim, ylim, type_vd)
        if type_vd == 1:
            voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(sites)
            plot_voronoi_diagram(voronoi_diagram, xlim, ylim)
        elif type_vd == 2:
            voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(sites)
            plot_voronoi_diagram(voronoi_diagram, xlim, ylim, site_class=WeightedSite)
