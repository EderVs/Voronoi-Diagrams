"""Test Algorithm using Point Sites."""
# Standard
from typing import List, Any

# Models
from voronoi_diagrams.models import Site, PointBisector, Point

# Algorithm
from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm, VoronoiDiagram

# Math
from decimal import Decimal


class TestPointSites:
    """Test formula."""

    def _check_bisectors_and_vertex(
        self,
        voronoi_diagram: VoronoiDiagram,
        expected_bisectors: List[PointBisector],
        expected_vertices: List[Point],
    ):
        print(voronoi_diagram.bisectors_list)
        print(voronoi_diagram.vertices_list)
        # Bisectors.
        assert len(voronoi_diagram.bisectors_list) == len(expected_bisectors)
        for bisector in voronoi_diagram.bisectors_list:
            assert bisector in expected_bisectors

        # Vertex.
        assert len(voronoi_diagram.vertices_list) == len(expected_vertices)
        for vertex in voronoi_diagram.vertices_list:
            assert vertex in expected_vertices

    def test_2_point_sites(self):
        """Test 2 point sites.

        There are no intersections (vertex) in this test.
        """
        p = Point(Decimal(0), Decimal(0))
        q = Point(Decimal(2), Decimal(2))
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        points = (p, q)
        bisector = PointBisector((site_p, site_q))
        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)
        self._check_bisectors_and_vertex(voronoi_diagram, [bisector], [])

    def test_2_sites_same_x(self):
        """Test when all sites have same x coordinate."""
        p = Point(Decimal(2), Decimal(-2))
        q = Point(Decimal(2), Decimal(2))
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        points = (p, q)
        bisector_p_q = PointBisector(sites=(site_p, site_q))

        expected_bisectors = [bisector_p_q]
        expected_vertices = []

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_intersection_right(self):
        """Create Diagram of 3 sites.

        There is going to be one intersection.
        """
        p = Point(Decimal(0), Decimal(0))
        q = Point(Decimal(2), Decimal(2))
        r = Point(Decimal(1), Decimal(-1))
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_p_r = PointBisector(sites=(site_p, site_r))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_p_r, bisector_q_r]
        expected_vertices = [Point(Decimal(1.5), Decimal(0.5))]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_intersection_left(self):
        """Create Diagram of 3 sites.

        There is going to be one intersection.
        """
        p = Point(Decimal(0), Decimal(0))
        q = Point(Decimal(-0.6), Decimal(2))
        r = Point(Decimal(1), Decimal(-1))
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_p_r = PointBisector(sites=(site_p, site_r))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_p_r, bisector_q_r]
        expected_vertices = [
            Point(
                Decimal("2.985714285714285657415106289"),
                Decimal("1.985714285714285657415106289"),
            )
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_intersection_middle(self):
        """Create Diagram of 3 sites.

        There is going to be one intersection.
        """
        p = Point(Decimal(0), Decimal(0))
        q = Point(Decimal(0.49), Decimal(1.716))
        r = Point(Decimal(1), Decimal(-1))
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_p_r = PointBisector(sites=(site_p, site_r))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_p_r, bisector_q_r]
        expected_vertices = [
            Point(
                Decimal("1.499718041704442417152644862"),
                Decimal("0.4997180417044424171526448628"),
            )
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_intersection_up(self):
        """Create Diagram of 3 sites.

        There is going to be one intersection.
        """
        p = Point(Decimal(0), Decimal(0))
        q = Point(Decimal(0), Decimal(2))
        r = Point(Decimal(1), Decimal(-1))
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_p_r = PointBisector(sites=(site_p, site_r))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_p_r, bisector_q_r]
        expected_vertices = [Point(Decimal(2), Decimal(1))]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_intersection_in_site(self):
        """Create Diagram of 3 sites.

        There is going to be one intersection.
        """
        p = Point(Decimal(0), Decimal(0))
        q = Point(Decimal(2), Decimal(2))
        r = Point(Decimal(2), Decimal(-2))
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_p_r = PointBisector(sites=(site_p, site_r))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_p_r, bisector_q_r]
        expected_vertices = [Point(Decimal(2.0), Decimal(0))]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_3_sites_same_x(self):
        """Test when all sites have same x coordinate."""
        p = Point(Decimal(2), Decimal(-2))
        q = Point(Decimal(2), Decimal(0))
        r = Point(Decimal(2), Decimal(2))
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_q_r]
        expected_vertices = []

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_3_sites_same_y(self):
        """Test when all sites have same x coordinate."""
        p = Point(Decimal(-2), Decimal(2))
        q = Point(Decimal(0), Decimal(2))
        r = Point(Decimal(2), Decimal(2))
        site_p = Site(p.x, p.y)
        site_q = Site(q.x, q.y)
        site_r = Site(r.x, r.y)
        points = (p, q, r)
        bisector_p_q = PointBisector(sites=(site_p, site_q))
        bisector_q_r = PointBisector(sites=(site_q, site_r))

        expected_bisectors = [bisector_p_q, bisector_q_r]
        expected_vertices = []

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_4_sites(self):
        """Create Diagram of 4 sites.

        There is going to be one intersection.
        """
        p1 = Point(Decimal(0), Decimal(0))
        p2 = Point(Decimal(0.49), Decimal(1.716))
        p3 = Point(Decimal(1), Decimal(-1))
        p4 = Point(Decimal(6.6), Decimal(5.44))
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
        expected_vertices = [
            Point(
                Decimal("1.499718041704442417152644862"),
                Decimal("0.4997180417044424171526448628"),
            ),
            Point(
                Decimal("5.018474882664648148876445313"),
                Decimal("1.160456623769871347338581763"),
            ),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_4_sites_up(self):
        """Create Diagram of 4 sites.

        There is going to be one intersection.
        """
        p1 = Point(Decimal(0), Decimal(0))
        p2 = Point(Decimal(0.5), Decimal(1.7))
        p3 = Point(Decimal(1), Decimal(-1))
        p4 = Point(Decimal(0.5), Decimal(3))
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
        expected_vertices = [
            Point(
                Decimal("1.486363636363636339138053920"),
                Decimal("0.4863636363636363391380539193"),
            ),
            Point(
                Decimal("-4.849999999999999866773237046"),
                Decimal("2.349999999999999977795539508"),
            ),
            Point(
                Decimal("11.54999999999999982236431606"),
                Decimal("2.349999999999999977795539508"),
            ),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_4_sites_one_interception(self):
        """Create Diagram of 4 sites.

        There is going to be one intersection.
        """
        p1 = Point(Decimal(0.5), Decimal(1.7))
        p2 = Point(Decimal(2.2), Decimal(2))
        p3 = Point(Decimal(0.8), Decimal(0))
        p4 = Point(Decimal(2.5), Decimal(0.3))
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
        expected_vertices = [
            Point(
                Decimal("1.500000000000000022167204686"),
                Decimal("1.000000000000000003911859650"),
            ),
            Point(
                Decimal("1.500000000000000076933239794"),
                Decimal("1.000000000000000082149052662"),
            ),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_4_sites_same_x(self):
        """Test when all sites have same x coordinate."""
        p1 = Point(Decimal(0), Decimal(1))
        p2 = Point(Decimal(0), Decimal(-1))
        p3 = Point(Decimal(0), Decimal(0))
        p4 = Point(Decimal(0), Decimal(0.3))
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        points = (p1, p2, p3, p4)
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))
        bisector_p1_p4 = PointBisector(sites=(site_p1, site_p4))

        expected_bisectors = [bisector_p2_p3, bisector_p3_p4, bisector_p1_p4]
        expected_vertices = []

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_4_sites_same_y(self):
        """Test when all sites have same y coordinate."""
        p1 = Point(Decimal(1), Decimal(0))
        p2 = Point(Decimal(-1), Decimal(0))
        p3 = Point(Decimal(0), Decimal(0))
        p4 = Point(Decimal(0.3), Decimal(0))
        site_p1 = Site(p1.x, p1.y)
        site_p2 = Site(p2.x, p2.y)
        site_p3 = Site(p3.x, p3.y)
        site_p4 = Site(p4.x, p4.y)
        points = (p1, p2, p3, p4)
        bisector_p2_p3 = PointBisector(sites=(site_p2, site_p3))
        bisector_p3_p4 = PointBisector(sites=(site_p3, site_p4))
        bisector_p1_p4 = PointBisector(sites=(site_p1, site_p4))

        expected_bisectors = [bisector_p2_p3, bisector_p3_p4, bisector_p1_p4]
        expected_vertices = []

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_4_sites_square(self):
        """Test when sites form a square."""
        p1 = Point(Decimal(-1), Decimal(-1))
        p2 = Point(Decimal(1), Decimal(-1))
        p3 = Point(Decimal(-1), Decimal(1))
        p4 = Point(Decimal(1), Decimal(1))
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
        expected_vertices = [Point(Decimal(0), Decimal(0))]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_4_sites_rhombus(self):
        """Test when sites form a rhombus."""
        p1 = Point(Decimal(0), Decimal(-1))
        p2 = Point(Decimal(1), Decimal(0))
        p3 = Point(Decimal(-1), Decimal(0))
        p4 = Point(Decimal(0), Decimal(1))
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
        expected_vertices = [Point(Decimal(0), Decimal(0))]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_5_sites_square_and_one(self):
        """Test when sites form a square."""
        p1 = Point(Decimal(-1), Decimal(-1))
        p2 = Point(Decimal(1), Decimal(-1))
        p3 = Point(Decimal(-1), Decimal(1))
        p4 = Point(Decimal(1), Decimal(1))
        p5 = Point(Decimal(5), Decimal(5))
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
        expected_vertices = [
            Point(Decimal(0), Decimal(0)),
            Point(Decimal(6), Decimal(0)),
            Point(Decimal(0), Decimal(6)),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_5_sites_rhombus_and_one(self):
        """Test when sites form a rhombus."""
        p1 = Point(Decimal(0), Decimal(-1))
        p2 = Point(Decimal(-1), Decimal(0))
        p3 = Point(Decimal(1), Decimal(0))
        p4 = Point(Decimal(0), Decimal(1))
        p5 = Point(Decimal(0), Decimal(5))
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
        expected_vertices = [
            Point(Decimal(0), Decimal(0)),
            Point(Decimal(-3), Decimal(3)),
            Point(Decimal(3), Decimal(3)),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_5_sites_rhombus_and_one_more_intersection(self):
        """Test when sites form a rhombus."""
        p1 = Point(Decimal(0), Decimal(-1))
        p2 = Point(Decimal(-1), Decimal(0))
        p3 = Point(Decimal(1), Decimal(0))
        p4 = Point(Decimal(0), Decimal(1))
        p5 = Point(Decimal(4), Decimal(4))
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
        expected_vertices = [
            Point(Decimal(0), Decimal(0)),
            Point(
                Decimal("2.214285714285714285714285714"),
                Decimal("2.214285714285714285714285714"),
            ),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_5_sites_square_in_middle(self):
        """Test when sites form a square area."""
        p1 = Point(Decimal(0), Decimal(-1))
        p2 = Point(Decimal(-1), Decimal(0))
        p3 = Point(Decimal(1), Decimal(0))
        p4 = Point(Decimal(0), Decimal(1))
        p5 = Point(Decimal(0), Decimal(0))
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
        expected_vertices = [
            Point(Decimal(-0.5), Decimal(-0.5)),
            Point(Decimal(-0.5), Decimal(0.5)),
            Point(Decimal(0.5), Decimal(-0.5)),
            Point(Decimal(0.5), Decimal(0.5)),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_5_sites_rhombus_in_middle(self):
        """Test when sites form a rhombus area."""
        p1 = Point(Decimal(1), Decimal(-1))
        p2 = Point(Decimal(-1), Decimal(-1))
        p3 = Point(Decimal(1), Decimal(1))
        p4 = Point(Decimal(-1), Decimal(1))
        p5 = Point(Decimal(0), Decimal(0))
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
        expected_vertices = [
            Point(Decimal(0), Decimal(-1)),
            Point(Decimal(-1), Decimal(0)),
            Point(Decimal(1), Decimal(0)),
            Point(Decimal(0), Decimal(1)),
        ]

        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(points)

        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )
