"""VD Plot urls."""

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.MainView.as_view(), name="main"),
    path("plot-vd/", views.PlotVDView.as_view(), name="plot_vd"),
]
