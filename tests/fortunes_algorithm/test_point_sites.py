"""Test Algorithm using Point Sites."""
# Standard
from typing import List, Any

# Models
from voronoi_diagrams.data_structures.models import Site, PointBisector, Point

# Algorithm
from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm, VoronoiDiagram


class TestPointSites:
    """Test formula."""

    def _check_bisectors_and_vertex(
        self,
        voronoi_diagram: VoronoiDiagram,
        expected_bisectors: List[PointBisector],
        expected_vertex: List[Point],
    ):
        print(voronoi_diagram.bisectors)
        print(voronoi_diagram.vertex)
        # Bisectors.
        assert len(voronoi_diagram.bisectors) == len(expected_bisectors)
        for bisector in voronoi_diagram.bisectors:
            assert bisector in expected_bisectors

        # Vertex.
        assert len(voronoi_diagram.vertex) == len(expected_vertex)
        for vertex in voronoi_diagram.vertex:
            assert vertex in expected_vertex

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
        self._check_bisectors_and_vertex(voronoi_diagram, [bisector], [])

    def test_2_sites_same_x(self):
        """Test when all sites have same x coordinate."""
        p = Point(2, -2)
        q = Point(2, 2)
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        points = (p, q)
        bisector_p_q = PointBisector(sites=(site_p, site_q))

        expected_bisectors = [bisector_p_q]
        expected_vertex = []

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_intersection_right(self):
        """Create Diagram of 3 sites.

        There is going to be one intersection.
        """
        p = Point(0, 0)
        q = Point(2, 2)
        r = Point(1, -1)
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_p_r = PointBisector(sites=(site_p, site_r))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_p_r, bisector_q_r]
        expected_vertex = [Point(1.5, 0.5)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_intersection_left(self):
        """Create Diagram of 3 sites.

        There is going to be one intersection.
        """
        p = Point(0, 0)
        q = Point(-0.6, 2)
        r = Point(1, -1)
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_p_r = PointBisector(sites=(site_p, site_r))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_p_r, bisector_q_r]
        expected_vertex = [Point(2.9857142857142858, 1.9857142857142858)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_intersection_middle(self):
        """Create Diagram of 3 sites.

        There is going to be one intersection.
        """
        p = Point(0, 0)
        q = Point(0.49, 1.716)
        r = Point(1, -1)
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_p_r = PointBisector(sites=(site_p, site_r))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_p_r, bisector_q_r]
        expected_vertex = [Point(1.4997180417044425, 0.49971804170444234)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_intersection_up(self):
        """Create Diagram of 3 sites.

        There is going to be one intersection.
        """
        p = Point(0, 0)
        q = Point(0, 2)
        r = Point(1, -1)
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_p_r = PointBisector(sites=(site_p, site_r))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_p_r, bisector_q_r]
        expected_vertex = [Point(2, 1)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_intersection_in_site(self):
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
        expected_vertex = [Point(2.0, 0)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_3_sites_same_x(self):
        """Test when all sites have same x coordinate."""
        p = Point(2, -2)
        q = Point(2, 0)
        r = Point(2, 2)
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_q_r]
        expected_vertex = []

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_3_sites_same_y(self):
        """Test when all sites have same x coordinate."""
        p = Point(-2, 2)
        q = Point(0, 2)
        r = Point(2, 2)
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_q_r]
        expected_vertex = []

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_4_sites(self):
        """Create Diagram of 4 sites.

        There is going to be one intersection.
        """
        p1 = Point(0, 0)
        p2 = Point(0.49, 1.716)
        p3 = Point(1, -1)
        p4 = Point(6.6, 5.44)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        points = (p1, p2, p3, p4)
        bisector_p1_p2 = PointBisector(sites=(site_p1, site_p2))
        bisector_p1_p3 = PointBisector(sites=(site_p1, site_p3))
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p2_p4 = PointBisector(sites=(site_p2, site_p4))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))

        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p2_p3,
            bisector_p2_p4,
            bisector_p3_p4,
        ]
        expected_vertex = [
            Point(1.4997180417044425, 0.49971804170444234),
            Point(5.018474882664648, 1.1604566237698712),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_4_sites_up(self):
        """Create Diagram of 4 sites.

        There is going to be one intersection.
        """
        p1 = Point(0, 0)
        p2 = Point(0.5, 1.7)
        p3 = Point(1, -1)
        p4 = Point(0.5, 3)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        points = (p1, p2, p3, p4)
        bisector_p1_p2 = PointBisector(sites=(site_p1, site_p2))
        bisector_p1_p3 = PointBisector(sites=(site_p1, site_p3))
        bisector_p1_p4 = PointBisector(sites=(site_p1, site_p4))
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p2_p4 = PointBisector(sites=(site_p2, site_p4))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))

        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p1_p4,
            bisector_p2_p3,
            bisector_p2_p4,
            bisector_p3_p4,
        ]
        expected_vertex = [
            Point(1.486363636363636, 0.4863636363636364),
            Point(-4.8500000000000005, 2.35),
            Point(11.550000000000002, 2.35),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_4_sites_one_interception(self):
        """Create Diagram of 4 sites.

        There is going to be one intersection.
        """
        p1 = Point(0.5, 1.7)
        p2 = Point(2.2, 2)
        p3 = Point(0.8, 0)
        p4 = Point(2.5, 0.3)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        points = (p1, p2, p3, p4)
        bisector_p1_p2 = PointBisector(sites=(site_p1, site_p2))
        bisector_p1_p3 = PointBisector(sites=(site_p1, site_p3))
        bisector_p1_p4 = PointBisector(sites=(site_p1, site_p4))
        bisector_p2_p4 = PointBisector(sites=(site_p2, site_p4))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))

        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p1_p4,
            bisector_p2_p4,
            bisector_p3_p4,
        ]
        # Precision errors in operations but we agree that is almost the same point.
        expected_vertex = [Point(1.5, 1.0), Point(1.5, 0.9999999999999998)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_4_sites_same_x(self):
        """Test when all sites have same x coordinate."""
        p1 = Point(0, 1)
        p2 = Point(0, -1)
        p3 = Point(0, 0)
        p4 = Point(0, 0.3)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        points = (p1, p2, p3, p4)
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))
        bisector_p1_p4 = PointBisector(sites=(site_p1, site_p4))

        expected_bisectors = [bisector_p2_p3, bisector_p3_p4, bisector_p1_p4]
        expected_vertex = []

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_4_sites_same_y(self):
        """Test when all sites have same y coordinate."""
        p1 = Point(1, 0)
        p2 = Point(-1, 0)
        p3 = Point(0, 0)
        p4 = Point(0.3, 0)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        points = (p1, p2, p3, p4)
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))
        bisector_p1_p4 = PointBisector(sites=(site_p1, site_p4))

        expected_bisectors = [bisector_p2_p3, bisector_p3_p4, bisector_p1_p4]
        expected_vertex = []

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_4_sites_square(self):
        """Test when sites form a square."""
        p1 = Point(-1, -1)
        p2 = Point(1, -1)
        p3 = Point(-1, 1)
        p4 = Point(1, 1)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        points = (p1, p2, p3, p4)
        bisector_p1_p2 = PointBisector(sites=(site_p1, site_p2))
        bisector_p1_p3 = PointBisector(sites=(site_p1, site_p3))
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p2_p4 = PointBisector(sites=(site_p2, site_p4))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))

        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p2_p3,
            bisector_p2_p4,
            bisector_p3_p4,
        ]
        expected_vertex = [Point(0, 0)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_4_sites_rhombus(self):
        """Test when sites form a rhombus."""
        p1 = Point(0, -1)
        p2 = Point(1, 0)
        p3 = Point(-1, 0)
        p4 = Point(0, 1)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        points = (p1, p2, p3, p4)
        bisector_p1_p2 = PointBisector(sites=(site_p1, site_p2))
        bisector_p1_p3 = PointBisector(sites=(site_p1, site_p3))
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p2_p4 = PointBisector(sites=(site_p2, site_p4))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))

        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p2_p3,
            bisector_p2_p4,
            bisector_p3_p4,
        ]
        expected_vertex = [Point(0, 0)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_5_sites_square_and_one(self):
        """Test when sites form a square."""
        p1 = Point(-1, -1)
        p2 = Point(1, -1)
        p3 = Point(-1, 1)
        p4 = Point(1, 1)
        p5 = Point(5, 5)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        site_p5 = Site(p5.x, p5.y)
        points = (p1, p2, p3, p4, p5)
        bisector_p1_p2 = PointBisector(sites=(site_p1, site_p2))
        bisector_p1_p3 = PointBisector(sites=(site_p1, site_p3))
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p2_p4 = PointBisector(sites=(site_p2, site_p4))
        bisector_p2_p5 = PointBisector(sites=(site_p2, site_p5))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))
        bisector_p3_p5 = PointBisector(sites=(site_p3, site_p5))
        bisector_p4_p5 = PointBisector(sites=(site_p4, site_p5))

        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p2_p3,
            bisector_p2_p5,
            bisector_p2_p4,
            bisector_p3_p4,
            bisector_p3_p5,
            bisector_p4_p5,
        ]
        expected_vertex = [Point(0, 0), Point(6, 0), Point(0, 6)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_5_sites_rhombus_and_one(self):
        """Test when sites form a rhombus."""
        p1 = Point(0, -1)
        p2 = Point(-1, 0)
        p3 = Point(1, 0)
        p4 = Point(0, 1)
        p5 = Point(0, 5)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        site_p5 = Site(p5.x, p5.y)
        points = (p1, p2, p3, p4, p5)
        bisector_p1_p2 = PointBisector(sites=(site_p1, site_p2))
        bisector_p1_p3 = PointBisector(sites=(site_p1, site_p3))
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p2_p4 = PointBisector(sites=(site_p2, site_p4))
        bisector_p2_p5 = PointBisector(sites=(site_p2, site_p5))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))
        bisector_p3_p5 = PointBisector(sites=(site_p3, site_p5))
        bisector_p4_p5 = PointBisector(sites=(site_p4, site_p5))

        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p2_p3,
            bisector_p2_p4,
            bisector_p2_p5,
            bisector_p3_p4,
            bisector_p3_p5,
            bisector_p4_p5,
        ]
        expected_vertex = [Point(0, 0), Point(-3, 3), Point(3, 3)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_5_sites_rhombus_and_one_more_intersection(self):
        """Test when sites form a rhombus."""
        p1 = Point(0, -1)
        p2 = Point(-1, 0)
        p3 = Point(1, 0)
        p4 = Point(0, 1)
        p5 = Point(4, 4)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        site_p5 = Site(p5.x, p5.y)
        points = (p1, p2, p3, p4, p5)
        bisector_p1_p2 = PointBisector(sites=(site_p1, site_p2))
        bisector_p1_p3 = PointBisector(sites=(site_p1, site_p3))
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p2_p4 = PointBisector(sites=(site_p2, site_p4))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))
        bisector_p3_p5 = PointBisector(sites=(site_p3, site_p5))
        bisector_p4_p5 = PointBisector(sites=(site_p4, site_p5))

        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p2_p3,
            bisector_p2_p4,
            bisector_p3_p4,
            bisector_p3_p5,
            bisector_p4_p5,
        ]
        expected_vertex = [Point(0, 0), Point(2.2142857142857144, 2.2142857142857144)]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_5_sites_square_in_middle(self):
        """Test when sites form a square area."""
        p1 = Point(0, -1)
        p2 = Point(-1, 0)
        p3 = Point(1, 0)
        p4 = Point(0, 1)
        p5 = Point(0, 0)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        site_p5 = Site(p5.x, p5.y)
        points = (p1, p2, p3, p4, p5)
        bisector_p1_p2 = PointBisector(sites=(site_p1, site_p2))
        bisector_p1_p3 = PointBisector(sites=(site_p1, site_p3))
        bisector_p1_p5 = PointBisector(sites=(site_p1, site_p5))
        bisector_p2_p4 = PointBisector(sites=(site_p2, site_p4))
        bisector_p2_p5 = PointBisector(sites=(site_p2, site_p5))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))
        bisector_p3_p5 = PointBisector(sites=(site_p3, site_p5))
        bisector_p4_p5 = PointBisector(sites=(site_p4, site_p5))

        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p1_p5,
            bisector_p2_p4,
            bisector_p2_p5,
            bisector_p3_p4,
            bisector_p3_p5,
            bisector_p4_p5,
        ]
        expected_vertex = [
            Point(-0.5, -0.5),
            Point(-0.5, 0.5),
            Point(0.5, -0.5),
            Point(0.5, 0.5),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )

    def test_5_sites_rhombus_in_middle(self):
        """Test when sites form a rhombus area."""
        p1 = Point(1, -1)
        p2 = Point(-1, -1)
        p3 = Point(1, 1)
        p4 = Point(-1, 1)
        p5 = Point(0, 0)
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        site_p5 = Site(p5.x, p5.y)
        points = (p1, p2, p3, p4, p5)
        bisector_p1_p2 = PointBisector(sites=(site_p1, site_p2))
        bisector_p1_p3 = PointBisector(sites=(site_p1, site_p3))
        bisector_p1_p5 = PointBisector(sites=(site_p1, site_p5))
        bisector_p2_p4 = PointBisector(sites=(site_p2, site_p4))
        bisector_p2_p5 = PointBisector(sites=(site_p2, site_p5))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))
        bisector_p3_p5 = PointBisector(sites=(site_p3, site_p5))
        bisector_p4_p5 = PointBisector(sites=(site_p4, site_p5))

        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p1_p5,
            bisector_p2_p4,
            bisector_p2_p5,
            bisector_p3_p4,
            bisector_p3_p5,
            bisector_p4_p5,
        ]
        expected_vertex = [
            Point(0, -1),
            Point(-1, 0),
            Point(1, 0),
            Point(0, 1),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertex
        )
