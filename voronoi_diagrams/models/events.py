"""Event representation."""

# Standar Library
from typing import Any, Optional, Tuple
from abc import ABCMeta, abstractmethod
from xml.etree import ElementTree as ET

# Models
from .points import Point

# Data Structures
from ..data_structures.avl_tree import AVLNode

# Math
from math import tan, atan, sin, cos
from decimal import Decimal

# Conic Sections
from conic_sections.utils.circle import get_circle_formula_x, get_circle_formula_y

# Types
Coordinates = Tuple[Decimal, Decimal]


class Event:
    """Event Representation. It can be either a Site or an Interception."""

    __metaclass__ = ABCMeta

    is_site: bool
    point: Point
    name: str

    def __init__(self, x: Decimal, y: Decimal, is_site: bool, name: str = ""):
        """Construct Event."""
        self.point = Point(x, y)
        self.is_site = is_site
        self.name = name

    @abstractmethod
    def get_event_point(self) -> Point:
        """Get event point to evaluate."""
        raise NotImplementedError

    @abstractmethod
    def get_str(self) -> str:
        """Get letter in str representation of event."""
        raise NotImplementedError

    def get_point_str(self) -> str:
        """Get point string representation."""
        return f"{'{0:.4f}'.format(self.point.x)}, {'{0:.4f}'.format(self.point.y)}"

    def __str__(self) -> str:
        """Get String representation."""
        event_str = self.get_str()
        return f"{self.name} {event_str}"

    def get_display_str(self) -> str:
        """Get string representation in plot."""
        return f"{self.name} S({self.get_point_str()})"

    @abstractmethod
    def get_event_str(self) -> str:
        """Get event str."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Get object representation."""
        return self.__str__()

    def get_comparison(self, event: "Event") -> Decimal:
        """Get comparison between 2 events."""
        event_point = self.get_event_point()
        other_event_point = event.get_event_point()
        if other_event_point.y == event_point.y:
            return other_event_point.x - event_point.x
        return event_point.y - other_event_point.y

    def get_xml_element_value(self, label: str, value: str) -> str:
        """Get xml element with value."""
        numeric_element = ET.Element("element")
        numeric_element.set("type", "numeric")
        numeric_element.set("label", label)
        numeric_show = ET.SubElement(numeric_element, "value")
        numeric_show.set("val", value)
        numeric_show = ET.SubElement(numeric_element, "show")
        numeric_show.set("object", "false")
        numeric_show.set("label", "true")
        numeric_obj_color = ET.SubElement(numeric_element, "objColor")
        numeric_obj_color.set("r", "0")
        numeric_obj_color.set("g", "0")
        numeric_obj_color.set("b", "0")
        numeric_obj_color.set("alpha", "0")
        numeric_layer = ET.SubElement(numeric_element, "layer")
        numeric_layer.set("val", "0")
        numeric_label_mode = ET.SubElement(numeric_element, "labelMode")
        numeric_label_mode.set("val", "1")
        numeric_line_style = ET.SubElement(numeric_element, "lineStyle")
        numeric_line_style.set("thickness", "10")
        numeric_line_style.set("type", "0")
        numeric_line_style.set("typeHidden", "1")

        numeric_xml = (
            ET.tostring(numeric_element, encoding="unicode", method="xml") + "\n"
        )
        return numeric_xml


