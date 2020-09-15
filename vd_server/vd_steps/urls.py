"""VD steps urls."""

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("next/", views.PlotNextStepView.as_view(), name="next_step"),
    path("first/", views.FirstStepView.as_view(), name="first_step"),
    path("prev/", views.PlotPrevStepView.as_view(), name="prev_step"),
    path("info/", views.StepInfoView.as_view(), name="step_info"),
]
