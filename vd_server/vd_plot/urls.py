"""VD Plot urls."""

from django.contrib import admin
from django.urls import path, include
from .views import MainView

urlpatterns = [path("", MainView.as_view(), name="main")]