class Site(Event):
    """Site to handle in Fortune's Algorithm.

    By itself it is just a point.
    """

    def __init__(self, x: Decimal, y: Decimal, name: str = "") -> None:
        """Construct point."""
        super(Site, self).__init__(x, y, True, name=name)

    def get_str(self):
        """Get string representation of Site."""
        return f"S({self.get_point_str()})"

    def __eq__(self, site: "Site") -> bool:
        """Get equality between sites."""
        return self.point.x == site.point.x and self.point.y == site.point.y

    def get_display_str(self) -> str:
        """Get string representation in plot."""
        return f"{self.name} S({self.get_point_str()})"

    def get_event_str(self) -> str:
        """Get event str."""
        return f"S {self.name}"

    def get_x_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the last point of the site pointing to given point."""
        return self.point.x

    def get_y_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the last point of the site pointing to given point."""
        return self.point.y

    def get_y_frontier_formula(self, x: Decimal) -> Tuple[Decimal, Decimal]:
        """Get the frontier's y coordinates given x coordinate."""
        return (self.point.y, self.point.y)

    def get_x_frontier_formula(self, x: Decimal) -> Tuple[Decimal, Decimal]:
        """Get the frontier's x coordinates given y coordinate."""
        return (self.point.x, self.point.x)

    def get_site_distance(self, x: Decimal, y: Decimal) -> Decimal:
        """Get distance to site from another point.

        In this case the site distance is the distance to the site point.
        """
        return (
            ((self.point.x - x) ** Decimal(2)) + ((self.point.y - y) ** Decimal(2))
        ).sqrt()

    def get_distance_to_site_point_from_point(self, x: Decimal, y: Decimal) -> Decimal:
        """Get distance to site point from another point."""
        return (
            ((self.point.x - x) ** Decimal(2)) + ((self.point.y - y) ** Decimal(2))
        ).sqrt()

    def get_distance_to_site_frontier_from_point(
        self, x: Decimal, y: Decimal
    ) -> Decimal:
        """Get distance to site frontier from point."""
        return self.get_distance_to_site_point_from_point(x, y)

    def get_weighted_distance(self, x: Decimal, y: Decimal) -> Decimal:
        """Get distance to site frontier from point.

        The frontier in this case is the site point itself.
        """
        return self.get_distance_to_site_point_from_point(x, y)

    def get_highest_site_point(self) -> Point:
        """Get lowest point in the site."""
        return self.point

    def get_lowest_site_point(self) -> Point:
        """Get lowest point in the site."""
        return self.point

    def get_event_point(self) -> Point:
        """Get event point to evaluate."""
        return self.get_highest_site_point()

    def is_dominated(self, site: "Site") -> bool:
        """Check if this site is dominated by other site."""
        return False

    def get_object_to_hash(self) -> Coordinates:
        """Get object to hash this site."""
        return (self.point.x, self.point.y)

    def get_xml(self) -> str:
        """Get XML representation."""
        xml_str = ""
        label_x = "p_{{{0}x}}".format(self.name)
        value_x = "{}".format(self.point.x)
        xml_str += self.get_xml_element_value(label_x, value_x) + "\n"
        label_y = "p_{{{0}y}}".format(self.name)
        value_y = "{}".format(self.point.y)
        xml_str += self.get_xml_element_value(label_y, value_y) + "\n"

        label_point = "p_{{{0}}}".format(self.name)
        exp = "({0}, {1})".format(label_x, label_y)
        xml_str += self.point.get_xml(label_point, exp) + "\n"
        return xml_str


class Intersection(Event):
    """Intersection to handle in Fortune's Algorithm."""

    vertex: Point
    region_node: AVLNode

    def __init__(self, event: Point, vertex: Point, region_node: AVLNode) -> None:
        """Construct point."""
        super(Intersection, self).__init__(event.x, event.y, False)
        self.vertex = vertex
        self.region_node = region_node

    def get_str(self) -> str:
        """Get string representation of Site."""
        return f"I({self.get_point_str()})"

    def get_event_str(self) -> str:
        """Get event str."""
        return self.get_str()

    def get_event_point(self) -> Point:
        """Get event point to evaluate."""
        return self.point


