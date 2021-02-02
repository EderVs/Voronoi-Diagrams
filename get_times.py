"""Get execution times."""

# Standard Library
from typing import List, Optional
from decimal import Decimal
import time
from random import random


# Voronoi Diagrams
from voronoi_diagrams.fortunes_algorithm import (
    FortunesAlgorithm,
    AUTOMATIC_MODE,
)
from voronoi_diagrams.models import Point

# Plot
from plots.plot_utils.voronoi_diagram import SiteToUse


VORONOI_DIAGRAM_TYPE = 1
AW_VORONOI_DIAGRAM_TYPE = 2


def get_diagram_and_time(sites: List[SiteToUse], type_vd: int,) -> None:
    """Get and plot Voronoi Diagram depending on the requested type."""
    start_time = time.time()
    if type_vd == VORONOI_DIAGRAM_TYPE:
        FortunesAlgorithm.calculate_voronoi_diagram(sites)
    elif type_vd == AW_VORONOI_DIAGRAM_TYPE:
        FortunesAlgorithm.calculate_aw_voronoi_diagram(sites)

    return time.time() - start_time


def get_sites_to_use(n: int, type_vd: int) -> Optional[List[SiteToUse]]:
    """Get sites to use and limit_sites."""
    sites = []
    if type_vd not in [1, 2]:
        return None

    for _ in range(n):
        if type_vd == VORONOI_DIAGRAM_TYPE:
            x, y = (Decimal(random() * 200 - 100), Decimal(random() * 200 - 100))
            site_point = Point(x, y)
            sites.append(site_point)
        elif type_vd == AW_VORONOI_DIAGRAM_TYPE:
            decimals = Decimal("4")
            multiplier = Decimal("10") ** decimals
            x, y, w = (
                Decimal(random() * 200 - 100),
                Decimal(random() * 200 - 100),
                Decimal(random() * 10),
            )
            x = Decimal(int(x * multiplier) / multiplier)
            y = Decimal(int(y * multiplier) / multiplier)
            w = Decimal(int(w * multiplier) / multiplier)
            site_point = Point(x, y)
            sites.append((site_point, w))

    return sites


def execute_x_times(times: int, n: int) -> Decimal:
    print("Executing", n, " sites in Voronoi Diagrams")
    total_vd_time = Decimal(0)
    for _ in range(times):
        print("|")
        sites = get_sites_to_use(n, VORONOI_DIAGRAM_TYPE)
        total_vd_time += Decimal(get_diagram_and_time(sites, VORONOI_DIAGRAM_TYPE))
    average_vd_time = total_vd_time / Decimal(times)
    print("Average VD time:", average_vd_time)

    print("Executing", n, " weighted sites in AW Voronoi Diagrams")
    total_aw_vd_time = Decimal(0)
    for _ in range(times):
        print("|")
        sites = get_sites_to_use(n, AW_VORONOI_DIAGRAM_TYPE)
        total_aw_vd_time += Decimal(
            get_diagram_and_time(sites, AW_VORONOI_DIAGRAM_TYPE)
        )
    average_aw_vd_time = total_aw_vd_time / Decimal(times)
    print("Average AW VD time:", average_aw_vd_time)


if __name__ == "__main__":
    times = 10
    for i in range(1, 5):
        print("New Iteration -------------------------------------")
        execute_x_times(times, 10 ** i)
