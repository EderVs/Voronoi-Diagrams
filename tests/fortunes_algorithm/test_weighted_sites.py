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

    def test_3_sites(self):
        """Test 3 sites."""
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

        p1 = Point(Decimal("36.7"), Decimal("1.6"))
        p1_w = Decimal(2)
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal(5)
        p3 = Point(Decimal("13.4"), Decimal("3.4"))
        p3_w = Decimal(2)
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
                Decimal("23.195022965036205420119586051441729068756103515625"),
                Decimal("-21.511647174809116478400028427131474018096923828125"),
            ),
            Point(
                Decimal("26.469144622760826024432390113361179828643798828125"),
                Decimal("20.870038727961539137822910561226308345794677734375"),
            ),
        ]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_3_sites_no_vertices(self):
        """Test 3 sites.

        There are no intersections (vertices) in this test.
        """
        p1 = Point(Decimal(38), Decimal(2))
        p1_w = Decimal(1)
        p2 = Point(Decimal(34), Decimal(39))
        p2_w = Decimal(2)
        p3 = Point(Decimal(36), Decimal(-10))
        p3_w = Decimal(5)
        site_p1 = WeightedSite(p1.x, p1.y, p1_w)
        site_p2 = WeightedSite(p2.x, p2.y, p2_w)
        site_p3 = WeightedSite(p3.x, p3.y, p3_w)
        points_and_weights = ((p1, p1_w), (p2, p2_w), (p3, p3_w))
        bisector_p1_p2 = WeightedPointBisector((site_p1, site_p2))
        bisector_p1_p3 = WeightedPointBisector((site_p1, site_p3))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        expected_bisectors = [bisector_p1_p2, bisector_p1_p3]
        expected_vertices = []
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

        p1 = Point(Decimal(38), Decimal(2))
        p1_w = Decimal(1)
        p2 = Point(Decimal(38), Decimal(39))
        p2_w = Decimal(2)
        p3 = Point(Decimal(38), Decimal(-10))
        p3_w = Decimal(5)
        site_p1 = WeightedSite(p1.x, p1.y, p1_w)
        site_p2 = WeightedSite(p2.x, p2.y, p2_w)
        site_p3 = WeightedSite(p3.x, p3.y, p3_w)
        points_and_weights = ((p1, p1_w), (p2, p2_w), (p3, p3_w))
        bisector_p1_p2 = WeightedPointBisector((site_p1, site_p2))
        bisector_p1_p3 = WeightedPointBisector((site_p1, site_p3))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        expected_bisectors = [bisector_p1_p2, bisector_p1_p3]
        expected_vertices = []
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_3_sites_without_weights(self):
        """Test 3 sites.

        There are no intersections (vertices) in this test.
        """
        p1 = Point(Decimal(38), Decimal(2))
        p1_w = Decimal(0)
        p2 = Point(Decimal(40), Decimal(38))
        p2_w = Decimal(0)
        p3 = Point(Decimal(20), Decimal(0))
        p3_w = Decimal(0)
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
                Decimal("26.81366459627329135173567919991910457611083984375"),
                Decimal("20.67701863354037783437888720072805881500244140625"),
            )
        ]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_3_sites_without_weights_vertical(self):
        """Test 3 sites.

        There are no intersections (vertices) in this test.
        """
        p1 = Point(Decimal(38), Decimal(2))
        p1_w = Decimal(0)
        p2 = Point(Decimal(40), Decimal(0))
        p2_w = Decimal(0)
        p3 = Point(Decimal(20), Decimal(0))
        p3_w = Decimal(0)
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
        expected_vertices = [Point(Decimal("30"), Decimal("-8"),)]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_3_sites_without_weights_vertical_and_horizontal(self):
        """Test 3 sites.

        There are no intersections (vertices) in this test.
        """
        p1 = Point(Decimal(40), Decimal(5))
        p1_w = Decimal(0)
        p2 = Point(Decimal(40), Decimal(0))
        p2_w = Decimal(0)
        p3 = Point(Decimal(20), Decimal(0))
        p3_w = Decimal(0)
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
        expected_vertices = [Point(Decimal("30"), Decimal("2.5"),)]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_4_sites(self):
        """Test 4 sites."""
        p1 = Point(Decimal("40"), Decimal("5"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("36.5"), Decimal("-2.4"))
        p2_w = Decimal("4")
        p3 = Point(Decimal("23.75"), Decimal("2.25"))
        p3_w = Decimal("5")
        p4 = Point(Decimal("19.6"), Decimal("25.6"))
        p4_w = Decimal("2")
        site_p1 = WeightedSite(p1.x, p1.y, p1_w)
        site_p2 = WeightedSite(p2.x, p2.y, p2_w)
        site_p3 = WeightedSite(p3.x, p3.y, p3_w)
        site_p4 = WeightedSite(p4.x, p4.y, p4_w)
        points_and_weights = ((p1, p1_w), (p2, p2_w), (p3, p3_w), (p4, p4_w))
        bisector_p1_p2 = WeightedPointBisector((site_p1, site_p2))
        bisector_p1_p3 = WeightedPointBisector((site_p1, site_p3))
        bisector_p1_p4 = WeightedPointBisector((site_p1, site_p4))
        bisector_p2_p3 = WeightedPointBisector((site_p2, site_p3))
        bisector_p3_p4 = WeightedPointBisector((site_p3, site_p4))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p1_p4,
            bisector_p2_p3,
            bisector_p3_p4,
        ]
        expected_vertices = [
            Point(
                Decimal("30.522802422504742736464322661049664020538330078125"),
                Decimal("2.581536125410982318584274253225885331630706787109375"),
            ),
            Point(
                Decimal("27.786748740244686217693015350960195064544677734375"),
                Decimal("13.3062948690129889683930741739459335803985595703125"),
            ),
        ]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

        p1 = Point(Decimal("40"), Decimal("5"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("36.5"), Decimal("-2.4"))
        p2_w = Decimal("4")
        p3 = Point(Decimal("23.75"), Decimal("2.25"))
        p3_w = Decimal("5")
        p4 = Point(Decimal("14"), Decimal("4"))
        p4_w = Decimal("2")
        site_p1 = WeightedSite(p1.x, p1.y, p1_w)
        site_p2 = WeightedSite(p2.x, p2.y, p2_w)
        site_p3 = WeightedSite(p3.x, p3.y, p3_w)
        site_p4 = WeightedSite(p4.x, p4.y, p4_w)
        points_and_weights = ((p1, p1_w), (p2, p2_w), (p3, p3_w), (p4, p4_w))
        bisector_p1_p2 = WeightedPointBisector((site_p1, site_p2))
        bisector_p1_p3 = WeightedPointBisector((site_p1, site_p3))
        bisector_p1_p4 = WeightedPointBisector((site_p1, site_p4))
        bisector_p2_p3 = WeightedPointBisector((site_p2, site_p3))
        bisector_p2_p4 = WeightedPointBisector((site_p2, site_p4))
        bisector_p3_p4 = WeightedPointBisector((site_p3, site_p4))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
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
                Decimal("30.522802422504742736464322661049664020538330078125"),
                Decimal("2.581536125410982318584274253225885331630706787109375"),
            ),
            Point(
                Decimal("21.83673459217973089607767178677022457122802734375"),
                Decimal("-18.2628496544823377689681365154683589935302734375"),
            ),
            Point(
                Decimal("26.51369782967488930580657324753701686859130859375"),
                Decimal("17.1438564285112278184897149913012981414794921875"),
            ),
        ]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

        p1 = Point(Decimal("36.7"), Decimal("1.6"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal("5")
        p3 = Point(Decimal("13.4"), Decimal("3.4"))
        p3_w = Decimal("2")
        p4 = Point(Decimal("52.6"), Decimal("27.4"))
        p4_w = Decimal("4")
        site_p1 = WeightedSite(p1.x, p1.y, p1_w)
        site_p2 = WeightedSite(p2.x, p2.y, p2_w)
        site_p3 = WeightedSite(p3.x, p3.y, p3_w)
        site_p4 = WeightedSite(p4.x, p4.y, p4_w)
        points_and_weights = ((p1, p1_w), (p2, p2_w), (p3, p3_w), (p4, p4_w))
        bisector_p1_p2 = WeightedPointBisector((site_p1, site_p2))
        bisector_p1_p3 = WeightedPointBisector((site_p1, site_p3))
        bisector_p1_p4 = WeightedPointBisector((site_p1, site_p4))
        bisector_p2_p3 = WeightedPointBisector((site_p2, site_p3))
        bisector_p3_p4 = WeightedPointBisector((site_p3, site_p4))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p1_p4,
            bisector_p2_p3,
            bisector_p3_p4,
        ]
        expected_vertices = [
            Point(
                Decimal("23.195022965036205420119586051441729068756103515625"),
                Decimal("-21.511647174809116478400028427131474018096923828125"),
            ),
            Point(
                Decimal("26.469144622760826024432390113361179828643798828125"),
                Decimal("20.870038727961539137822910561226308345794677734375"),
            ),
            Point(
                Decimal("26.977832844500397868614527396857738494873046875"),
                Decimal("27.45472515381070621742765069939196109771728515625"),
            ),
        ]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

        p1 = Point(Decimal("36.7"), Decimal("1.6"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal("5")
        p3 = Point(Decimal("13.4"), Decimal("3.4"))
        p3_w = Decimal("2")
        p4 = Point(Decimal("32"), Decimal("2.14"))
        p4_w = Decimal("4")
        site_p1 = WeightedSite(p1.x, p1.y, p1_w)
        site_p2 = WeightedSite(p2.x, p2.y, p2_w)
        site_p3 = WeightedSite(p3.x, p3.y, p3_w)
        site_p4 = WeightedSite(p4.x, p4.y, p4_w)
        points_and_weights = ((p1, p1_w), (p2, p2_w), (p3, p3_w), (p4, p4_w))
        bisector_p1_p2 = WeightedPointBisector((site_p1, site_p2))
        bisector_p1_p3 = WeightedPointBisector((site_p1, site_p3))
        bisector_p1_p4 = WeightedPointBisector((site_p1, site_p4))
        bisector_p2_p3 = WeightedPointBisector((site_p2, site_p3))
        bisector_p2_p4 = WeightedPointBisector((site_p2, site_p4))
        bisector_p3_p4 = WeightedPointBisector((site_p3, site_p4))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
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
                Decimal("23.195022965036205420119586051441729068756103515625"),
                Decimal("-21.511647174809116478400028427131474018096923828125"),
            ),
            Point(
                Decimal("26.7498329695602734545900602824985980987548828125"),
                Decimal("24.50339343927415569623917690478265285491943359375"),
            ),
            Point(
                Decimal("25.930130575231569167726775049231946468353271484375"),
                Decimal("19.569718372035143971743309521116316318511962890625"),
            ),
            Point(
                Decimal("25.913143883533347633374432916752994060516357421875"),
                Decimal("-11.7365557052741333876610951847396790981292724609375"),
            ),
        ]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_5_sites(self):
        """Test 5 sites."""
        p1 = Point(Decimal("36.7"), Decimal("1.6"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal("5")
        p3 = Point(Decimal("13.4"), Decimal("3.4"))
        p3_w = Decimal("2")
        p4 = Point(Decimal("32"), Decimal("2.14"))
        p4_w = Decimal("4")
        p5 = Point(Decimal("28"), Decimal("10"))
        p5_w = Decimal("1")
        site_p1 = WeightedSite(p1.x, p1.y, p1_w)
        site_p2 = WeightedSite(p2.x, p2.y, p2_w)
        site_p3 = WeightedSite(p3.x, p3.y, p3_w)
        site_p4 = WeightedSite(p4.x, p4.y, p4_w)
        site_p5 = WeightedSite(p5.x, p5.y, p5_w)
        points_and_weights = (
            (p1, p1_w),
            (p2, p2_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        bisector_p1_p2 = WeightedPointBisector((site_p1, site_p2))
        bisector_p1_p3 = WeightedPointBisector((site_p1, site_p3))
        bisector_p1_p4 = WeightedPointBisector((site_p1, site_p4))
        bisector_p1_p5 = WeightedPointBisector((site_p1, site_p5))
        bisector_p2_p3 = WeightedPointBisector((site_p2, site_p3))
        bisector_p2_p4 = WeightedPointBisector((site_p2, site_p4))
        bisector_p2_p5 = WeightedPointBisector((site_p2, site_p5))
        bisector_p3_p5 = WeightedPointBisector((site_p3, site_p5))
        bisector_p4_p5 = WeightedPointBisector((site_p4, site_p5))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        expected_bisectors = [
            bisector_p1_p2,
            bisector_p1_p3,
            bisector_p1_p4,
            bisector_p1_p5,
            bisector_p2_p3,
            bisector_p2_p4,
            bisector_p2_p5,
            bisector_p3_p5,
            bisector_p4_p5,
        ]
        expected_vertices = [
            Point(
                Decimal("23.195022965036205420119586051441729068756103515625"),
                Decimal("-21.511647174809116478400028427131474018096923828125"),
            ),
            Point(
                Decimal("25.913143883533347633374432916752994060516357421875"),
                Decimal("-11.7365557052741333876610951847396790981292724609375"),
            ),
            Point(
                Decimal("27.37706884756726566365614417009055614471435546875"),
                Decimal("2.395486209641373154255461486172862350940704345703125"),
            ),
            Point(
                Decimal("32.8412086290852442971299751661717891693115234375"),
                Decimal("5.588553097025879878856358118355274200439453125"),
            ),
            Point(
                Decimal("20.6432720530798832214713911525905132293701171875"),
                Decimal("5.6026444142095694900262969895265996456146240234375"),
            ),
        ]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

        p1 = Point(Decimal("36.7"), Decimal("1.6"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal("5")
        p3 = Point(Decimal("13.4"), Decimal("3.4"))
        p3_w = Decimal("2")
        p4 = Point(Decimal("32"), Decimal("2.14"))
        p4_w = Decimal("4")
        p5 = Point(Decimal("27"), Decimal("-13.5"))
        p5_w = Decimal("1")
        site_p1 = WeightedSite(p1.x, p1.y, p1_w)
        site_p2 = WeightedSite(p2.x, p2.y, p2_w)
        site_p3 = WeightedSite(p3.x, p3.y, p3_w)
        site_p4 = WeightedSite(p4.x, p4.y, p4_w)
        site_p5 = WeightedSite(p5.x, p5.y, p5_w)
        points_and_weights = (
            (p1, p1_w),
            (p2, p2_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        bisector_p1_p3 = WeightedPointBisector((site_p1, site_p3))
        bisector_p1_p4 = WeightedPointBisector((site_p1, site_p4))
        bisector_p1_p5 = WeightedPointBisector((site_p1, site_p5))
        bisector_p2_p3 = WeightedPointBisector((site_p2, site_p3))
        bisector_p2_p4 = WeightedPointBisector((site_p2, site_p4))
        bisector_p2_p5 = WeightedPointBisector((site_p2, site_p5))
        bisector_p3_p4 = WeightedPointBisector((site_p3, site_p4))
        bisector_p3_p5 = WeightedPointBisector((site_p3, site_p5))
        bisector_p4_p5 = WeightedPointBisector((site_p4, site_p5))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        expected_bisectors = [
            bisector_p1_p3,
            bisector_p1_p4,
            bisector_p1_p5,
            bisector_p2_p3,
            bisector_p2_p4,
            bisector_p2_p5,
            bisector_p3_p4,
            bisector_p3_p5,
            bisector_p4_p5,
        ]
        expected_vertices = [
            Point(
                Decimal("30.34729940447785878632203093729913234710693359375"),
                Decimal("-4.37406323830063126223421932081691920757293701171875"),
            ),
            Point(
                Decimal("20.354186410998604372935005812905728816986083984375"),
                Decimal("-4.28314108153177297566571724019013345241546630859375"),
            ),
            Point(
                Decimal("26.9768707113081092074935440905392169952392578125"),
                Decimal("-3.181920552671356983154282715986482799053192138671875"),
            ),
            Point(
                Decimal("25.930130575231569167726775049231946468353271484375"),
                Decimal("19.569718372035143971743309521116316318511962890625"),
            ),
            Point(
                Decimal("26.7498329695602734545900602824985980987548828125"),
                Decimal("24.50339343927415569623917690478265285491943359375"),
            ),
        ]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

        p1 = Point(Decimal("40.1"), Decimal("3"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal("5")
        p3 = Point(Decimal("16.2"), Decimal("3"))
        p3_w = Decimal("2")
        p4 = Point(Decimal("32"), Decimal("4"))
        p4_w = Decimal("4")
        p5 = Point(Decimal("19.21"), Decimal("1.59"))
        p5_w = Decimal("1")
        site_p1 = WeightedSite(p1.x, p1.y, p1_w)
        site_p2 = WeightedSite(p2.x, p2.y, p2_w)
        site_p3 = WeightedSite(p3.x, p3.y, p3_w)
        site_p4 = WeightedSite(p4.x, p4.y, p4_w)
        site_p5 = WeightedSite(p5.x, p5.y, p5_w)
        points_and_weights = (
            (p1, p1_w),
            (p2, p2_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        bisector_p1_p3 = WeightedPointBisector((site_p1, site_p3))
        bisector_p1_p4 = WeightedPointBisector((site_p1, site_p4))
        bisector_p1_p5 = WeightedPointBisector((site_p1, site_p5))
        bisector_p2_p4 = WeightedPointBisector((site_p2, site_p4))
        bisector_p2_p5 = WeightedPointBisector((site_p2, site_p5))
        bisector_p3_p5 = WeightedPointBisector((site_p3, site_p5))
        bisector_p4_p5 = WeightedPointBisector((site_p4, site_p5))
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        expected_bisectors = [
            bisector_p1_p3,
            bisector_p1_p4,
            bisector_p1_p5,
            bisector_p2_p4,
            bisector_p2_p5,
            bisector_p3_p5,
            bisector_p4_p5,
        ]
        expected_vertices = [
            Point(
                Decimal("31.13272934807425684766712947748601436614990234375"),
                Decimal("-8.7569999351260232600679955794475972652435302734375"),
            ),
            Point(
                Decimal("27.95864696372947122426921851001679897308349609375"),
                Decimal("-0.395718931677663920964960198034532368183135986328125"),
            ),
            Point(
                Decimal("26.7100260252399692717517609708011150360107421875"),
                Decimal("5.7235016993763085935142953530885279178619384765625"),
            ),
            Point(
                Decimal("28.497320292656983298229533829726278781890869140625"),
                Decimal("63.47058450654454730965881026349961757659912109375"),
            ),
            Point(
                Decimal("28.149999999995035437905244180001318454742431640625"),
                Decimal("80.70465905304178022561245597898960113525390625"),
            ),
        ]
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

    def test_site_in_site(self):
        """Test site inside another site."""
        p1 = Point(Decimal("36.7"), Decimal("1.6"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal("5")
        p3 = Point(Decimal("13.4"), Decimal("3.4"))
        p3_w = Decimal("2")
        p4 = Point(Decimal("32"), Decimal("2.14"))
        p4_w = Decimal("4")
        p5 = Point(Decimal("21"), Decimal("2"))
        p5_w = Decimal("1")
        points_and_weights = (
            (p1, p1_w),
            (p2, p2_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        # Expected voronoi diagram.
        points_and_weights = (
            (p1, p1_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        expected_voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )

        expected_bisectors = expected_voronoi_diagram.bisectors_list
        expected_vertices = expected_voronoi_diagram.vertices_list
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

        p1 = Point(Decimal("36.7"), Decimal("1.6"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal("5")
        p3 = Point(Decimal("13.4"), Decimal("3.4"))
        p3_w = Decimal("2")
        p4 = Point(Decimal("32"), Decimal("4"))
        p4_w = Decimal("4")
        p5 = Point(Decimal("21"), Decimal("2"))
        p5_w = Decimal("1")
        points_and_weights = (
            (p1, p1_w),
            (p2, p2_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        # Expected voronoi diagram.
        points_and_weights = (
            (p1, p1_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        expected_voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )

        expected_bisectors = expected_voronoi_diagram.bisectors_list
        expected_vertices = expected_voronoi_diagram.vertices_list
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

        p1 = Point(Decimal("39.48"), Decimal("7.6"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal("5")
        p3 = Point(Decimal("15.83"), Decimal("6.7"))
        p3_w = Decimal("2")
        p4 = Point(Decimal("32"), Decimal("4"))
        p4_w = Decimal("4")
        p5 = Point(Decimal("21"), Decimal("2"))
        p5_w = Decimal("1")
        points_and_weights = (
            (p1, p1_w),
            (p2, p2_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        # Expected voronoi diagram.
        points_and_weights = (
            (p1, p1_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        expected_voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )

        expected_bisectors = expected_voronoi_diagram.bisectors_list
        expected_vertices = expected_voronoi_diagram.vertices_list
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

        p1 = Point(Decimal("28.36"), Decimal("6.25"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal("5")
        p3 = Point(Decimal("20.27"), Decimal("4.3"))
        p3_w = Decimal("2")
        p4 = Point(Decimal("26.2"), Decimal("5.27"))
        p4_w = Decimal("4")
        p5 = Point(Decimal("21"), Decimal("2"))
        p5_w = Decimal("1")
        points_and_weights = (
            (p1, p1_w),
            (p2, p2_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        # Expected voronoi diagram.
        points_and_weights = (
            (p1, p1_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        expected_voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )

        expected_bisectors = expected_voronoi_diagram.bisectors_list
        expected_vertices = expected_voronoi_diagram.vertices_list
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )

        p1 = Point(Decimal("28.36"), Decimal("6.25"))
        p1_w = Decimal("2")
        p2 = Point(Decimal("23.75"), Decimal("2.25"))
        p2_w = Decimal("50")
        p3 = Point(Decimal("20.27"), Decimal("4.3"))
        p3_w = Decimal("2")
        p4 = Point(Decimal("26.2"), Decimal("5.27"))
        p4_w = Decimal("4")
        p5 = Point(Decimal("21"), Decimal("2"))
        p5_w = Decimal("1")
        points_and_weights = (
            (p1, p1_w),
            (p2, p2_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )
        # Expected voronoi diagram.
        points_and_weights = (
            (p1, p1_w),
            (p3, p3_w),
            (p4, p4_w),
            (p5, p5_w),
        )
        expected_voronoi_diagram = FortunesAlgorithm.calculate_aw_voronoi_diagram(
            points_and_weights
        )

        expected_bisectors = expected_voronoi_diagram.bisectors_list
        expected_vertices = expected_voronoi_diagram.vertices_list
        self._check_bisectors_and_vertex(
            voronoi_diagram, expected_bisectors, expected_vertices
        )


TestWeightedSites().test_5_sites()
