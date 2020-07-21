"""Plot voronoi diagram."""

from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm
from voronoi_diagrams.models import Point, WeightedSite

from plots.plot_utils.voronoi_diagram import plot_voronoi_diagram

from decimal import Decimal

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
        if type_vd == 1:
            voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(sites)
            plot_voronoi_diagram(voronoi_diagram)
        elif type_vd == 2:
            voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(sites)
            plot_voronoi_diagram(voronoi_diagram, site_class=WeightedSite)
