"""VD Plot views."""

from typing import Dict
import json

from django.shortcuts import render
from django.views import View

from django import http

from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm, VoronoiDiagram
from voronoi_diagrams.models import Point
from plots.plot_utils.voronoi_diagram import get_vd_html

from decimal import Decimal

voronoi_diagrams: Dict[int, VoronoiDiagram] = {}


class MainView(View):
    """Main View."""

    template = "vd_plot/main.html"

    def get(self, request):
        """GET method."""
        return render(request, self.template)


class PlotVDView(View):
    """Main View."""

    def get(self, request):
        """Get voronoi diagram."""
        # TODO: Add serializer of sites.
        body_unicode = request.body.decode("utf-8")
        if not body_unicode:
            return http.HttpResponseNotFound()

        body_data = json.loads(body_unicode)
        if not body_data.get("sites", False):
            return http.HttpResponseNotFound()

        sites = []
        names = []
        for x, y, name in body_data["sites"]:
            sites.append(Point(Decimal(x), Decimal(y)))
            names.append(name)

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(
            sites, False, names=names
        )
        plot_div = get_vd_html(
            voronoi_diagram,
            [],
            (Decimal(-100), Decimal(100)),
            (Decimal(-100), Decimal(100)),
        )
        return http.HttpResponse(plot_div)
