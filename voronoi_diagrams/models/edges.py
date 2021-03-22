"""Bisectors Representations in the Voronoi Diagram."""

from abc import abstractmethod
from typing import Tuple, Any, Optional, List, Iterable
from decimal import Decimal
import numpy as np
from xml.etree import ElementTree as ET

# Models
from .bisectors import Bisector, PointBisector, WeightedPointBisector
from .boundaries import Boundary, PointBoundary, WeightedPointBoundary

# Ranges
# Bisector side is set to be an int if there is other sides when using other type of sites.
BisectorSide = int
# Each range must have the same Bisector Side.
Range = Tuple[Optional[Decimal], Optional[Decimal], BisectorSide]


Vertex = "vertices.Vertex"


class Edge:
    """Edge representation in the Voronoi diagram."""

    bisector: Bisector
    vertices: List[Vertex]
    ranges_b_plus: List[Range]
    ranges_b_minus: List[Range]
    boundary_plus: Boundary
    boundary_minus: Boundary
    ranges_vertical: List[Tuple[Optional[Decimal], Optional[Decimal]]]

    def __init__(
        self,
        bisector: Any,
        boundary_plus: Boundary,
        boundary_minus: Boundary,
        vertex1: Vertex = None,
        vertex2: Vertex = None,
    ) -> None:
        """Constructor."""
        self.bisector = bisector
        self.vertices = []
        if vertex1 is not None:
            self.vertices.append(vertex1)
        if vertex2 is not None:
            self.vertices.append(vertex2)
        self.ranges_b_plus = []
        self.ranges_b_minus = []
        self.ranges_vertical = []
        self.boundary_plus = boundary_plus
        self.boundary_minus = boundary_minus

    def __eq__(self, other: "Edge") -> bool:
        """Equallity between VoronoiDiagramBisectors."""
        return self.bisector == other.bisector and (
            (self.vertex1 == other.vertex1 and self.vertex2 == other.vertex2)
            or (self.vertex1 == other.vertex2 and self.vertex2 == other.vertex1)
        )

    def __str__(self) -> str:
        """Return string representation."""
        return f"B({str(self.bisector)}, {str(self.vertices)})"

    def is_to_the_infinity(self) -> bool:
        """Check if the bisector doesn't have one vertex."""
        return len(self.vertices) != 2

    def get_vertices(self) -> Tuple[Vertex, Vertex]:
        """Get vertices linked to this bisector."""
        if len(self.vertices) == 0:
            vertex1 = None
            vertex2 = None
        elif len(self.vertices) == 1:
            vertex1 = self.vertices[0]
            vertex2 = None
        else:
            if self.vertices[0].vertex.y > self.vertices[1].vertex.y or (
                self.vertices[0].vertex.y == self.vertices[1].vertex.y
                and self.vertices[0].vertex.x > self.vertices[1].vertex.x
            ):
                vertex1 = self.vertices[1]
                vertex2 = self.vertices[0]
            else:
                vertex1 = self.vertices[0]
                vertex2 = self.vertices[1]

        return (vertex1, vertex2)

    def add_vertex(self, vertex: Vertex):
        """Add vertex."""
        if len(self.vertices) >= 2:
            return
        self.vertices.append(vertex)

    def get_x(self, y: Decimal) -> Optional[Decimal]:
        """Get x given y of the bisector.

        Used in vertical bisectors.
        """
        xs = self.bisector.formula_x(y)
        if len(xs) == 0:
            return None
        return xs[0]

    def get_ranges(
        self, xlim: Tuple[Decimal, Decimal], ylim: Tuple[Decimal, Decimal]
    ) -> Tuple[List[Optional[Decimal]], List[Optional[Decimal]]]:
        """Get Ranges to plot."""
        x_ranges = []
        y_ranges = []
        num_steps = Decimal("50")

        self.complete_ranges()
        if self.bisector.is_vertical():
            x_ranges, y_ranges = self.get_ranges_when_bisector_is_vertical(
                num_steps, xlim, ylim
            )
        else:
            x_ranges, y_ranges = self.get_ranges_when_bisector_is_not_vertical(
                num_steps, xlim, ylim
            )

        if len(x_ranges) == 0 or len(y_ranges) == 0:
            ranges = ([], [])
        else:
            ranges = (np.concatenate(x_ranges), np.concatenate(y_ranges))
        return ranges

    def get_ranges_when_bisector_is_vertical(
        self,
        num_steps: Decimal,
        xlim: Tuple[Decimal, Decimal],
        ylim: Tuple[Decimal, Decimal],
    ) -> Tuple[List[Iterable[Any]], List[Iterable[Any]]]:
        """Get ranges when bisector is vertical."""
        x_ranges = []
        y_ranges = []
        for y0, y1 in self.ranges_vertical:
            if y0 is None:
                y0 = ylim[0]
            if y1 is None:
                y1 = ylim[1]
            step = abs(y0 - y1) / num_steps
            if step > 0:
                y_range = np.arange(y0, y1, step)
                x_range = [self.get_x(y) for y in y_range]
                x_ranges.append(x_range)
                y_ranges.append(y_range)
            else:
                x_ranges.append([])
                y_ranges.append([])
        return (x_ranges, y_ranges)

    def get_ranges_when_bisector_is_not_vertical(
        self,
        num_steps: Decimal,
        xlim: Tuple[Decimal, Decimal],
        ylim: Tuple[Decimal, Decimal],
    ) -> Tuple[List[Iterable[Any]], List[Iterable[Any]]]:
        """Get ranges when bisector is not vertical."""
        x_ranges = []
        y_ranges = []
        for x1, x0, side in self.ranges_b_minus[::-1]:
            if x0 is None:
                if side == 0:
                    x0 = xlim[0]
                else:
                    x0 = xlim[1]
            self.get_ranges_in_general(x_ranges, y_ranges, x0, x1, side, num_steps)
        for x0, x1, side in self.ranges_b_plus:
            if x1 is None:
                if side == 0:
                    x1 = xlim[1]
                else:
                    x1 = xlim[0]
            self.get_ranges_in_general(x_ranges, y_ranges, x0, x1, side, num_steps)
        return (x_ranges, y_ranges)

    def get_ranges_in_general(
        self,
        x_ranges: List[Iterable[Any]],
        y_ranges: List[Iterable[Any]],
        x0: Decimal,
        x1: Decimal,
        side: int,
        num_steps: Decimal,
    ) -> None:
        """Get ranges in general."""
        step = abs(x0 - x1) / num_steps
        if step > 0:
            if side == 1:
                x_range = np.arange(x0, x1, -step)
            else:
                x_range = np.arange(x0, x1, step)
            y_range = []
            for x in x_range:
                y_range.append(self.get_y_by_side(x, side))
            x_ranges.append(x_range)
            y_ranges.append(y_range)
        else:
            x_ranges.append([])
            y_ranges.append([])

    @abstractmethod
    def get_y_by_side(self, w: Decimal, side: BisectorSide) -> Optional[Decimal]:
        """Get y by BisectorSide."""
        raise NotImplementedError

    def add_begin_range(
        self, x: Decimal, boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add new of the the bisector to be graphed."""
        if boundary_sign:
            self.ranges_b_plus.append((x, None, side))
        else:
            self.ranges_b_minus.append((x, None, side))

    def add_begin_range_vertical(self, y: Optional[Decimal]):
        """Add new vertical range."""
        self.ranges_vertical.append((y, None))

    @abstractmethod
    def add_end_range(
        self, x: Decimal, boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add end of the bisector to be ploted."""
        raise NotImplementedError

    def add_end_range_vertical(self, y: Decimal):
        """Add end of the vertical range."""
        self.ranges_vertical[-1] = (self.ranges_vertical[-1][0], y)

    @abstractmethod
    def complete_ranges(self):
        """Add a new range if neccessary."""
        raise NotImplementedError

    @abstractmethod
    def get_xml(self) -> str:
        """Get xml representation of the edge.

        The xml representation is based on Geogebra ggb xml.
        Docs: https://wiki.geogebra.org/en/Reference:XML
        """
        raise NotImplementedError

    def create_xml_expression(self, label, condition, expression):
        """Something."""
        exp_str = "{0} = If[{1}, {2}]".format(label, condition, expression)

        edge_expression = ET.Element("expression")
        edge_expression.set(
            "label", label,
        )
        edge_expression.set(
            "exp", exp_str,
        )

        edge_element = ET.Element("element")
        edge_element.set("type", "function")
        edge_element.set("label", label)
        edge_show = ET.SubElement(edge_element, "show")
        edge_show.set("object", "true")
        edge_show.set("label", "true")
        edge_show.set("ev", "4")
        edge_obj_color = ET.SubElement(edge_element, "objColor")
        edge_obj_color.set("r", "0")
        edge_obj_color.set("g", "0")
        edge_obj_color.set("b", "0")
        edge_obj_color.set("alpha", "0")
        edge_layer = ET.SubElement(edge_element, "layer")
        edge_layer.set("val", "0")
        edge_label_mode = ET.SubElement(edge_element, "labelMode")
        edge_label_mode.set("val", "0")
        edge_fixed = ET.SubElement(edge_element, "fixed")
        edge_fixed.set("val", "true")
        edge_line_style = ET.SubElement(edge_element, "lineStyle")
        edge_line_style.set("thickness", "5")
        edge_line_style.set("type", "0")
        edge_line_style.set("typeHidden", "1")
        edge_line_style.set("opacity", "204")

        expression_xml = (
            ET.tostring(edge_expression, encoding="unicode", method="xml")
            + "\n"
            + ET.tostring(edge_element, encoding="unicode", method="xml")
        )
        return expression_xml


class PointBisectorEdge(Edge):
    """Point Bisector Edge representation in Voronoi Diagram."""

    bisector: PointBisector
    boundary_plus: PointBoundary
    boundary_minus: PointBoundary

    def __init__(
        self,
        bisector: PointBisector,
        boundary_plus: PointBoundary,
        boundary_minus: PointBoundary,
        vertex1: Any = None,
        vertex2: Any = None,
    ) -> None:
        """Create Voronoi Diagram Weighted Bisector."""
        super().__init__(bisector, boundary_plus, boundary_minus, vertex1, vertex2)

    def add_end_range(
        self, x: Decimal, boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add new of the the bisector to be graphed."""
        if boundary_sign:
            ranges = self.ranges_b_plus
        else:
            ranges = self.ranges_b_minus

        ranges[-1] = (ranges[-1][0], x, side)

    def get_y_by_side(self, x: Decimal, side: BisectorSide) -> Optional[Decimal]:
        """Get y by BisectorSide."""
        ys = self.bisector.formula_y(x)
        if len(ys) == 0:
            return None
        return ys[0]

    def complete_ranges(self):
        """Add a new range if neccessary."""
        pass

    def get_xml(self, i: int) -> str:
        """Get xml representation of the edge.

        The xml representation is based on Geogebra ggb xml.
        Docs: https://wiki.geogebra.org/en/Reference:XML
        """
        self.complete_ranges()
        xml_str = ""
        edge_label = "e_{{{0},{1}," + str(i) + "}}"
        expression_l = "b(x, p_{{{0}x}}, p_{{{1}x}}, p_{{{0}y}}, p_{{{1}y}})"
        if len(self.ranges_b_plus) > 0 and len(self.ranges_b_minus) > 0:
            # Both Boundaries have one type
            condition = "{0} x {1}"
            if self.ranges_b_minus[-1][1] is None:
                first_limit = ""
            else:
                first_limit = "{0} ≤".format(self.ranges_b_minus[-1][1])
            if self.ranges_b_plus[-1][1] is None:
                last_limit = ""
            else:
                last_limit = "≤ {0}".format(self.ranges_b_plus[-1][1])

            edge_label_1 = edge_label.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name
            )
            condition_1 = condition.format(first_limit, last_limit)
            expression_1 = expression_l.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name
            )
            xml_str += (
                self.create_xml_expression(edge_label_1, condition_1, expression_1)
                + "\n"
            )
        elif len(self.ranges_b_plus) > 0:
            condition = "{0} x {1}"
            if self.ranges_b_plus[-1][2] == 0:
                if self.ranges_b_plus[-1][1] is None:
                    last_limit = ""
                else:
                    last_limit = "≤ {0}".format(self.ranges_b_plus[-1][1])
                first_limit = "{0} ≤".format(self.ranges_b_plus[-1][0])
            else:
                if self.ranges_b_plus[-1][1] is None:
                    first_limit = ""
                else:
                    first_limit = "{0} ≤".format(self.ranges_b_plus[-1][1])
                last_limit = "≤ {0}".format(self.ranges_b_plus[-1][0])

            edge_label_1 = edge_label.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name
            )
            condition_1 = condition.format(first_limit, last_limit)
            expression_1 = expression_l.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name
            )
            xml_str += (
                self.create_xml_expression(edge_label_1, condition_1, expression_1)
                + "\n"
            )
        elif len(self.ranges_b_minus) > 0:
            condition = "{0} x {1}"
            if self.ranges_b_minus[-1][2] == 0:
                if self.ranges_b_minus[-1][1] is None:
                    first_limit = ""
                else:
                    first_limit = "{0} ≤".format(self.ranges_b_minus[-1][1])
                last_limit = "≤ {0}".format(self.ranges_b_minus[-1][0])
            else:
                if self.ranges_b_minus[-1][1] is None:
                    last_limit = ""
                else:
                    last_limit = "≤ {0}".format(self.ranges_b_minus[-1][1])
                first_limit = "{0} ≤".format(self.ranges_b_minus[-1][0])

            edge_label_1 = edge_label.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name
            )
            condition_1 = condition.format(first_limit, last_limit)
            expression_1 = expression_l.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name
            )
            xml_str += (
                self.create_xml_expression(edge_label_1, condition_1, expression_1)
                + "\n"
            )
        return xml_str


class WeightedPointBisectorEdge(Edge):
    """Weighted Point Bisector representation in Voronoi Diagram."""

    bisector: WeightedPointBisector
    boundary_plus: WeightedPointBoundary
    boundary_minus: WeightedPointBoundary

    def __init__(
        self,
        bisector: WeightedPointBisector,
        boundary_plus: WeightedPointBoundary,
        boundary_minus: WeightedPointBoundary,
        vertex1: Any = None,
        vertex2: Any = None,
    ) -> None:
        """Create Voronoi Diagram Weighted Bisector."""
        super().__init__(bisector, boundary_plus, boundary_minus, vertex1, vertex2)

    def add_end_range(
        self, x: Optional[Decimal], boundary_sign: bool, side: BisectorSide
    ) -> None:
        """Add new of the the bisector to be graphed."""
        if boundary_sign:
            ranges = self.ranges_b_plus
        else:
            ranges = self.ranges_b_minus

        last_side = ranges[-1][2]
        if last_side != side:
            vertical_tangents = self.bisector.get_vertical_tangents()
            if len(vertical_tangents) >= 1:
                ranges[-1] = (
                    ranges[-1][0],
                    vertical_tangents[0],
                    last_side,
                )
                ranges.append((vertical_tangents[0], x, side))
        else:
            ranges[-1] = (ranges[-1][0], x, side)

    def get_y_by_side(self, x: Decimal, side: BisectorSide) -> Optional[Decimal]:
        """Get y by BisectorSide."""
        ys = self.bisector.formula_y(x)
        if len(ys) == 0:
            return None
        elif len(ys) == 1:
            return ys[0]
        else:
            if side == 1:
                return max(ys)
            return min(ys)

    def complete_ranges(self) -> None:
        """Add a new range if neccessary."""
        # No blank lines
        def complete_range_in_boundary_if_neccessary(x, side, boundary):
            if x is None and side == 0 and boundary.is_boundary_not_x_monotone():
                self.add_end_range(None, boundary.sign, 1)

        def delete_first_with_side_0(b_range):
            for i, (_, _, side) in enumerate(b_range):
                if side == 0:
                    del b_range[i]
                    break

        if len(self.ranges_b_minus) > 0 and len(self.ranges_b_plus) > 0:
            x0, x1, side = self.ranges_b_plus[-1]
            complete_range_in_boundary_if_neccessary(x1, side, self.boundary_plus)
            x1, x0, side = self.ranges_b_minus[-1]
            complete_range_in_boundary_if_neccessary(x0, side, self.boundary_minus)
            return
        if len(self.ranges_b_minus) > 0:
            x1, x0, side = self.ranges_b_minus[-1]
            return complete_range_in_boundary_if_neccessary(
                x0, side, self.boundary_minus
            )
        if len(self.ranges_b_plus) > 0:
            x0, x1, side = self.ranges_b_plus[-1]
            return complete_range_in_boundary_if_neccessary(
                x1, side, self.boundary_plus
            )

        sites = self.bisector.get_sites_tuple()
        are_sites_in_same_y = (
            sites[0].get_event_point().y == sites[1].get_event_point().y
        )
        if not self.bisector.is_vertical() and are_sites_in_same_y:
            delete_first_with_side_0(self.ranges_b_plus)
            delete_first_with_side_0(self.ranges_b_minus)

    def get_xml(self, i: int) -> str:
        """Get xml representation of the edge.

        The xml representation is based on Geogebra ggb xml.
        Docs: https://wiki.geogebra.org/en/Reference:XML
        """
        self.complete_ranges()
        xml_str = ""
        edge_label = "e_{{{0},{1},{2}," + str(i) + "}}"
        expression = "B_{{{2}}}(x, p_{{{0}x}}, p_{{{1}x}}, p_{{{0}y}}, p_{{{1}y}}, p_{{{0}w}}, p_{{{1}w}})"
        expression_l = "b(x, p_{{{0}x}}, p_{{{1}x}}, p_{{{0}y}}, p_{{{1}y}})"
        if len(self.ranges_b_minus) > 1:
            # Boundary minus has two types
            condition = "{0} ≤ x {1}"
            if self.ranges_b_minus[-1][1] is None:
                first_limit = ""
            else:
                first_limit = "≤ {0}".format(self.ranges_b_minus[-1][1])
            if len(self.ranges_b_plus) > 0:
                if self.ranges_b_plus[-1][1] is None:
                    last_limit = ""
                else:
                    last_limit = "≤ {0}".format(self.ranges_b_plus[-1][1])
            else:
                last_limit = "≤ {0}".format(self.ranges_b_minus[0][0])

            edge_label_1 = edge_label.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, "p"
            )
            condition_1 = condition.format(self.ranges_b_minus[-1][0], first_limit)
            expression_1 = expression.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, "p"
            )
            xml_str += (
                self.create_xml_expression(edge_label_1, condition_1, expression_1)
                + "\n"
            )
            edge_label_2 = edge_label.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, "m"
            )
            condition_2 = condition.format(self.ranges_b_minus[-1][0], last_limit)
            expression_2 = expression.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, "m"
            )
            xml_str += (
                self.create_xml_expression(edge_label_2, condition_2, expression_2)
                + "\n"
            )

        elif len(self.ranges_b_plus) > 1:
            # Boundary plus has two types
            condition = "{0} x ≤ {1}"
            if self.ranges_b_plus[-1][1] is None:
                first_limit = ""
            else:
                first_limit = "{0} ≤".format(self.ranges_b_plus[-1][1])
            if len(self.ranges_b_minus) > 0:
                if self.ranges_b_minus[-1][1] is None:
                    last_limit = ""
                else:
                    last_limit = "{0} ≤".format(self.ranges_b_minus[-1][1])
            else:
                last_limit = "{0} ≤".format(self.ranges_b_plus[0][0])

            edge_label_1 = edge_label.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, "p"
            )
            condition_1 = condition.format(first_limit, self.ranges_b_plus[-1][0])
            expression_1 = expression.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, "p"
            )
            xml_str += (
                self.create_xml_expression(edge_label_1, condition_1, expression_1)
                + "\n"
            )
            edge_label_2 = edge_label.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, "m"
            )
            condition_2 = condition.format(last_limit, self.ranges_b_plus[-1][0])
            expression_2 = expression.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, "m"
            )
            xml_str += (
                self.create_xml_expression(edge_label_2, condition_2, expression_2)
                + "\n"
            )
        elif len(self.ranges_b_plus) > 0 and len(self.ranges_b_minus) > 0:
            # Both Boundaries have one type
            p, q = self.bisector.get_sites_tuple()
            if p.point.y - p.weight > q.point.y - q.weight:
                if p.weight > q.weight:
                    sign_str = "m"
                else:
                    sign_str = "p"
            else:
                sign_str = "p"

            condition = "{0} x {1}"
            if self.ranges_b_minus[-1][1] is None:
                first_limit = ""
            else:
                first_limit = "{0} ≤".format(self.ranges_b_minus[-1][1])
            if self.ranges_b_plus[-1][1] is None:
                last_limit = ""
            else:
                last_limit = "≤ {0}".format(self.ranges_b_plus[-1][1])

            edge_label_1 = edge_label.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, sign_str
            )
            condition_1 = condition.format(first_limit, last_limit)
            if self.bisector.sites[0].weight == self.bisector.sites[1].weight:
                expression_1 = expression_l.format(
                    self.bisector.sites[0].name, self.bisector.sites[1].name
                )
            else:
                expression_1 = expression.format(
                    self.bisector.sites[0].name, self.bisector.sites[1].name, sign_str
                )
            xml_str += (
                self.create_xml_expression(edge_label_1, condition_1, expression_1)
                + "\n"
            )
        elif len(self.ranges_b_plus) > 0:
            p, q = self.bisector.get_sites_tuple()
            if p.point.y - p.weight > q.point.y - q.weight:
                if p.weight > q.weight:
                    sign_str = "m"
                else:
                    sign_str = "p"
            else:
                if self.ranges_b_plus[-1][2] == 0:
                    sign_str = "m"
                else:
                    sign_str = "p"

            condition = "{0} x {1}"
            if self.ranges_b_plus[-1][2] == 0:
                if self.ranges_b_plus[-1][1] is None:
                    last_limit = ""
                else:
                    last_limit = "≤ {0}".format(self.ranges_b_plus[-1][1])
                first_limit = "{0} ≤".format(self.ranges_b_plus[-1][0])
            else:
                if self.ranges_b_plus[-1][1] is None:
                    first_limit = ""
                else:
                    first_limit = "{0} ≤".format(self.ranges_b_plus[-1][1])
                last_limit = "≤ {0}".format(self.ranges_b_plus[-1][0])

            edge_label_1 = edge_label.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, sign_str
            )
            condition_1 = condition.format(first_limit, last_limit)
            if self.bisector.sites[0].weight == self.bisector.sites[1].weight:
                expression_1 = expression_l.format(
                    self.bisector.sites[0].name, self.bisector.sites[1].name
                )
            else:
                expression_1 = expression.format(
                    self.bisector.sites[0].name, self.bisector.sites[1].name, sign_str
                )
            xml_str += (
                self.create_xml_expression(edge_label_1, condition_1, expression_1)
                + "\n"
            )
        elif len(self.ranges_b_minus) > 0:
            p, q = self.bisector.get_sites_tuple()
            if p.point.y - p.weight > q.point.y - q.weight:
                if p.weight > q.weight:
                    sign_str = "m"
                else:
                    sign_str = "p"
            else:
                if self.ranges_b_minus[-1][2] == 0:
                    sign_str = "m"
                else:
                    sign_str = "p"

            condition = "{0} x {1}"
            if self.ranges_b_minus[-1][2] == 0:
                if self.ranges_b_minus[-1][1] is None:
                    first_limit = ""
                else:
                    first_limit = "{0} ≤".format(self.ranges_b_minus[-1][1])
                last_limit = "≤ {0}".format(self.ranges_b_minus[-1][0])
            else:
                if self.ranges_b_minus[-1][1] is None:
                    last_limit = ""
                else:
                    last_limit = "≤ {0}".format(self.ranges_b_minus[-1][1])
                first_limit = "{0} ≤".format(self.ranges_b_minus[-1][0])

            edge_label_1 = edge_label.format(
                self.bisector.sites[0].name, self.bisector.sites[1].name, sign_str
            )
            condition_1 = condition.format(first_limit, last_limit)
            if self.bisector.sites[0].weight == self.bisector.sites[1].weight:
                expression_1 = expression_l.format(
                    self.bisector.sites[0].name, self.bisector.sites[1].name
                )
            else:
                expression_1 = expression.format(
                    self.bisector.sites[0].name, self.bisector.sites[1].name, sign_str
                )
            xml_str += (
                self.create_xml_expression(edge_label_1, condition_1, expression_1)
                + "\n"
            )
        return xml_str
