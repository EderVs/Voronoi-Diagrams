""" VD Steps View. """

# Django
from django.shortcuts import render
from django.views import View
from django import http


class StepView(View):
    """Step View that will have the visitor's ip."""

    ip: str

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
        self.handle_post(request)

    def handle_get(self, request):
        """Handle GET Request."""
        raise NotImplementedError

    def handle_post(self, request):
        """Handle POST Request."""
        raise NotImplementedError


class PlotNextStepView(StepView):
    """Plot next step view."""

    def handle_get(self, request):
        """GET method."""
        print(self.ip)
        return http.HttpResponse(self.ip)
