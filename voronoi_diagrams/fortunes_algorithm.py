"""Fortune's Algorithm to calculate Voronoi Diagrams.

General Solution.
"""
# Standard Library
from typing import Iterable, List, Any, Optional, Tuple, Dict, Type

# Data structures
from .data_structures import LList, QQueue
from .data_structures.l import LNode

# Models
from .models import (
    Site,
    WeightedSite,
    Point,
    Bisector,
    Event,
    Intersection,
    Region,
    Boundary,
    PointBisector,
    PointBoundary,
    WeightedPointBisector,
    WeightedPointBoundary,
    Edge,
    PointBisectorEdge,
    WeightedPointBisectorEdge,
    Vertex,
)

# Math
from decimal import Decimal

# Plot
from plotly import graph_objects as go
from plots.plot_utils.models.events import (
    plot_sweep_line,
    get_site_traces,
    plot_events_traces,
)
from plots.plot_utils.models.boundaries import get_plot_scatter_boundary
from plots.plot_utils.models.bisectors import plot_edge
from plots.plot_utils.models.vertices import plot_vertex

# Types
Limit = Tuple[Decimal, Decimal]

# Modes
STATIC_MODE = 0
DYNAMIC_MODE = 1


class FortunesAlgorithm:
    """Fortune's Algorithm implementation."""

    @staticmethod
    def calculate_voronoi_diagram(
        points: List[Point],
        plot_steps: bool = False,
        xlim: Limit = (-100, 100),
        ylim: Limit = (-100, 100),
        mode: int = STATIC_MODE,
        names: Optional[List[str]] = None,
    ) -> "FortunesAlgorithm":
        """Calculate Voronoi Diagram."""
        if names is None or len(points) != len(names):
            names = [str(i + 1) for i in range(len(points))]
        sites = [
            Site(points[i].x, points[i].y, name=names[i]) for i in range(len(points))
        ]
        voronoi_diagram = FortunesAlgorithm(
            sites, plot_steps=plot_steps, xlim=xlim, ylim=ylim, mode=mode,
        )

        return voronoi_diagram

    @staticmethod
    def calculate_aw_voronoi_diagram(
        points_and_weights: List[Tuple[Point, Decimal]],
        plot_steps: bool = False,
        xlim: Limit = (-100, 100),
        ylim: Limit = (-100, 100),
        mode: int = STATIC_MODE,
        names: Optional[List[str]] = None,
    ) -> "FortunesAlgorithm":
        """Calculate AW Voronoi Diagram."""
        sites = []
        if names is None or len(points_and_weights) != len(names):
            names = [str(i + 1) for i in range(len(points_and_weights))]
        for i in range(len(points_and_weights)):
            point, weight = points_and_weights[i]
            site = WeightedSite(point.x, point.y, weight, name=names[i])
            sites.append(site)

        voronoi_diagram = FortunesAlgorithm(
            sites, plot_steps=plot_steps, xlim=xlim, ylim=ylim, mode=mode,
        )

        return voronoi_diagram

    vertices: List[Vertex]
    vertices_list: List[Point]
    edges: List[Edge]
    bisectors_list: List[Bisector]
    mode: int
    event: Event  # Current Event

    _vertices_dict: Dict[Tuple[Decimal, Decimal], Vertex]
    _bisectors: Dict[Any, Bisector]
    _active_bisectors: Dict[Any, Edge]
    sites: List[Site]
    _plot_steps: bool
    _figure: Optional[go.Figure]
    _figure_traces: int
    _boundary_plot_dict: Dict[str, int]
    _bisector_plot_dict: Dict[Tuple[str, bool], int]
    _begin_event: bool
    _updated_regions: List[Region]
    _updated_boundaries: List[Boundary]

    def __init__(
        self,
        sites: Iterable[Site],
        plot_steps: bool = False,
        xlim: Optional[Limit] = (-100, 100),
        ylim: Optional[Limit] = (-100, 100),
        mode: Optional[int] = STATIC_MODE,
    ) -> None:
        """Construct and calculate Voronoi Diagram."""
        self.vertices = []
        self.vertices_list = []
        self._vertices = dict()

        self.edges = []
        self.bisectors_list = []
        self._bisectors = dict()
        self._active_bisectors = dict()

        # Type of Voronoi diagram.
        self.sites = list(sites)
        if len(self.sites) == 0:
            return

        self.SITE_CLASS = type(self.sites[0])
        if self.SITE_CLASS == Site:
            self.BISECTOR_CLASS = PointBisector
            self.REGION_CLASS = Region
            self.BOUNDARY_CLASS = PointBoundary
            self.EDGE_CLASS = PointBisectorEdge
            self._site_traces = 1
        elif self.SITE_CLASS == WeightedSite:
            self.BISECTOR_CLASS = WeightedPointBisector
            self.REGION_CLASS = Region
            self.BOUNDARY_CLASS = WeightedPointBoundary
            self.EDGE_CLASS = WeightedPointBisectorEdge
            self._site_traces = 2

        # Plot.
        self._plot_steps = plot_steps
        if self._plot_steps:
            self._figure = go.Figure()
            layout = go.Layout(
                height=745,
                width=815,
                hovermode="closest",
                legend={"itemclick": "toggleothers", "itemdoubleclick": "toggle"},
            )
            template = dict(layout=layout)
            self._figure.update_layout(title="VD", template=template)
            self._figure.update_xaxes(range=list(xlim))
            self._figure.update_yaxes(range=list(ylim), scaleanchor="x", scaleratio=1)
            self._xlim = xlim
            self._ylim = ylim
            self._figure_traces = 0
            self._traces = []
            self._boundary_plot_dict = {}
            self._bisector_plot_dict = {}
        else:
            self._figure = None

        self._updated_regions = []
        self._updated_boundaries = []

        # Mode.
        self.mode = mode
        self._begin_event = True
        self._init_structures()
        if self.mode == STATIC_MODE:
            self._calculate_diagram()

    def _init_structures(self):
        """Init data structures used."""
        # Step 1.
        self.q_queue = QQueue()
        for site in self.sites:
            self.q_queue.enqueue(site)
            if self._plot_steps:
                self._set_site_trace(site)

        # Step 2.
        self.event = self.q_queue.dequeue()

        # Step 3.
        r_p = self.REGION_CLASS(self.event, None, None)
        self._updated_regions = [r_p]
        r_p.active = True
        self.l_list = LList(r_p)
        self._plot_step()

    def _set_site_trace(self, site):
        """Set site trace in traces."""
        if self._plot_steps:
            site_traces = get_site_traces(site, self.SITE_CLASS)
            self._traces += site_traces
            self._figure_traces += len(site_traces)

    def _calculate_diagram(self):
        """Calculate point diagram."""
        # Step 4.
        while not self.q_queue.is_empty():
            self.calculate_next_event()

    def calculate_next_event(self):
        """Calculate next event in the Queue."""
        self.move_to_next_event()
        self.calculate_event()

    def move_to_next_event(self):
        """Move to next event in Queue."""
        # Reset active boundaries and regions.
        for region in self._updated_regions:
            region.active = False
        for boundary in self._updated_boundaries:
            boundary.active = False
        self._updated_regions = []
        self._updated_boundaries = []

        # Step 4.
        if self.q_queue.is_empty():
            return

        # Step 5.
        self.event = self.q_queue.dequeue()
        self._plot_step()
        self._begin_event = False
        if not self.event.is_site:
            self.event.region_node.value.is_to_be_deleted = True
            self.event.region_node.value.left.is_to_be_deleted = True
            self.event.region_node.value.right.is_to_be_deleted = True

    def calculate_event(self):
        """Calculate actual event."""
        self._plot_step()
        # Step 6 and 7.
        if self.event.is_site:
            self._handle_site(self.event)
        # Step 13: p is an intersection.
        else:
            self._handle_intersection(self.event)
        self._plot_step()
        self._begin_event = True

    def _plot_step(self):
        """Plot step."""
        if self._plot_steps:
            # keep the sites and clean all other traces.
            self._figure.data = []
            for trace in self._traces:
                if trace is not None:
                    self._figure.add_trace(trace)
            plot_sweep_line(self._figure, self._xlim, self._ylim, self.event)
            plot_events_traces(self._figure, self.q_queue)
            # self._figure.show()

    def next_step(self):
        """Calculate next step."""
        if self._begin_event:
            self.move_to_next_event()
        else:
            self.calculate_event()

    def is_next_step(self):
        """Get if there is a next step to calculate."""
        return not self.q_queue.is_empty() or not self._begin_event

    def _handle_site(self, p: Site):
        """Handle when event is a site."""
        # Step 8.
        # Find an occurrence of a region R*q on L containing p.
        r_q, r_q_node = self._find_region_containing_p(p)
        left_region_node = r_q_node.left_neighbor
        right_region_node = r_q_node.right_neighbor

        # Step 8.1.
        # Check if p is dominated by q.
        if p.is_dominated(r_q.site):
            # Discard this site.
            return

        # Step 9.
        # Create Bisector B*pq.
        # Actually we are creating Bpq.
        bisector_p_q = self.BISECTOR_CLASS(sites=(p, r_q.site))
        self.add_edge(bisector_p_q, sign=None)

        # Step 10.
        # Update list L so that it contains ...,R*q,C-pq,R*p,C+pq,R*q,... in place of R*q.
        r_p = self.REGION_CLASS(p, None, None)
        (
            boundary_p_q_plus,
            boundary_p_q_minus,
            r_q_left_node,
            r_q_right_node,
        ) = self._update_l_list(r_p, r_q, bisector_p_q)

        if bisector_p_q.is_vertical():
            self.add_begin_vertical_edge(bisector_p_q, None)
        else:
            self.add_begin_edge(boundary_p_q_minus, p.point)
            self.add_begin_edge(boundary_p_q_plus, p.point)

        if self._plot_steps:
            self._add_boundaries_to_plot([boundary_p_q_minus, boundary_p_q_plus])
            self._add_bisector_to_plot(
                bisector_p_q, None
            )  # It doesn't matter the sign here.

        # Step 11.
        # Delete from Q the intersection between the left and right boundary of R*q, if any.
        left_boundary: Optional[Boundary] = None
        right_boundary: Optional[Boundary] = None
        # Left
        if left_region_node is not None:
            left_boundary = left_region_node.value.right
            self._delete_intersection_from_boundary(
                left_boundary, is_left_intersection=False
            )
        # Right
        if right_region_node is not None:
            right_boundary = right_region_node.value.left
            self._delete_intersection_from_boundary(
                right_boundary, is_left_intersection=True
            )

        # Step 12.
        # Insert into Q the intersection between C-pq and its neighbor to the left on L, if any, and
        # the intersection between C+pq and its neighbor to the right, if any.
        self._insert_posible_intersections(
            left_boundary,
            boundary_p_q_minus,
            r_q_left_node,
            boundary_p_q_plus,
            right_boundary,
            r_q_right_node,
        )

    def _handle_intersection(self, p: Intersection):
        """Handle when event is an intersection."""
        # Step 14.
        # Let p be the intersection of boundaries Cqr and Crs.
        intersection_region_node = p.region_node
        r_q, r_s, r_q_node, r_s_node = self._get_regions_and_nodes_of_intersection(p)
        left_boundary = r_q.left
        right_boundary = r_s.right
        intersection_region_node_value_left = intersection_region_node.value.left
        intersection_region_node_value_right = intersection_region_node.value.right
        intersection_left_bisector = intersection_region_node_value_left.bisector
        intersection_left_bisector_sign = intersection_region_node_value_left.sign
        intersection_right_bisector = intersection_region_node_value_right.bisector
        intersection_right_bisector_sign = intersection_region_node_value_right.sign

        # Step 15.
        # Create bisector B*qs.
        bisector_q_s = self.BISECTOR_CLASS(sites=(r_q.site, r_s.site))

        # Step 16.
        # Update list L so it contains Cqs instead of Cqr, Rr*, Crs
        boundary_q_s_sign = self.BOUNDARY_CLASS.get_boundary_sign(
            p.point, r_q.site, r_s.site
        )
        boundary_q_s = self.BOUNDARY_CLASS(bisector_q_s, boundary_q_s_sign)
        self.add_edge(bisector_q_s, sign=boundary_q_s_sign)
        left_region_node = intersection_region_node.left_neighbor
        right_region_node = intersection_region_node.right_neighbor

        self.add_endpoint_to_new_edge(boundary_q_s, p)
        if intersection_region_node.value.left.bisector.is_vertical():
            self.add_end_vertical_edge(
                intersection_region_node.value.left.bisector,
                p.vertex.y,
                intersection_region_node.value.left.sign,
            )
        else:
            self.add_end_edge(intersection_region_node.value.left, p.point)
        if intersection_region_node.value.right.bisector.is_vertical():
            self.add_end_vertical_edge(
                intersection_region_node.value.right.bisector,
                p.vertex.y,
                intersection_region_node.value.right.sign,
            )
        else:
            self.add_end_edge(intersection_region_node.value.right, p.point)

        if self._plot_steps:
            # Remove
            self._remove_boundaries_from_figure_traces(
                intersection_region_node.value.left,
                intersection_region_node.value.right,
            )
            self._update_boundaries_bisectors_figure_traces(
                [
                    intersection_region_node.value.left,
                    intersection_region_node.value.right,
                ]
            )
            # Add new boundary
            self._add_boundary_to_plot(boundary_q_s)
            # Add new bisector
            self._add_bisector_to_plot(bisector_q_s, boundary_q_s_sign)

        boundary_q_s.active = True
        self._updated_boundaries = [boundary_q_s]
        self._updated_regions = []
        self.l_list.remove_region(intersection_region_node, boundary_q_s)

        # Step 17.
        # Delete from Q any intersection between Cqr and its neighbor to the
        # left and between Crs and its neighbor to the right.
        self._delete_intersection_from_boundary(
            intersection_region_node_value_left, is_left_intersection=True
        )
        if left_region_node is not None:
            self._delete_intersection_from_boundary(
                left_region_node.value.left, is_left_intersection=False
            )
        self._delete_intersection_from_boundary(
            intersection_region_node_value_right, is_left_intersection=False
        )
        if right_region_node is not None:
            self._delete_intersection_from_boundary(
                right_region_node.value.right, is_left_intersection=True
            )

        # Step 18.
        # Insert any intersections between Cqs and its neighbors to the left or right
        # into Q.
        self._insert_posible_intersections(
            left_boundary,
            boundary_q_s,
            r_q_node,
            boundary_q_s,
            right_boundary,
            r_s_node,
        )

        # Step 19.
        # Mark p as a vertex and as an endpoint of B*qr, B*rs and B*qs.
        # Add that this vertex is an endpoint of B*qr, B*rs and B*qs.
        vd_bisectors = self.get_edges(
            [
                (intersection_left_bisector, intersection_left_bisector_sign),
                (intersection_right_bisector, intersection_right_bisector_sign),
                (bisector_q_s, boundary_q_s_sign),
            ]
        )
        self.add_vertex(p.vertex, vd_bisectors)

    def add_vertex(self, point: Point, edges: Optional[List[Edge]] = None) -> None:
        """Add point in the vertex list."""
        point_tuple = point.get_tuple()
        if point_tuple not in self._vertices:
            vertex = Vertex(point)
            self._vertices[point_tuple] = vertex
            self.vertices.append(vertex)
            self.vertices_list.append(point)
        else:
            vertex = self._vertices[point_tuple]

        if edges is not None:
            for vd_bisector in edges:
                vertex.add_edge(vd_bisector)
                vd_bisector.add_vertex(vertex)

        if self._plot_steps:
            self._add_vertex_trace(vertex)

    def add_edge(self, bisector: Bisector, sign: Optional[bool] = True) -> None:
        """Add point in the edges list."""
        hasheable_of_bisector = bisector.get_object_to_hash()
        if hasheable_of_bisector not in self._bisectors:
            self._bisectors[hasheable_of_bisector] = bisector
            self.bisectors_list.append(bisector)
        edge = self.EDGE_CLASS(
            bisector,
            self.BOUNDARY_CLASS(bisector, True),
            self.BOUNDARY_CLASS(bisector, False),
        )
        self.edges.append(edge)
        if sign is None:
            self._active_bisectors[(hasheable_of_bisector, False)] = edge
            self._active_bisectors[(hasheable_of_bisector, True)] = edge
        else:
            self._active_bisectors[(hasheable_of_bisector, sign)] = edge

    def _find_region_containing_p(self, p: Site) -> Tuple[Region, Region, LNode]:
        """Find an occurrence of a region R*q on L containing p."""
        r_q_node = self.l_list.search_region_node(p)
        r_q = r_q_node.value
        return r_q, r_q_node

    def add_endpoint_to_new_edge(self, boundary: Boundary, p: Intersection):
        """Add endpoint in new edge."""
        if boundary.bisector.is_vertical():
            self.add_begin_vertical_edge(boundary.bisector, p.vertex.y, boundary.sign)
        else:
            self.add_begin_edge(boundary, p.point)

    def _update_l_list(
        self, r_p: Region, r_q: Region, bisector_p_q: Bisector,
    ) -> Tuple[Boundary, Boundary, LNode, LNode]:
        """Update list L so that it contains ...,R*q,C-pq,R*p,C+pq,R*q,... in the place of R*q."""
        boundary_p_q_plus = self.BOUNDARY_CLASS(bisector_p_q, True)  # type: ignore
        boundary_p_q_minus = self.BOUNDARY_CLASS(bisector_p_q, False)  # type: ignore
        r_q_left = self.REGION_CLASS(r_q.site, r_q.left, boundary_p_q_minus)
        r_q_right = self.REGION_CLASS(r_q.site, boundary_p_q_plus, r_q.right)
        r_p.left = boundary_p_q_minus
        r_p.right = boundary_p_q_plus

        self._updated_boundaries = [boundary_p_q_minus, boundary_p_q_plus]
        self._updated_regions = [r_q_left, r_p, r_q_right]
        for region in self._updated_regions:
            region.active = True
        for boundary in self._updated_boundaries:
            boundary.active = True

        # Update L list.
        r_q_left_node, r_p_node, r_q_right_node = self.l_list.update_regions(
            r_q_left, r_p, r_q_right
        )
        return (
            boundary_p_q_plus,
            boundary_p_q_minus,
            r_q_left_node,
            r_q_right_node,
        )

    def _add_boundaries_to_plot(self, boundaries: List[Boundary]):
        """Add boundaries to plot."""
        if self._plot_steps:
            for boundary in boundaries:
                self._add_boundary_to_plot(boundary)

    def _add_boundary_to_plot(self, boundary: Boundary):
        """Add boundary to plot."""
        if self._plot_steps:
            trace = get_plot_scatter_boundary(
                boundary, self._xlim, self._ylim, self.BISECTOR_CLASS,
            )
            self._traces.append(trace)
            self._figure_traces += 1
            # TODO: Change to use complete_string()
            self._boundary_plot_dict[str(boundary)] = self._figure_traces - 1

    def _add_bisector_to_plot(self, bisector: Bisector, sign: Optional[bool]):
        """Add boundary to plot."""
        if self._plot_steps:
            if sign is None:
                vd_bisector = self.get_edges([(bisector, True)])[0]
            else:
                vd_bisector = self.get_edges([(bisector, sign)])[0]
            traces = plot_edge(vd_bisector, self._xlim, self._ylim, self.BISECTOR_CLASS)
            self._traces += traces
            traces_numbers = list(
                range(self._figure_traces, self._figure_traces + len(traces))
            )
            if sign is None:
                self._bisector_plot_dict[
                    (str(bisector.get_object_to_hash()), True)
                ] = traces_numbers
                self._bisector_plot_dict[
                    (str(bisector.get_object_to_hash()), False)
                ] = traces_numbers
            else:
                self._bisector_plot_dict[
                    (str(bisector.get_object_to_hash()), sign)
                ] = traces_numbers
            self._figure_traces += len(traces)

    def get_edges(self, bisectors: List[Tuple[Bisector, bool]]) -> List[Edge]:
        """Get voronoi diagram bisectors based on the current state."""
        edges = []
        for bisector, sign in bisectors:
            hasheable_of_bisector = bisector.get_object_to_hash()
            edge = self._active_bisectors[(hasheable_of_bisector, sign)]
            edges.append(edge)
        return edges

    def _delete_intersection_from_boundary(
        self, boundary: Optional[Boundary], is_left_intersection: bool
    ) -> None:
        if boundary is None:
            return

        if is_left_intersection and boundary.left_intersection is not None:
            self.q_queue.delete(boundary.left_intersection)
            boundary.left_intersection = None
        elif not is_left_intersection and boundary.right_intersection is not None:
            self.q_queue.delete(boundary.right_intersection)
            boundary.right_intersection = None

    def _insert_posible_intersections(
        self,
        left_left_boundary: Optional[Boundary],
        left_right_boundary: Boundary,
        left_region_node: LNode,
        right_left_boundary: Boundary,
        right_right_boundary: Optional[Boundary],
        right_region_node: LNode,
    ) -> None:
        """Insert posible intersections in Q."""
        # Left.
        if left_left_boundary is not None:
            self._insert_intersection(
                left_left_boundary, left_right_boundary, left_region_node
            )

        # Right.
        if right_right_boundary is not None:
            self._insert_intersection(
                right_left_boundary, right_right_boundary, right_region_node
            )

    def _insert_intersection(
        self, boundary_1: Boundary, boundary_2: Boundary, region_node: LNode
    ) -> None:
        """Look for intersections between the the boundaries."""
        # There could be a possibility that the two boundaries are from the same bisector.
        if boundary_1.bisector == boundary_2.bisector:
            return

        intersection_point_tuples = boundary_1.get_intersections(boundary_2)
        if intersection_point_tuples:
            # Adding all intersections.
            for vertex, event in intersection_point_tuples:
                intersection = Intersection(event, vertex, region_node)
                # Insert intersection to Q.
                self.q_queue.enqueue(intersection)
                # Save intersection in both boundaries.
                boundary_1.right_intersection = intersection
                boundary_2.left_intersection = intersection

    def _get_regions_and_nodes_of_intersection(self, p: Intersection):
        """Get regions and their nodes of the intersection p."""
        intersection_region_node = p.region_node
        # Left and right neighbor cannot be None because p is an intersection.
        r_q_node = intersection_region_node.left_neighbor
        r_q = r_q_node.value  # type: ignore
        r_s_node = intersection_region_node.right_neighbor
        r_s = r_s_node.value  # type: ignore
        return r_q, r_s, r_q_node, r_s_node

    def _update_boundaries_bisectors_figure_traces(
        self, boundaries: List[Optional[Boundary]]
    ):
        """Update boundaries bisectors' figure traces."""
        for boundary in boundaries:
            if boundary is None:
                continue
            self._update_bisector_figure_traces(boundary.bisector, boundary.sign)

    def _update_bisector_figure_traces(self, bisector: Bisector, sign: bool):
        """Update bisector's figure traces."""
        bisector_traces = self._bisector_plot_dict[
            (str(bisector.get_object_to_hash()), sign)
        ]
        bisector_other_sign_traces = self._bisector_plot_dict.get(
            (str(bisector.get_object_to_hash()), not sign), []
        )
        if bisector_traces == bisector_other_sign_traces:
            sign = None
        for bisector_trace_i in bisector_traces:
            self._traces[bisector_trace_i] = None
        self._add_bisector_to_plot(bisector, sign)

    def _add_vertex_trace(self, vertex: Vertex):
        """Add vertex to vd trace."""
        trace = plot_vertex(vertex)
        self._traces.append(trace)
        self._figure_traces += 1

    def _remove_boundaries_from_figure_traces(
        self, boundary1: Optional[Boundary], boundary2: Optional[Boundary]
    ):
        """Remove boundary from figure traces."""
        if boundary1 is None and boundary2 is None:
            return
        if boundary1 is None:
            self._remove_boundary_from_figure_traces(boundary2)
        elif boundary2 is None:
            self._remove_boundary_from_figure_traces(boundary1)
        else:
            position1 = self._boundary_plot_dict[str(boundary1)]
            position2 = self._boundary_plot_dict[str(boundary2)]
            if position1 > position2:
                self._remove_boundary_from_figure_traces(boundary1)
                self._remove_boundary_from_figure_traces(boundary2)
            else:
                self._remove_boundary_from_figure_traces(boundary2)
                self._remove_boundary_from_figure_traces(boundary1)

    def _remove_boundary_from_figure_traces(self, boundary: Optional[Boundary]):
        """Remove boundary from figure traces."""
        if boundary is None:
            return
        self._traces[self._boundary_plot_dict[str(boundary)]] = None

    def add_begin_vertical_edge(
        self, bisector: Bisector, y: Optional[Decimal], sign: bool = True
    ):
        """Add endpoint to begin vertical edge."""
        edge = self.get_edges([(bisector, sign)])[0]
        edge.add_begin_range_vertical(y)

    def add_begin_edge(self, boundary: Boundary, point: Point) -> None:
        """Add endpoint to begin edge."""
        edge = self.get_edges([(boundary.bisector, boundary.sign)])[0]
        side = boundary.get_side_where_point_belongs(point)
        edge.add_begin_range(point.x, boundary.sign, side)

    def add_end_vertical_edge(self, bisector: Bisector, y: Decimal, sign: bool = True):
        """Add endpoint to end vertical edge."""
        edge = self.get_edges([(bisector, sign)])[0]
        edge.add_end_range_vertical(y)

    def add_end_edge(self, boundary: Boundary, point: Point) -> None:
        """Add endpoint to end edge."""
        edge = self.get_edges([(boundary.bisector, boundary.sign)])[0]
        side = boundary.get_side_where_point_belongs(point)
        edge.add_end_range(point.x, boundary.sign, side)
