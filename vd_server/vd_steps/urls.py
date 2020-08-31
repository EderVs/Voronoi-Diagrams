"""VD steps urls."""

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("plot-next/", views.PlotNextStepView.as_view(), name="plot_next"),
    path("first-step/", views.FirstStepView.as_view(), name="first_step"),
]
