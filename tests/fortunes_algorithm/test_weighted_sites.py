"""Test Algorithm using Weighted Point Sites."""

# Standard
from typing import List, Any

# Models
from voronoi_diagrams.models import WeightedSite, WeightedPointBisector, Point

# Algorithm
from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm, VoronoiDiagram

# Math
from decimal import Decimal


class TestWeightedSites:
    """Test formula."""

    def _check_bisectors_and_vertex(
        self,
        voronoi_diagram: VoronoiDiagram,
        expected_bisectors: List[WeightedPointBisector],
        expected_vertices: List[Point],
    ):
        print(voronoi_diagram.bisectors)
        print(voronoi_diagram.vertices)
        # Bisectors.
        assert len(voronoi_diagram.bisectors) == len(expected_bisectors)
        for bisector in voronoi_diagram.bisectors:
            assert bisector in expected_bisectors

        # Vertex.
        assert len(voronoi_diagram.vertices) == len(expected_vertices)
        for vertex in voronoi_diagram.vertices:
            assert vertex in expected_vertices

    def test_2_sites(self):
        """Test 2 sites.

        There are no intersections (vertices) in this test.
        """
        p = Point(Decimal(0), Decimal(0))
        p_w = Decimal(1.5)
        q = Point(Decimal(10), Decimal(12))
        q_w = Decimal(2.5)
        site_p = WeightedSite(p.x, p.y, p_w)
        site_q = WeightedSite(q.x, q.y, q_w)
        points_and_weights = ((p, p_w), (q, q_w))
        bisector = WeightedPointBisector((site_p, site_q))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        self._check_bisectors_and_vertex(voronoi_diagram, [bisector], [])

    def test_2_sites_without_weight(self):
        """Test 2 sites without weight.

        There are no intersections (vertices) in this test.
        """
        p = Point(Decimal(0), Decimal(0))
        p_w = Decimal(0)
        q = Point(Decimal(10), Decimal(12))
        q_w = Decimal(0)
        site_p = WeightedSite(p.x, p.y, p_w)
        site_q = WeightedSite(q.x, q.y, q_w)
        points_and_weights = ((p, p_w), (q, q_w))
        bisector = WeightedPointBisector((site_p, site_q))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        self._check_bisectors_and_vertex(voronoi_diagram, [bisector], [])

    def test_2_sites(self):
        """Test 2 sites.

        There are no intersections (vertices) in this test.
        """
        p1 = Point(Decimal(38), Decimal(2))
        p1_w = Decimal(1)
        p2 = Point(Decimal(34), Decimal(39))
        p2_w = Decimal(2)
        p3 = Point(Decimal(10), Decimal(7))
        p3_w = Decimal(5)
        site_p1 = WeightedSite(p1.x, p1.y, p1_w)
        site_p2 = WeightedSite(p2.x, p2.y, p2_w)
        site_p3 = WeightedSite(p3.x, p3.y, p3_w)
        points_and_weights = ((p1, p1_w), (p2, p2_w), (p3, p3_w))
        bisector_p1_p2 = WeightedPointBisector((site_p1, site_p2))
        bisector_p1_p3 = WeightedPointBisector((site_p1, site_p3))
        bisector_p2_p3 = WeightedPointBisector((site_p2, site_p3))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        expected_bisectors = [bisector_p1_p2, bisector_p1_p3, bisector_p2_p3]
        expected_vertices = [
            Point(
                Decimal("23.7599947570548692965530790388584136962890625"),
                Decimal("19.77888156319230716917445533908903598785400390625"),
            )
        ]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )
