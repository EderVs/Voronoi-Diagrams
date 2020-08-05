"""Fortune's Algorithm to calculate Voronoi Diagrams.

General Solution.
"""
# Standard Library
from typing import Iterable, List, Any, Optional, Tuple, Set, Dict, Type

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
    IntersectionEvent,
    Region,
    Boundary,
    PointBisector,
    PointBoundary,
    WeightedPointBisector,
    WeightedPointBoundary,
    VoronoiDiagramBisector,
    VoronoiDiagramVertex,
)

# Math
from decimal import Decimal

# Plot
from plotly import graph_objects as go
from plots.plot_utils.models.sites import plot_site, plot_sweep_line
from plots.plot_utils.data_structures.l_list import plot_l_list

Limit = Tuple[Decimal, Decimal]


class VoronoiDiagram:
    """Voronoi Diagram representation."""

    vertices: List[VoronoiDiagramVertex]
    vertices_list: List[Point]
    bisectors: List[VoronoiDiagramBisector]
    bisectors_list: List[Bisector]

    _vertices_dict: Dict[Tuple[Decimal, Decimal], VoronoiDiagramVertex]
    _bisectors: Dict[Any, Bisector]
    _active_bisectors: Dict[Any, VoronoiDiagramBisector]
    sites: List[Site]
    _plot_steps: bool
    _figure: Optional[go.Figure]

    def __init__(
        self,
        sites: Iterable[Site],
        site_class: Type[Site] = Site,
        plot_steps: bool = False,
        xlim: Optional[Limit] = (-100, 100),
        ylim: Optional[Limit] = (-100, 100),
    ):
        """Construct and calculate Voronoi Diagram."""
        self.vertices = []
        self.vertices_list = []
        self._vertices = dict()

        self.bisectors = []
        self.bisectors_list = []
        self._bisectors = dict()
        self._active_bisectors = dict()

        self.sites = list(sites)
        self.SITE_CLASS = site_class
        if site_class == Site:
            self.BISECTOR_CLASS = PointBisector
            self.REGION_CLASS = Region
            self.BOUNDARY_CLASS = PointBoundary
            self._site_traces = 1
        elif site_class == WeightedSite:
            self.BISECTOR_CLASS = WeightedPointBisector
            self.REGION_CLASS = Region
            self.BOUNDARY_CLASS = WeightedPointBoundary
            self._site_traces = 3

        self._plot_steps = plot_steps
        if self._plot_steps:
            self._figure = go.Figure()
            layout = go.Layout(height=1000, width=1000,)
            template = dict(layout=layout)
            self._figure.update_layout(title="VD", template=template)
            self._figure.update_xaxes(range=list(xlim))
            self._figure.update_yaxes(range=list(ylim), scaleanchor="x", scaleratio=1)
            self._xlim = xlim
            self._ylim = ylim
        else:
            self._figure = None
        self._calculate_diagram()

    def add_vertex(
        self, point: Point, vd_bisectors: Optional[List[VoronoiDiagramBisector]] = None
    ) -> None:
        """Add point in the vertex list."""
        point_tuple = point.get_tuple()
        if point_tuple not in self._vertices:
            vd_vertex = VoronoiDiagramVertex(point)
            self._vertices[point_tuple] = vd_vertex
            self.vertices.append(vd_vertex)
            self.vertices_list.append(point)
        else:
            vd_vertex = self._vertices[point_tuple]

        if vd_bisectors is not None:
            for vd_bisector in vd_bisectors:
                vd_vertex.add_bisector(vd_bisector)
                vd_bisector.add_vertex(vd_vertex)

    def add_bisector(self, bisector: Bisector, sign: Optional[bool] = True) -> None:
        """Add point in the vertex list."""
        hasheable_of_bisector = bisector.get_object_to_hash()
        if hasheable_of_bisector not in self._bisectors:
            self._bisectors[hasheable_of_bisector] = bisector
            self.bisectors_list.append(bisector)
        vd_bisector = VoronoiDiagramBisector(bisector)
        self.bisectors.append(vd_bisector)
        if sign is None:
            self._active_bisectors[(hasheable_of_bisector, False)] = vd_bisector
            self._active_bisectors[(hasheable_of_bisector, True)] = vd_bisector
        else:
            self._active_bisectors[(hasheable_of_bisector, sign)] = vd_bisector

    def get_voronoi_diagram_bisectors(
        self, bisectors: List[Tuple[Bisector, bool]]
    ) -> List[VoronoiDiagramBisector]:
        """Get voronoi diagram bisectors based on the current state."""
        vd_bisectors = []
        for bisector, sign in bisectors:
            hasheable_of_bisector = bisector.get_object_to_hash()
            vd_bisector = self._active_bisectors[(hasheable_of_bisector, sign)]
            vd_bisectors.append(vd_bisector)
        return vd_bisectors

    def _find_region_containing_p(self, p: Site) -> Tuple[Region, Region, LNode]:
        """Find an occurrence of a region R*q on L containing p.

        Also returns the Region of p.
        """
        r_p = self.REGION_CLASS(p, None, None)
        r_q_node = self.l_list.search_region_node(r_p)
        r_q = r_q_node.value
        return r_p, r_q, r_q_node

    def _update_list_l(
        self, r_p: Region, r_q: Region, bisector_p_q: Bisector,
    ) -> Tuple[Boundary, Boundary, LNode, LNode]:
        """Update list L so that it contains ...,R*q,C-pq,R*p,C+pq,R*q,... in place of R*q."""
        boundary_p_q_plus = self.BOUNDARY_CLASS(bisector_p_q, True)  # type: ignore
        boundary_p_q_minus = self.BOUNDARY_CLASS(bisector_p_q, False)  # type: ignore
        r_q_left = self.REGION_CLASS(r_q.site, r_q.left, boundary_p_q_minus)
        r_q_right = self.REGION_CLASS(r_q.site, boundary_p_q_plus, r_q.right)
        r_p.left = boundary_p_q_minus
        r_p.right = boundary_p_q_plus
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
                intersection = IntersectionEvent(event, vertex, region_node)
                # Insert intersection to Q.
                self.q_queue.enqueue(intersection)
                # Save intersection in both boundaries.
                boundary_1.right_intersection = intersection
                boundary_2.left_intersection = intersection

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

    def _handle_site(self, p: Site):
        """Handle when event is a site."""
        # Step 8.
        # Find an occurrence of a region R*q on L containing p.
        r_p, r_q, r_q_node = self._find_region_containing_p(p)
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
        self.add_bisector(bisector_p_q, sign=None)

        # Step 10.
        # Update list L so that it contains ...,R*q,C-pq,R*p,C+pq,R*q,... in place of R*q.
        (
            boundary_p_q_plus,
            boundary_p_q_minus,
            r_q_left_node,
            r_q_right_node,
        ) = self._update_list_l(r_p, r_q, bisector_p_q)

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

    def _get_regions_and_nodes_of_intersection(self, p: IntersectionEvent):
        """Get regions and their nodes of the intersection p."""
        intersection_region_node = p.region_node
        # Left and right neighbor cannot be None because p is an intersection.
        r_q_node = intersection_region_node.left_neighbor
        r_q = r_q_node.value  # type: ignore
        r_s_node = intersection_region_node.right_neighbor
        r_s = r_s_node.value  # type: ignore
        return r_q, r_s, r_q_node, r_s_node

    def _handle_intersection(self, p: IntersectionEvent):
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
        boundary_q_s_sign = r_q.site.get_event_point().y > r_s.site.get_event_point().y
        boundary_q_s = self.BOUNDARY_CLASS(bisector_q_s, boundary_q_s_sign)
        self.add_bisector(bisector_q_s, sign=boundary_q_s_sign)
        left_region_node = intersection_region_node.left_neighbor
        right_region_node = intersection_region_node.right_neighbor
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
        vd_bisectors = self.get_voronoi_diagram_bisectors(
            [
                (intersection_left_bisector, intersection_left_bisector_sign),
                (intersection_right_bisector, intersection_right_bisector_sign),
                (bisector_q_s, boundary_q_s_sign),
            ]
        )
        self.add_vertex(p.vertex, vd_bisectors)

    def _calculate_diagram(self):
        """Calculate point diagram."""
        # Step 1.
        self.q_queue = QQueue()
        for site in self.sites:
            self.q_queue.enqueue(site)
            plot_site(self._figure, site, self.SITE_CLASS)
        # Step 2.
        p = self.q_queue.dequeue()
        # Step 3.
        r_p = self.REGION_CLASS(p, None, None)
        self.l_list = LList(r_p)
        self._plot_step(p)
        # Step 4.
        while not self.q_queue.is_empty():
            # Step 5.
            p = self.q_queue.dequeue()
            self._plot_step(p)
            # Step 6 and 7.
            if p.is_site:
                self._handle_site(p)
            # Step 13: p is an intersection.
            else:
                self._handle_intersection(p)
            self._plot_step(p)

    def _plot_step(self, p: Event):
        """Plot step."""
        if self._plot_steps:
            # keep the sites and clean all other traces.
            self._figure.data = self._figure.data[: self._site_traces * len(self.sites)]
            plot_l_list(
                self._figure, self.l_list, self._xlim, self._ylim, self.BISECTOR_CLASS,
            )
            plot_sweep_line(self._figure, self._xlim, self._ylim, p)
            self._figure.show()
            print(self.l_list)


