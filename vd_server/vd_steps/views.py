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

    def get(self, request):
        """GET method."""
        self.set_visitors_ip(request)
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

    def handle_get(self, request):
        """GET Method."""
        err = self.set_body(request)
        if err is not None:
            return err

        db.save_vd(self.ip, self.sites, self.names, self.xlim, self.ylim, self.vd_type)
        step, ok = db.get_current_step(self.ip)
        if not ok:
            return http.HttpResponseNotFound()

        return http.HttpResponse(step)


class PlotNextStepView(StepView):
    """Plot next step view."""

    def handle_get(self, request):
        """GET method."""
        step, ok = db.get_next_step(self.ip)
        if not ok:
            return http.HttpResponseNotFound()

        return http.HttpResponse(step)


class PlotPrevStepView(StepView):
    """Plot prev step view."""

    def handle_get(self, request):
        """GET method."""
        step, ok = db.get_prev_step(self.ip)
        if not ok:
            return http.HttpResponseNotFound()

        return http.HttpResponse(step)


class StepInfoView(StepView):
    """Step info view."""

    def handle_get(self, request):
        """GET method."""
        vd = db.get_vd(self.ip)
        response = {"is_next_step": vd.is_next_step()}

        return http.HttpResponse(response)
