"""VD steps utils."""

# Standard Library
from typing import Any, Dict

# Voronoi Diagrams
from voronoi_diagrams.models import Event, Region, Boundary


def get_event_dict(event: Event) -> Dict[str, Any]:
    """Get event dict."""
    final_event_dict = {}
    event_dict = event.__dict__.copy()
    final_event_dict["point"] = event.point.__dict__.copy()
    final_event_dict["is_site"] = event.is_site
    final_event_dict["name"] = event.name
    final_event_dict["event_str"] = event.get_event_str()
    if event.is_site and "weight" in event_dict:
        final_event_dict["weight"] = event_dict["weight"]
    return final_event_dict


def get_boundary_dict(boundary: Boundary) -> Dict[str, Any]:
    """Get boundary dict."""
    final_boundary_dict = {}
    final_boundary_dict["sign"] = boundary.sign
    final_boundary_dict["sites"] = []
    final_boundary_dict["active"] = boundary.active
    final_boundary_dict["is_to_be_deleted"] = boundary.is_to_be_deleted
    for site in boundary.bisector.get_sites_tuple():
        final_boundary_dict["sites"].append(get_event_dict(site))

    return final_boundary_dict


def get_region_dict(region: Region) -> Dict[str, Any]:
    """Get region dict."""
    final_region_dict = {}
    final_region_dict["active"] = region.active
    final_region_dict["is_to_be_deleted"] = region.is_to_be_deleted
    # Site
    final_region_dict["site"] = get_event_dict(region.site)
    # Boundaries
    if region.left is None:
        final_region_dict["left"] = None
    else:
        final_region_dict["left"] = get_boundary_dict(region.left)
    if region.right is None:
        final_region_dict["right"] = None
    else:
        final_region_dict["right"] = get_boundary_dict(region.right)

    return final_region_dict
