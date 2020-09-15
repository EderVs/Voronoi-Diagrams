"""VD steps utils."""

# Standard Library
from typing import Any, Dict

# Voronoi Diagrams
from voronoi_diagrams.models import Event


def get_event_dict(event: Event) -> Dict[str, Any]:
    """Get event dict."""
    final_event_dict = {}
    event_dict = event.__dict__.copy()
    final_event_dict["point"] = event.point.__dict__.copy()
    final_event_dict["is_site"] = event.is_site
    final_event_dict["name"] = event.name
    if event.is_site and "weight" in event_dict:
        final_event_dict["weight"] = event_dict["weight"]
    return final_event_dict