class WeightedSite(Site):
    """Weighted Site to handle in Fortune's Algorithm.

    Is a point with weight.
    """

    weight: Decimal

    def __init__(self, x: Decimal, y: Decimal, weight: Decimal, name: str = "") -> None:
        """Construct point."""
        super(WeightedSite, self).__init__(x, y, name=name)
        self.weight = weight

    def __eq__(self, site: "WeightedSite") -> bool:
        """Get equality between weighted sites."""
        return (
            self.point.x == site.point.x
            and self.point.y == site.point.y
            and self.weight == site.weight
        )

    def get_site_distance(self, x: Decimal, y: Decimal) -> Decimal:
        """Get distance to site from another point.

        In this case the site distance is the distance to the site point plus the weight.
        """
        return (
            ((self.point.x - x) ** Decimal(2)) + ((self.point.y - y) ** Decimal(2))
        ).sqrt() + abs(self.weight)

    def compare_weights(self, site: "WeightedSite") -> int:
        """Compare weight between sites."""
        if self.weight >= 0:
            return self.weight - site.weight
        else:
            return site.weight - self.weight

    def get_x_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the last point of the site pointing to given point."""
        if point.x >= self.point.x:
            sign = Decimal(1)
        else:
            sign = Decimal(-1)

        if point.x == self.point.x:
            return self.point.x

        angle = abs(atan((point.y - self.point.y) / (point.x - self.point.x)))
        x = abs(self.weight) * Decimal(cos(angle))
        return self.point.x + sign * x

    def get_x_farthest_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the farthest point of the site pointing to given point."""
        if point.x >= self.point.x:
            sign = Decimal(-1)
        else:
            sign = Decimal(1)

        if point.x == self.point.x:
            return self.point.x

        angle = abs(atan((point.y - self.point.y) / (point.x - self.point.x)))
        x = abs(self.weight) * Decimal(cos(angle))
        return self.point.x + sign * x

    def get_y_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the last point of the site pointing to given point."""
        if point.y >= self.point.y:
            sign = Decimal(1)
        else:
            sign = Decimal(-1)

        if point.x == self.point.x:
            return self.point.y + sign * self.weight

        angle = abs(atan((point.y - self.point.y) / (point.x - self.point.x)))
        y = abs(self.weight) * Decimal(sin(angle))
        return self.point.y + sign * y

    def get_y_farthest_frontier_pointing_to_point(self, point: Point) -> Decimal:
        """Get the farthest point of the site pointing to given point."""
        if point.y >= self.point.y:
            sign = Decimal(-1)
        else:
            sign = Decimal(1)

        if point.x == self.point.x:
            return self.point.y + sign * self.weight

        angle = abs(atan((point.y - self.point.y) / (point.x - self.point.x)))
        y = abs(self.weight) * Decimal(sin(angle))
        return self.point.y + sign * y

    def get_y_frontier_formula(self, x: Decimal) -> Optional[Tuple[Decimal, Decimal]]:
        """Get the frontier's y coordinates given x coordinate."""
        return get_circle_formula_y(self.point.x, self.point.y, abs(self.weight), x)

    def get_x_frontier_formula(self, y: Decimal) -> Optional[Tuple[Decimal, Decimal]]:
        """Get the frontier's x coordinates given y coordinate."""
        return get_circle_formula_x(self.point.x, self.point.y, abs(self.weight), y)

    def get_distance_to_site_frontier_from_point(
        self, x: Decimal, y: Decimal
    ) -> Decimal:
        """Get distance to site frontier from point.

        The frontier in this case is the circle given by the weight as radius.
        """
        return super(WeightedSite, self).get_distance_to_site_point_from_point(
            x, y
        ) - abs(self.weight)

    def get_weighted_distance(self, x: Decimal, y: Decimal) -> Decimal:
        """Get distance to site frontier from point.

        The frontier in this case is the circle given by the weight as radius.
        """
        return super(WeightedSite, self).get_distance_to_site_point_from_point(
            x, y
        ) + abs(self.weight)

    def get_highest_site_point(self) -> Point:
        """Get highest point in the site."""
        return Point(self.point.x, self.point.y + abs(self.weight))

    def get_lowest_site_point(self) -> Point:
        """Get lowest point in the site."""
        return Point(self.point.x, self.point.y - abs(self.weight))

    def get_str(self):
        """Get String representation."""
        return f"WS({self.get_point_str()}, {'{0:.4f}'.format(self.weight)})"

    def is_dominated(self, site: "WeightedSite") -> bool:
        """Check if this weighted site is dominated by other weighted site."""
        if self.weight >= 0:
            return self.weight >= site.get_weighted_distance(self.point.x, self.point.y)
        else:
            return abs(site.weight) >= self.get_weighted_distance(
                site.point.x, self.point.y
            )

    def get_object_to_hash(self) -> Tuple[Decimal, Decimal, Decimal]:
        """Get object to hash this site."""
        return (self.point.x, self.point.y, self.weight)

    def get_comparison(self, event: Event) -> Decimal:
        """Get comparison between 2 events."""
        if not event.is_site:
            return super().get_comparison(event)

        # We now know that event is a Weighted site.
        event_point = self.get_event_point()
        other_event_point = event.get_event_point()
        if other_event_point.y == event_point.y:
            if self.weight == event.weight:
                return other_event_point.x - event_point.x
            # The smallest site will be first.
            return self.weight - event.weight
        return event_point.y - other_event_point.y

    def get_xml(self) -> str:
        """Get xml representation."""
        wp_xml = super().get_xml() + "\n"
        label_x = "p_{{{0}x}}".format(self.name)
        label_y = "p_{{{0}y}}".format(self.name)
        label_w = "p_{{{0}w}}".format(self.name)
        value_w = "{}".format(self.weight)
        wp_xml += self.get_xml_element_value(label_w, value_w) + "\n"
        wp_xml += self.get_weight_circle_xml(label_x, label_y, label_w) + "\n"
        return wp_xml

    def get_weight_circle_xml(self, label_x, label_y, label_w) -> str:
        """Get weight circle in xml."""
        all_xml = ""
        circle_label = "w_{{{},{}}}"
        expression = "c_{{{0}}}(x, {1}, {2}, {3})"
        exp_1 = "{0}(x) = {1}".format(
            circle_label.format(self.name, "1"),
            expression.format("1", label_x, label_y, label_w),
        )
        all_xml += (
            self.get_xml_expression(circle_label.format(self.name, "1"), exp_1) + "\n"
        )

        exp_2 = "{0}(x) = {1}".format(
            circle_label.format(self.name, "2"),
            expression.format("2", label_x, label_y, label_w),
        )
        all_xml += (
            self.get_xml_expression(circle_label.format(self.name, "2"), exp_2) + "\n"
        )
        return all_xml

    def get_xml_expression(self, label, exp) -> str:
        """Get expression."""
        weight_expression = ET.Element("expression")
        weight_expression.set(
            "label", label,
        )
        weight_expression.set(
            "exp", exp,
        )

        weight_element = ET.Element("element")
        weight_element.set("type", "function")
        weight_element.set("label", label)
        weight_show = ET.SubElement(weight_element, "show")
        weight_show.set("object", "true")
        weight_show.set("label", "true")
        weight_show.set("ev", "4")
        weight_obj_color = ET.SubElement(weight_element, "objColor")
        weight_obj_color.set("r", "0")
        weight_obj_color.set("g", "0")
        weight_obj_color.set("b", "0")
        weight_obj_color.set("alpha", "0")
        weight_layer = ET.SubElement(weight_element, "layer")
        weight_layer.set("val", "0")
        weight_label_mode = ET.SubElement(weight_element, "labelMode")
        weight_label_mode.set("val", "0")
        weight_fixed = ET.SubElement(weight_element, "fixed")
        weight_fixed.set("val", "true")
        weight_line_style = ET.SubElement(weight_element, "lineStyle")
        weight_line_style.set("thickness", "5")
        weight_line_style.set("type", "0")
        weight_line_style.set("typeHidden", "1")
        weight_line_style.set("opacity", "204")

        expression_xml = (
            ET.tostring(weight_expression, encoding="unicode", method="xml")
            + "\n"
            + ET.tostring(weight_element, encoding="unicode", method="xml")
        )
        return expression_xml
