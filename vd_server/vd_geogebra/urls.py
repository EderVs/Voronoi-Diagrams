"""Geogebra urls."""

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("gpp/", views.GetGeogebraGGP.as_view(), name="gpp"),
]
