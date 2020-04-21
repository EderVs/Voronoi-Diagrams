"""Fortune's Algorithm to calculate Voronoi Diagrams.

General Solution.
"""
# Standard Library
from typing import Iterable, List, Any, Optional, Tuple

# Data structures
from .data_structures import LList, QQueue
from .data_structures.l import LNode

# Models
from .data_structures.models import (
    Site,
    Point,
    Bisector,
    Event,
    Intersection,
    Region,
    Boundary,
    PointBisector,
    PointBoundary,
    PointRegion,
)


class VoronoiDiagram:
    """Voronoi Diagram representation."""

    vertex: List[Point] = []
    bisectors: List[Bisector] = []
    sites: List[Site] = []

    def __init__(self, sites: Iterable[Site], site_class: Any = Site):
        """Construct and calculate Voronoi Diagram."""
        self.sites = list(sites)
        if site_class == Site:
            self.BISECTOR_CLASS = PointBisector
            self.REGION_CLASS = PointRegion
            self.BOUNDARY_CLASS = PointBoundary
        self._calculate_diagram()

    def add_vertex(self, point: Point) -> None:
        """Add point in the vertex list."""
        self.vertex.append(point)

    def add_bisector(self, bisector: Bisector) -> None:
        """Add point in the vertex list."""
        self.bisectors.append(bisector)

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
    ) -> Tuple[Boundary, Boundary, Region, Region, LNode, LNode, LNode]:
        """Update list L so that it contains ...,R*q,C-pq,R*p,C+pq,R*q,... in place of R*q."""
        boundary_p_q_plus = self.BOUNDARY_CLASS(bisector_p_q, True)
        boundary_p_q_minus = self.BOUNDARY_CLASS(bisector_p_q, False)
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
            r_q_left,
            r_q_right,
            r_q_left_node,
            r_p_node,
            r_q_right_node,
        )

    def _delete_intersection_in_boundary_from_q(
        self, boundary: Optional[Boundary]
    ) -> None:
        if boundary is not None and boundary.intersection is not None:
            self.q_queue.delete(boundary.intersection)
            boundary.intersection = None

    def _insert_intersection(
        self, boundary_1: Boundary, boundary_2: Boundary, region_node: LNode
    ) -> None:
        """Look for intersections between the the boundaries."""
        intersection_point = boundary_1.get_intersection(boundary_2)
        if intersection_point is not None:
            intersection = Intersection(
                intersection_point.x, intersection_point.y, region_node
            )
            # Insert intersection to Q.
            self.q_queue.enqueue(intersection)
            # Save intersection in both boundaries.
            boundary_1.intersection = intersection
            boundary_2.intersection = intersection

    def _insert_posible_intersections(
        self,
        left_boundary: Boundary,
        boundary_p_q_plus: Boundary,
        r_q_left_node: LNode,
        right_boundary: Boundary,
        boundary_p_q_minus: Boundary,
        r_q_right_node: LNode,
    ) -> None:
        """Insert posible intersections in Q."""
        # Left.
        if left_boundary is not None:
            self._insert_intersection(left_boundary, boundary_p_q_plus, r_q_left_node)

        # Right.
        if right_boundary is not None:
            self._insert_intersection(
                right_boundary, boundary_p_q_minus, r_q_right_node
            )

    def _handle_site(self, p: Site):
        """Handle when event is a site."""
        # Step 8.
        # Find an occurrence of a region R*q on L containing p.
        r_p, r_q, r_q_node = self._find_region_containing_p(p)
        left_region_node = r_q_node.left_neighbor
        right_region_node = r_q_node.right_neighbor

        # Step 9.
        # Create Bisector B*pq.
        # Actually we are creating Bpq.
        bisector_p_q = self.BISECTOR_CLASS(sites=(p, r_q.site))
        self.add_bisector(bisector_p_q)

        # Step 10.
        # Update list L so that it contains ...,R*q,C-pq,R*p,C+pq,R*q,... in place of R*q.
        (
            boundary_p_q_plus,
            boundary_p_q_minus,
            r_q_left,
            r_q_right,
            r_q_left_node,
            r_p_node,
            r_q_right_node,
        ) = self._update_list_l(r_p, r_q, bisector_p_q)

        # Step 11.
        # Delete from Q the intersection between the left and right boundary of R*q, if any.
        left_boundary: Optional[Boundary] = None
        right_boundary: Optional[Boundary] = None
        # Left
        if left_region_node is not None:
            left_boundary = left_region_node.value.right
            self._delete_intersection_in_boundary_from_q(left_boundary)
        # Right
        if right_region_node is not None:
            right_boundary = right_region_node.value.left
            self._delete_intersection_in_boundary_from_q(right_boundary)

        # Step 12.
        # Insert into Q the intersection between C-pq and its neighbor to the left on L, if any, and
        # the intersection between C+pq and its neighbor to the right, if any.
        self._insert_posible_intersections(
            left_boundary,
            boundary_p_q_plus,
            r_q_left_node,
            right_boundary,
            boundary_p_q_minus,
            r_q_right_node,
        )

    def _get_regions_and_nodes_of_intersection(self, p: Intersection):
        """Get regions and their nodes of the intersection p."""
        intersection_region_node = p.region_node
        # Left and right neighbor cannot be None because p is an intersection.
        r_q_node = intersection_region_node.left_neighbor
        r_q = r_q_node.value
        r_s_node = intersection_region_node.right_neighbor
        r_s = r_s_node.value
        return r_q, r_s, r_q_node, r_s_node

    def _handle_intersection(self, p: Intersection):
        """Handle when event is an intersection."""
        # Step 14.
        # Let p be the intersection of boundaries Cqr and Crs.
        intersection_region_node = p.region_node
        r_q, r_s, r_q_node, r_s_node = self._get_regions_and_nodes_of_intersection(p)

        # Step 15.
        # Create bisector B*qs.
        bisector_q_s = self.BISECTOR_CLASS(sites=(r_q.site, r_s.site))
        self.add_bisector(bisector_q_s)

        # Step 16.
        # Update list L so it contains Cqs instead of Cqr, Rr*, Crs
        boundary_q_s = self.BOUNDARY_CLASS(bisector_q_s, r_q.site.y > r_s.site.y)
        self.l_list.remove_region(intersection_region_node, boundary_q_s)

        # Step 17.
        # Delete from Q any intersection between Cqr and its neighbor to the
        # left and between Crs and its neighbor to the right.
        self.q_queue.delete(intersection_region_node.value.left.intersection)
        self.q_queue.delete(intersection_region_node.value.right.intersection)

        # Step 18.
        # Insert any intersections between Cqs and its neighbors to the left or right
        # into Q.
        left_boundary = r_q.left
        right_boundary = r_s.right
        self._insert_posible_intersections(
            left_boundary,
            boundary_q_s,
            r_q_node,
            right_boundary,
            boundary_q_s,
            r_q_node,
        )

        # Step 19.
        # Mark p as a vertex and as an endpoint of B*qr, B*rs and B*qs.
        self.add_vertex(p.point)
        # TODO: Add as an endpoint of B*qr, B*rs and B*qs.

    def _calculate_diagram(self):
        """Calculate point diagram."""
        # Step 1.
        self.q_queue = QQueue()
        for site in self.sites:
            self.q_queue.enqueue(site)
        # Step 2.
        p = self.q_queue.dequeue()
        # Step 3.
        r_p = self.REGION_CLASS(p, None, None)
        self.l_list = LList(r_p)
        # Step 4.
        while not self.q_queue.is_empty():
            # Step 5.
            p = self.q_queue.dequeue()
            # Step 6 and 7.
            if p.is_site:
                self._handle_site(p)
            # Step 13: p is an intersection.
            else:
                self._handle_intersection(p)


class FortunesAlgorithm:
    """Fortune's Algorithm implementation."""

    @staticmethod
    def calculate_voronoi_diagram(
        sites: Iterable[Point], site_class: Any = Site
    ) -> VoronoiDiagram:
        """Calculate Voronoi Diagram."""
        voronoi_diagram = VoronoiDiagram(sites, site_class)

        return voronoi_diagram