class FortunesAlgorithm:
    """Fortune's Algorithm implementation."""

    @staticmethod
    def calculate_voronoi_diagram(
        points: List[Point],
        plot_steps: bool = False,
        xlim: Limit = (-100, 100),
        ylim: Limit = (-100, 100),
    ) -> VoronoiDiagram:
        """Calculate Voronoi Diagram."""
        sites = [
            Site(points[i].x, points[i].y, name=str(i + 1)) for i in range(len(points))
        ]
        voronoi_diagram = VoronoiDiagram(
            sites, site_class=Site, plot_steps=plot_steps, xlim=xlim, ylim=ylim
        )

        return voronoi_diagram

    @staticmethod
    def calculate_aw_voronoi_diagram(
        points_and_weights: List[Tuple[Point, Decimal]],
        plot_steps: bool = False,
        xlim: Limit = (-100, 100),
        ylim: Limit = (-100, 100),
    ) -> VoronoiDiagram:
        """Calculate AW Voronoi Diagram."""
        sites = []
        for i in range(len(points_and_weights)):
            point, weight = points_and_weights[i]
            site = WeightedSite(point.x, point.y, weight, name=str(i + 1))
            sites.append(site)

        voronoi_diagram = VoronoiDiagram(
            sites, site_class=WeightedSite, plot_steps=plot_steps, xlim=xlim, ylim=ylim
        )

        return voronoi_diagram
