"""VD Steps View."""

# Standard Library
import json
from decimal import Decimal
from typing import Tuple, List, Any

# Django
from django.shortcuts import render, redirect, reverse
from django.views import View
from django import http

# VD
from . import db
from voronoi_diagrams.fortunes_algorithm import (
    VoronoiDiagram,
    FortunesAlgorithm,
    DYNAMIC_MODE,
)
from voronoi_diagrams.models import Point


class StepView(View):
    """Step View that will have the visitor's ip."""

    ip: str
    sites: List[Any]
    names: List[Any]
    xlim: Tuple[Decimal, Decimal]
    ylim: Tuple[Decimal, Decimal]
    vd_type: str

    def set_visitors_ip(self, request):
        """Set visitors ip."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            self.ip = x_forwarded_for.split(",")[0]
        else:
            self.ip = request.META.get("REMOTE_ADDR")

    def set_body(self, request):
        """Set body."""
        body = request.GET.get("body")
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
        elif vd_type == "aw_vd":
            for x, y, w, name in body_data["sites"]:
                sites.append((Point(Decimal(x), Decimal(y)), Decimal(w)))
                names.append(name)

        self.sites = sites
        self.names = names
        self.xlim = xlim
        self.ylim = ylim
        self.vd_type = vd_type

    def get(self, request):
        """GET method."""
        self.set_visitors_ip(request)
        err = self.set_body(request)
        if err is not None:
            return err
        return self.handle_get(request)

    def post(self, request):
        """POST method."""
        self.set_visitors_ip(request)
        return self.handle_post(request)

    def handle_get(self, request):
        """Handle GET Request."""
        raise NotImplementedError

    def handle_post(self, request):
        """Handle POST Request."""
        raise NotImplementedError


class FirstStepView(StepView):
    """Init VD and get first step."""

    def handle_get(self, request):
        """GET Method."""
        body = request.GET["body"]
        if self.vd_type == "vd":
            voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(
                self.sites,
                False,
                xlim=self.xlim,
                ylim=self.ylim,
                mode=DYNAMIC_MODE,
                names=self.names,
            )
        elif self.vd_type == "aw_vd":
            voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
                self.sites,
                False,
                xlim=self.xlim,
                ylim=self.ylim,
                mode=DYNAMIC_MODE,
                names=self.names,
            )

        db.save_vd(self.ip, voronoi_diagram)

        return redirect(f"{reverse('plot_next')}?body={body}")


class PlotNextStepView(StepView):
    """Plot next step view."""

    def handle_get(self, request):
        """GET method."""
        vd = db.get_vd(self.ip)
        if vd is None or not vd.is_next_step():
            return http.HttpResponseNotFound("")

        vd.next_step()

        return http.HttpResponse(vd)
