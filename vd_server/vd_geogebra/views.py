"""Geogebra views."""
import json
import tempfile
from django.http.response import HttpResponse

from django.views import View

from django import http

from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm
from voronoi_diagrams.models import Point
from vd_steps import db

from decimal import Decimal
from zipfile import ZipFile


class GetGeogebraGGP(View):
    """Get geogebra ggp file."""

    def get(self, request):
        """Get voronoi diagram."""
        session = request.GET.get("session")

        if not session:
            return http.HttpResponseBadRequest()

        if not db.is_vd_finished(session):
            return http.HttpResponseBadRequest()

        vd = db.get_vd(session)
        all_xml = vd.get_xml()
        temp_dir = tempfile.TemporaryDirectory()
        with open(temp_dir.name + "/" + "geogebra.xml", "wb") as t_file:
            t_file.write(bytes(all_xml, "utf-8"))
            with ZipFile(temp_dir.name + "/" + "voronoi_diagram.ggb", "w") as zip:
                zip.write(t_file.name, "geogebra.xml")
        with open(temp_dir.name + "/" + "voronoi_diagram.ggb", "rb") as z_file:
            res = http.HttpResponse(z_file.read(), content_type="application/zip")
            res["Content-Disposition"] = "inline;filename=voronoi_diagram.ggb"
            temp_dir.cleanup()
            return res
