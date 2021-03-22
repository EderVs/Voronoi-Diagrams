"""Site Representation."""
# Standard Library
from typing import Tuple
from xml.etree import ElementTree as ET

# Math
from decimal import Decimal

Coordinates = Tuple[Decimal, Decimal]


class Point:
    """Point representation."""

    x: Decimal
    y: Decimal

    def __init__(self, x: Decimal, y: Decimal) -> None:
        """Construct point."""
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """Get String representation."""
        return f"{'{0:.4f}'.format(self.x)}, {'{0:.4f}'.format(self.y)}"

    def __repr__(self) -> str:
        """Get object representation."""
        return self.__str__()

    def __eq__(self, point: "Point") -> str:
        """Get equality between points."""
        return self.x == point.x and self.y == point.y

    def get_tuple(self) -> Coordinates:
        """Get tuple of coordinates (x, y)."""
        return (self.x, self.y)

    def get_xml(self, label, exp) -> str:
        """Get xml representation."""
        point_expression = ET.Element("expression")
        point_expression.set(
            "label", label,
        )
        point_expression.set("exp", exp)
        point_expression.set("type", "point")

        """
        <expression label="G" exp="(p_{x}, p_{y})" type="point" />
        <element type="point" label="G">
            <show object="true" label="true"/>
            <objColor r="0" g="0" b="0" alpha="0"/>
            <layer val="0"/>
            <labelMode val="0"/>
            <pointSize val="5"/>
            <pointStyle val="0"/>
        </element>
        """
        point_element = ET.Element("element")
        point_element.set("type", "point")
        point_element.set("label", label)
        point_show = ET.SubElement(point_element, "show")
        point_show.set("object", "true")
        point_show.set("label", "true")
        point_obj_color = ET.SubElement(point_element, "objColor")
        point_obj_color.set("r", "0")
        point_obj_color.set("g", "0")
        point_obj_color.set("b", "0")
        point_obj_color.set("alpha", "0")
        point_layer = ET.SubElement(point_element, "layer")
        point_layer.set("val", "0")
        point_label_mode = ET.SubElement(point_element, "labelMode")
        point_label_mode.set("val", "0")
        point_size = ET.SubElement(point_element, "pointSize")
        point_size.set("val", "5")
        point_style = ET.SubElement(point_element, "pointStyle")
        point_style.set("val", "0")

        expression_xml = (
            ET.tostring(point_expression, encoding="unicode", method="xml")
            + "\n"
            + ET.tostring(point_element, encoding="unicode", method="xml")
            + "\n"
        )
        return expression_xml
