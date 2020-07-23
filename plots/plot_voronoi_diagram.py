"""Plot voronoi diagram."""

from typing import List, Any

from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm
from voronoi_diagrams.models import Point, WeightedSite

from plots.plot_utils.voronoi_diagram import plot_voronoi_diagram, SiteToUse, Limit

from decimal import Decimal


def get_limit_sites(
    xlim: Limit, ylim: Limit, sites: List[SiteToUse], type_vd: int
) -> List[SiteToUse]:
    """Get limit sites."""
    to_return = []
    x0, x1 = xlim
    mid_x = (x0 + x1) / Decimal("2")
    y0, y1 = ylim
    mid_y = (y0 + y1) / Decimal("2")
    min_x_site = sites[0]
    max_x_site = sites[0]
    min_y_site = sites[0]
    max_y_site = sites[0]
    if type_vd == 1:
        for point in sites:
            if point.x < min_x_site.x:
                min_x_site = point
            if point.x > max_x_site.x:
                max_x_site = point
            if point.y < min_y_site.y:
                min_y_site = point
            if point.y > max_y_site.y:
                max_y_site = point
        # X
        if x0 >= min_x_site.x:
            x0_site = Point(min_x_site.x - 1, min_x_site.y)
        else:
            x0_site = Point(x0 - (min_x_site.x - x0), min_x_site.y)
        if x1 <= min_x_site.x:
            x1_site = Point(max_x_site.x + 1, max_x_site.y)
        else:
            x1_site = Point(x1 + (x1 - max_x_site.x), max_x_site.y)
        # Y
        if y0 >= min_y_site.y:
            y0_site = Point(min_y_site.x, min_y_site.y - 1)
        else:
            y0_site = Point(min_y_site.x, y0 - (min_y_site.y - y0))
        if y1 <= min_y_site.x:
            y1_site = Point(max_y_site.x, max_y_site.y + 1)
        else:
            y1_site = Point(max_y_site.x, y1 + (y1 - max_y_site.y))
        to_return = [x0_site, x1_site, y0_site, y1_site]
    elif type_vd == 2:
        for point, weight in sites:
            if point.x + weight < min_x_site[0].x + min_x_site[1]:
                min_x_site = (point, weight)
            if point.x - weight > max_x_site[0].x - max_x_site[1]:
                max_x_site = (point, weight)
            if point.y + weight < min_y_site[0].y + min_y_site[1]:
                min_y_site = (point, weight)
            if point.y - weight > max_y_site[0].y - min_y_site[1]:
                max_y_site = (point, weight)
        # X
        if x0 >= min_x_site[0].x:
            x0_site = (Point(min_x_site[0].x - 1, min_x_site[0].y), min_x_site[1])
        else:
            x0_site = (
                Point(x0 - (min_x_site[0].x - x0), min_x_site[0].y),
                min_x_site[1],
            )
        if x1 <= min_x_site[0].x:
            x1_site = (Point(max_x_site[0].x + 1, max_x_site[0].y), max_x_site[1])
        else:
            x1_site = (
                Point(x1 + (x1 - max_x_site[0].x), max_x_site[0].y),
                max_x_site[1],
            )
        # Y
        if y0 >= min_y_site[0].y:
            y0_site = (Point(min_y_site[0].x, min_y_site[0].y - 1), min_y_site[1])
        else:
            y0_site = (
                Point(min_y_site[0].x, y0 - (min_y_site[0].y - y0)),
                min_y_site[1],
            )
        if y1 <= min_y_site[0].x:
            y1_site = (Point(max_y_site[0].x, max_y_site[0].y + 1), max_y_site[1])
        else:
            y1_site = (
                Point(max_y_site[0].x, y1 + (y1 - max_y_site[0].y)),
                max_y_site[1],
            )
        to_return = [x0_site, x1_site, y0_site, y1_site]

    return to_return


if __name__ == "__main__":
    print("1) Voronoi Diagram")
    print("2) AW Voronoi Diagram")
    type_vd = int(input())

    # Get limits
    print(
        "Insert limits this way: x_min x_max y_min y_max (-100 100 -100 100 if blank)"
    )
    limits = input()
    if not limits:
        limits = "-100 100 -100 100"
    x_min, x_max, y_min, y_max = list(map(Decimal, limits.split()))
    xlim = (x_min, x_max)
    ylim = (y_min, y_max)

    # Get sites.
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

        limit_sites = get_limit_sites(xlim, ylim, sites, type_vd)
        sites += limit_sites
        if type_vd == 1:
            voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(sites)
            plot_voronoi_diagram(voronoi_diagram, limit_sites, xlim, ylim)
        elif type_vd == 2:
            voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(sites)
            plot_voronoi_diagram(
                voronoi_diagram, limit_sites, xlim, ylim, site_class=WeightedSite
            )
