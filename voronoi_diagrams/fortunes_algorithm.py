"""Fortune's Algorithm to calculate Voronoi Diagrams.

General Solution.
"""
# Standard Library
from typing import Iterable, List, Any, Optional

# Data structures
from data_structures import LList, QQueue

# Models
from data_structures.models import (
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

    def add_vertex(self, point: Point) -> None:
        """Add point in the vertex list."""
        self.vertex.append(point)

    def add_bisector(self, bisector: Bisector) -> None:
        """Add point in the vertex list."""
        self.bisectors.append(Bisector)


class FortunesAlgorithm:
    """Fortune's Algorithm implementation."""

    @classmethod
    def calculate_voronoi_diagram(
        sites: Iterable[Point], site_class: Any = Site
    ) -> VoronoiDiagram:
        """Calculate Voronoi Diagram."""
        if site_class == Site:
            BISECTOR_CLASS = PointBisector
            REGION_CLASS = PointRegion
            BOUNDARY_CLASS = PointBoundary
        voronoi_diagram = VoronoiDiagram()

        # Step 1.
        q_queue = QQueue()
        for site in sites:
            q_queue.enqueue(site)

        # Step 2.
        p = q_queue.dequeue()

        # Step 3.
        r_p = REGION_CLASS(p, None, None)
        l_list = LList(r_p)

        # Step 4.
        while not q_queue.is_empty():
            # Step 5.
            p = q_queue.dequeue()
            # Step 6 and 7.
            if p.is_site:
                # Step 8.
                r_p = REGION_CLASS(p, None, None)
                r_q_node = l_list.search_region_node(r_p)
                r_q = r_q_node.value
                # Step 9.
                bisector_p_q = BISECTOR_CLASS(sites=(p, r_q.site))
                voronoi_diagram.bisectors.append(bisector_p_q)
                # Step 10.
                boundary_p_q_plus = BOUNDARY_CLASS(bisector_p_q, True)
                boundary_p_q_minus = BOUNDARY_CLASS(bisector_p_q, False)
                r_q_left = REGION_CLASS(r_q.site, r_q.left, boundary_p_q_minus)
                r_q_right = REGION_CLASS(r_q.site, boundary_p_q_plus, r_q.right)
                r_p.left = boundary_p_q_minus
                r_p.right = boundary_p_q_plus
                # Update L list.
                r_q_left_node, r_p_node, r_q_right_node = l_list.update_regions(
                    r_q_left, r_p, r_q_right
                )
                # Step 11.
                # Delete from Q the intersection between the left and right boundary of
                # R_q, if any.
                left_right_intersection = None
                left_boundary: Optional[Boundary] = None
                right_boundary: Optional[Boundary] = None

                left_region_node = r_q_node.left_neighbor
                if left_region_node is not None:
                    left_boundary = left_region_node.value.right
                    if left_boundary is not None:
                        left_right_intersection = left_boundary.intersection
                        if left_boundary.intersection is not None:
                            left_boundary.intersection = None

                right_region_node = r_q_node.right_neighbor
                if right_region_node is not None:
                    right_boundary = right_region_node.value.left
                    if right_boundary is not None:
                        left_right_intersection = right_boundary.intersection
                        if right_boundary.intersection is not None:
                            right_boundary.intersection = None

                q_queue.delete(left_right_intersection)

                # Step 12.
                intersections_to_add: List[Intersection] = []
                # Left.
                if left_boundary is not None:
                    left_intersection_point = left_boundary.get_intersection(
                        boundary_p_q_plus
                    )
                    if left_intersection_point is not None:
                        left_intersection = Intersection(
                            left_intersection_point.x,
                            left_intersection_point.y,
                            r_q_left_node,
                        )
                        intersections_to_add.append(left_intersection)

                # Right.
                if right_boundary is not None:
                    right_intersection_point = right_boundary.get_intersection(
                        boundary_p_q_minus
                    )
                    if right_intersection_point is not None:
                        right_intersection = Intersection(
                            right_intersection_point.x,
                            right_intersection_point.y,
                            r_q_right_node,
                        )
                        intersections_to_add.append(right_intersection)
                # Add intersections to Q
                for intersection in intersections_to_add:
                    q_queue.enqueue(intersection)

            # Step 13: p is an intersection.
            else:
                # Step 14.
                p_intersection: Intersection = p
                intersection_region_node = p_intersection.region_node
                # Left neighbor cannot be None because p is an intersection.
                r_q = intersection_region_node.left_neighbor.value
                r_s = intersection_region_node.right_neighbor.value
                # Step 15.
                bisector_q_s = BISECTOR_CLASS(sites=(r_q.site, r_s.site))
                voronoi_diagram.bisectors.append(bisector_q_s)
                # Step 16.
                # Update list L so it contains Cqs instead of Cqr, Rr*, Crs
                boundary_q_s = BOUNDARY_CLASS(bisector_q_s, r_q.site.y > r_s.site.y)
                l_list.remove_region(intersection_region_node, boundary_q_s)

        return voronoi_diagram
