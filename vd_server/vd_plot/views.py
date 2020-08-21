from django.shortcuts import render
from django.views import View


class MainView(View):
    """Main View."""

    template = "vd_plot/main.html"

    def get(self, request):
        """GET method."""
        return render(request, self.template)
