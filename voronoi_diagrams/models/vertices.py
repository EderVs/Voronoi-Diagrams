"""Vertices in Voronoi Diagram."""

# Standard Library
from typing import List, Any, Optional
from xml.etree import ElementTree as ET

# Models
from .points import Point
from .edges import Edge


class Vertex:
    """Vertex representation in the Voronoi diagram."""

    point: Point
    edges: List[Edge]

    def __init__(self, point: Point, edges: Optional[List[Edge]] = None) -> None:
        """Constructor."""
        self.point = point
        if edges is None:
            edges = []
        self.edges = edges

    def __eq__(self, other: "Vertex") -> bool:
        """Equallity between Vertices."""
        return self.point == other.vertex

    def __str__(self) -> str:
        """Return string representation."""
        return f"V({str(self.point)})"

    def __repr__(self) -> str:
        """Return string representation."""
        return self.__str__()

    def add_edge(self, edge: Edge) -> List[Edge]:
        """Add bisector adjacent to this vertex."""
        self.edges.append(edge)
        return self.edges

    def get_xml(self, i: int) -> str:
        """Get XML representation."""
        xml_str = ""
        label_x = "v_{{{0}x}}".format(i)
        value_x = "{}".format(self.point.x)
        xml_str += self.get_xml_element_value(label_x, value_x) + "\n"
        label_y = "v_{{{0}y}}".format(i)
        value_y = "{}".format(self.point.y)
        xml_str += self.get_xml_element_value(label_y, value_y) + "\n"

        label_point = "v_{{{0}}}".format(i)
        exp = "({0}, {1})".format(label_x, label_y)
        xml_str += self.point.get_xml(label_point, exp) + "\n"
        return xml_str

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
