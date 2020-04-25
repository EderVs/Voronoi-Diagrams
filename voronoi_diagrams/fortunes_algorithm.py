"""Fortune's Algorithm to calculate Voronoi Diagrams.

General Solution.
"""
# Standard Library
from typing import Iterable, List, Any, Optional, Tuple, Set

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

    vertex: List[Point]
    _vertex: Set[Tuple[float, float]]
    bisectors: List[Bisector]
    _bisectors: Set[Tuple[Tuple[float, float], Tuple[float, float]]]
    sites: List[Site]

    def __init__(self, sites: Iterable[Site], site_class: Any = Site):
        """Construct and calculate Voronoi Diagram."""
        self.vertex = []
        self._vertex = set()
        self.bisectors = []
        self._bisectors = set()
        self.sites = list(sites)
        if site_class == Site:
            self.BISECTOR_CLASS = PointBisector
            self.REGION_CLASS = PointRegion
            self.BOUNDARY_CLASS = PointBoundary
        self._calculate_diagram()

    def add_vertex(self, point: Point) -> None:
        """Add point in the vertex list."""
        point_tuple = point.get_tuple()
        if point_tuple not in self._vertex:
            self._vertex.add(point_tuple)
            self.vertex.append(point)

    def add_bisector(self, bisector: Bisector) -> None:
        """Add point in the vertex list."""
        site_points = (
            bisector.sites[0].point.get_tuple(),
            bisector.sites[1].point.get_tuple(),
        )
        if site_points not in self._bisectors:
            self._bisectors.add(site_points)
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

        intersection_point = boundary_1.get_intersection(boundary_2)
        if intersection_point is not None and (
            (
                not boundary_1.sign
                and intersection_point.x <= region_node.value.site.point.x
            )
            or (
                boundary_1.sign
                and intersection_point.x >= region_node.value.site.point.x
            )
        ):
            intersection = Intersection(
                intersection_point.x, intersection_point.y, region_node
            )
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
        left_boundary = r_q.left
        right_boundary = r_s.right

        # Step 15.
        # Create bisector B*qs.
        bisector_q_s = self.BISECTOR_CLASS(sites=(r_q.site, r_s.site))
        self.add_bisector(bisector_q_s)

        # Step 16.
        # Update list L so it contains Cqs instead of Cqr, Rr*, Crs
        boundary_q_s = self.BOUNDARY_CLASS(
            bisector_q_s, r_q.site.point.y > r_s.site.point.y
        )
        intersection_region_node_value_left = intersection_region_node.value.left
        intersection_region_node_value_right = intersection_region_node.value.right
        left_region_node = intersection_region_node.left_neighbor
        right_region_node = intersection_region_node.right_neighbor
        self.l_list.remove_region(intersection_region_node, boundary_q_s)

        # Step 17.
        # Delete from Q any intersection between Cqr and its neighbor to the
        # left and between Crs and its neighbor to the right.
        # TODO: Put None the intersection of the other boundaries.
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
        points: Iterable[Point], site_class: Any = Site
    ) -> VoronoiDiagram:
        """Calculate Voronoi Diagram."""
        sites = [site_class(point.x, point.y) for point in points]
        voronoi_diagram = VoronoiDiagram(sites, site_class)

        return voronoi_diagram
