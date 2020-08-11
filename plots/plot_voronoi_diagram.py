"""Plot voronoi diagram."""

# Standard Library
from typing import List, Any, Tuple, Optional
from decimal import Decimal
import time
from random import random


# Voronoi Diagrams
from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm
from voronoi_diagrams.models import Point, WeightedSite

# Plot
from plots.plot_utils.voronoi_diagram import plot_voronoi_diagram, SiteToUse, Limit


VORONOI_DIAGRAM_TYPE = 1
AW_VORONOI_DIAGRAM_TYPE = 2


def get_limit_sites(
    xlim: Limit, ylim: Limit, sites: List[SiteToUse], type_vd: int
) -> List[SiteToUse]:
    """Get limit sites."""
    to_return = []
    x0, x1 = xlim
    y0, y1 = ylim
    min_x_site = sites[0]
    max_x_site = sites[0]
    min_y_site = sites[0]
    max_y_site = sites[0]

    if type_vd == VORONOI_DIAGRAM_TYPE:
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

    elif type_vd == AW_VORONOI_DIAGRAM_TYPE:
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


def get_limits() -> Tuple[Limit, Limit]:
    """Get Limits to used in the plot."""
    print(
        "Insert limits this way: x_min x_max y_min y_max (-100 100 -100 100 if blank)"
    )
    limits = input()
    if not limits:
        limits = "-100 100 -100 100"
    x_min, x_max, y_min, y_max = list(map(Decimal, limits.split()))
    xlim = (x_min, x_max)
    ylim = (y_min, y_max)
    return (xlim, ylim)


def get_diagram_and_plot(
    sites: List[SiteToUse],
    limit_sites: List[SiteToUse],
    xlim: Limit,
    ylim: Limit,
    type_vd: int,
    plot_steps: bool = False,
    plot_diagram: bool = False,
) -> None:
    """Get and plot Voronoi Diagram depending on the requested type."""
    sites += limit_sites
    # print(limit_sites)  # Debugging
    start_time = time.time()
    if type_vd == VORONOI_DIAGRAM_TYPE:
        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(
            sites, plot_steps=plot_steps, xlim=xlim, ylim=ylim
        )
        print("--- %s seconds to calculate diagram. ---" % (time.time() - start_time))
        if plot_diagram:
            plot_voronoi_diagram(voronoi_diagram, limit_sites, xlim, ylim)
    elif type_vd == AW_VORONOI_DIAGRAM_TYPE:
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            sites, plot_steps=plot_steps, xlim=xlim, ylim=ylim
        )
        print("--- %s seconds to calculate diagram. ---" % (time.time() - start_time))
        if plot_diagram:
            plot_voronoi_diagram(
                voronoi_diagram, limit_sites, xlim, ylim, site_class=WeightedSite
            )


def get_sites_to_use(type_vd: int, random_sites: bool) -> Optional[List[SiteToUse]]:
    """Get sites to use and limit_sites."""
    n = int(input("Insert number of sites: "))
    sites = []
    if type_vd not in [1, 2]:
        return None

    if type_vd == VORONOI_DIAGRAM_TYPE and not random_sites:
        print("Insert site this way: x y")
    elif type_vd == AW_VORONOI_DIAGRAM_TYPE and not random_sites:
        print("Insert site this way: x y w")
    for _ in range(n):
        if type_vd == VORONOI_DIAGRAM_TYPE:
            if random_sites:
                x, y = (Decimal(random() * 200 - 100), Decimal(random() * 200 - 100))
            else:
                x, y = list(map(Decimal, input().split()))
            site_point = Point(x, y)
            sites.append(site_point)
        elif type_vd == AW_VORONOI_DIAGRAM_TYPE:
            if random_sites:
                x, y, w = (
                    Decimal(random() * 200 - 100),
                    Decimal(random() * 200 - 100),
                    Decimal(random() * 10),
                )
            else:
                x, y, w = list(map(Decimal, input().split()))
            site_point = Point(x, y)
            sites.append((site_point, w))

    return sites


def get_type_of_voronoi_diagram() -> int:
    """Get type of voronoi diagram."""
    print("1) Voronoi Diagram")
    print("2) AW Voronoi Diagram")
    type_vd = int(input())
    return type_vd


def get_if_random_sites() -> bool:
    """Get if there will be random sites."""
    print("Random? 1/0")
    random_sites = bool(int(input()))
    return random_sites


def get_if_plot_steps() -> bool:
    """Get if each step in the voronoi diagram will be plot."""
    print("Plot steps? 1/0")
    plot_steps = bool(int(input()))
    return plot_steps


def get_if_plot_diagram() -> bool:
    """Get if the voronoi diagram will be plot."""
    print("Plot Diagram? 1/0")
    plot_diagram = bool(int(input()))
    return plot_diagram


if __name__ == "__main__":
    type_vd = get_type_of_voronoi_diagram()
    xlim, ylim = get_limits()
    random_sites = get_if_random_sites()
    plot_diagram = get_if_plot_diagram()
    plot_steps = get_if_plot_steps()
    sites = get_sites_to_use(type_vd, random_sites)
    if sites is None:
        print("Bye bye")
    else:
        # limit_sites = get_limit_sites(xlim, ylim, sites, type_vd)
        limit_sites = []
        get_diagram_and_plot(
            sites,
            limit_sites,
            xlim,
            ylim,
            type_vd,
            plot_steps=plot_steps,
            plot_diagram=plot_diagram,
        )
