"""VD Plot views."""

from typing import Dict
import json

from django.shortcuts import render
from django.views import View

from django import http

from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm
from voronoi_diagrams.models import Point
from plots.plot_utils.voronoi_diagram import get_vd_html
from vd_steps import db

from decimal import Decimal

voronoi_diagrams: Dict[int, FortunesAlgorithm] = {}


class MainView(View):
    """Main View."""

    template = "vd_plot/main.html"

    def get(self, request):
        """GET method."""
        return render(request, self.template)


class PlotVDView(View):
    """Plot Voronoi Diagram View."""

    def get(self, request):
        """Get voronoi diagram."""
        session = request.GET.get("session")
        if not session:
            return http.HttpResponseBadRequest()

        # TODO: Add serializer of sites.
        body = request.GET["body"]
        if not body:
            return http.HttpResponseNotFound()

        body_data = json.loads(body)
        if not body_data.get("sites", False):
            return http.HttpResponseNotFound()

        sites = []
        names = []

        vd_type = body_data.get("vd_type", "vd")
        xlim = (
            Decimal(body_data.get("limit_x0", "-100")),
            Decimal(body_data.get("limit_x1", "100")),
        )
        ylim = (
            Decimal(body_data.get("limit_y0", "-100")),
            Decimal(body_data.get("limit_y1", "100")),
        )
        if vd_type == "vd":
            for x, y, name in body_data["sites"]:
                sites.append(Point(Decimal(x), Decimal(y)))
                names.append(name)
            voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(
                sites, False, xlim=xlim, ylim=ylim, names=names
            )
        elif vd_type == "aw_vd":
            for x, y, w, name in body_data["sites"]:
                sites.append((Point(Decimal(x), Decimal(y)), Decimal(w)))
                names.append(name)
            voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
                sites, False, xlim=xlim, ylim=ylim, names=names
            )

        db.save_vd_completed(session, voronoi_diagram, xlim, ylim)
        step, ok = db.get_current_step(session)
        if not ok:
            return http.HttpResponseNotFound()

        return http.HttpResponse(step)
