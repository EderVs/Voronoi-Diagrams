"""Test Algorithm using Point Sites."""
# Standard
from typing import List, Any

# Models
from voronoi_diagrams.data_structures.models import Site, PointBisector, Point

# Algorithm
from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm, VoronoiDiagram


class TestPointSites:
    """Test formula."""

    def test_2_point_sites(self):
        """Test 2 point sites.
        
        There are no intersections (vertex) in this test.
        """
        p = Point(0, 0)
        q = Point(2, 2)
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        points = (p, q)
        bisector = PointBisector((site_p, site_q))
        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)
        assert len(voronoi_diagram.bisectors) == 1
        assert voronoi_diagram.bisectors[0].sites == bisector.sites
        assert len(voronoi_diagram.vertex) == 0

    def test_first_intersection(self):
        """Create Diagram of 3 sites.

        There is going to be one intersection.
        """
        p = Point(0, 0)
        q = Point(2, 2)
        r = Point(2, -2)
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_p_r = PointBisector(sites=(site_p, site_r))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_p_r, bisector_q_r]
        expected_vertex = [Point(2.0, 2.0)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        # Bisectors.
        assert len(voronoi_diagram.bisectors) == 3
        for bisector in voronoi_diagram.bisectors:
            assert bisector in expected_bisectors

        # Vertex.
        assert len(voronoi_diagram.vertex) == 1
        for vertex in voronoi_diagram.vertex:
            assert vertex in expected_vertex
