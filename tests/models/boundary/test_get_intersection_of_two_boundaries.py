"""Test get boundaries intersection point."""
# Standard
from typing import List, Any
from random import randint

# Models
from voronoi_diagrams.models import (
    PointBisector,
    Point,
    Site,
    PointBoundary,
    WeightedSite,
    WeightedPointBoundary,
    WeightedPointBisector,
)

# Math
from decimal import Decimal

# General Utils
from general_utils.numbers import are_close


class TestGetIntersectionInPointBoundary:
    """Test get intersections in PointBoundary."""

    def test_two_boundaries(self):
        """Test get intersection with 3 positive fixed sites."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        r = Site(Decimal(2), Decimal(-2))
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(p, r))
        boundary_pq_plus = PointBoundary(bisector_pq, False)
        boundary_pr_minus = PointBoundary(bisector_pr, True)
        intersections = boundary_pr_minus.get_intersections(boundary_pq_plus)
        assert intersections
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(2)
        assert intersection.y == Decimal(0)
        assert intersection_star.x == Decimal(2)
        assert intersection_star.y == Decimal(2)
        intersections2 = boundary_pq_plus.get_intersections(boundary_pr_minus)
        assert intersections2
        assert len(intersections2) == 1
        intersection2 = intersections2[0]
        intersection2, intersection2_star = intersection2
        assert intersection2.x == Decimal(2)
        assert intersection2.y == Decimal(0)
        assert intersection2_star.x == Decimal(2)
        assert intersection2_star.y == Decimal(2)


class TestParallelBisectorsIntersectionPoint:
    """Test that there are no intersections."""

    def test_bisectors_with_slope_0(self):
        """Test when the bisectors are horizontal."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(2), Decimal(2))
        r = Site(Decimal(2), Decimal(-2))
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(q, r))
        boundary_pq_plus = PointBoundary(bisector_pq, False)
        boundary_pr_minus = PointBoundary(bisector_pr, True)
        intersections = boundary_pr_minus.get_intersections(boundary_pq_plus)
        assert not intersections

    def test_bisectors_with_infinity_slope(self):
        """Test when the bisectors are vertical."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(1), Decimal(0))
        r = Site(Decimal(2), Decimal(0))
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(q, r))
        boundary_pq_plus = PointBoundary(bisector_pq, False)
        boundary_pr_minus = PointBoundary(bisector_pr, True)
        intersections = boundary_pr_minus.get_intersections(boundary_pq_plus)
        assert not intersections

    def test_parallel_bisectors(self):
        """Test when the bisectors are diagonals."""
        p = Site(Decimal(0), Decimal(0))
        q = Site(Decimal(1), Decimal(1))
        r = Site(Decimal(2), Decimal(2))
        bisector_pq = PointBisector(sites=(p, q))
        bisector_pr = PointBisector(sites=(q, r))
        boundary_pq_plus = PointBoundary(bisector_pq, False)
        boundary_pr_minus = PointBoundary(bisector_pr, True)
        intersections = boundary_pr_minus.get_intersections(boundary_pq_plus)
        assert not intersections


class TestGetIntersectionInWeightedPointBoundary:
    """Test get intersection in WeightedPointBoundary."""

    def test_two_normal_boundaries(self):
        """Test get intersection with 3 positive fixed sites."""
        p = WeightedSite(Decimal(50), Decimal(20), Decimal(6))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        r = WeightedSite(Decimal(-10), Decimal(30), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "26.071357865127087194423438631929457187652587890625"
        )
        assert intersection.y == Decimal(
            "56.97399440432361217290235799737274646759033203125"
        )
        assert intersection_star.x == Decimal(
            "26.071357865127087194423438631929457187652587890625"
        )
        assert intersection_star.y == Decimal("107.0155222687127964860201311")

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        p = WeightedSite(Decimal(-8), Decimal(30), Decimal(6))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        r = WeightedSite(Decimal(5), Decimal(20), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "142.2824956122580033479607664048671722412109375"
        )
        assert intersection.y == Decimal(
            "237.595493857161244477538275532424449920654296875"
        )
        assert intersection_star.x == Decimal(
            "142.2824956122580033479607664048671722412109375"
        )
        assert intersection_star.y == Decimal("499.8779894694192013325998825")

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "-46.1192303061356625448752311058342456817626953125"
        )
        assert intersection.y == Decimal(
            "-26.1669224285899275628253235481679439544677734375"
        )
        assert intersection_star.x == Decimal(
            "-46.1192303061356625448752311058342456817626953125"
        )
        assert intersection_star.y == Decimal("47.71384726527440049937736671")

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

    def test_concave_to_y_boundary(self):
        """Test get intersection with 3 positive fixed sites."""
        # qr is concave to y.
        p = WeightedSite(Decimal(50), Decimal(25), Decimal(6))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        r = WeightedSite(Decimal(5), Decimal(10), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "-195.64751728601504510152153670787811279296875"
        )
        assert intersection.y == Decimal(
            "737.2008338612932902833563275635242462158203125"
        )
        assert intersection_star.x == Decimal(
            "-195.64751728601504510152153670787811279296875"
        )
        assert intersection_star.y == Decimal("1496.575063910015190799840426")

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        # Both are concave to y.
        p = WeightedSite(Decimal(40), Decimal(10), Decimal(6))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        r = WeightedSite(Decimal(5), Decimal(10), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        p = WeightedSite(Decimal(11.5), Decimal(10.07), Decimal(6))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        r = WeightedSite(Decimal(11.2), Decimal(8), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "11.4773547011539189810491734533570706844329833984375"
        )
        assert intersection.y == Decimal(
            "9.522707454740849897234511445276439189910888671875"
        )
        assert intersection_star.x == Decimal(
            "11.4773547011539189810491734533570706844329833984375"
        )
        assert intersection_star.y == Decimal("16.07046829640067737307526993")

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "1.0997085109018398529912019512266851961612701416015625"
        )
        assert intersection.y == Decimal(
            "16.7276506075346560464822687208652496337890625"
        )
        assert intersection_star.x == Decimal(
            "1.0997085109018398529912019512266851961612701416015625"
        )
        assert intersection_star.y == Decimal("35.07634991840194240564230971")

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        # pq is concave to y.
        p = WeightedSite(Decimal(40), Decimal(10), Decimal(6))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        r = WeightedSite(Decimal(5), Decimal(19), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "38.110951833897416918262024410068988800048828125"
        )
        assert intersection.y == Decimal(
            "68.6352892425572207457662443630397319793701171875"
        )
        assert intersection_star.x == Decimal(
            "38.110951833897416918262024410068988800048828125"
        )
        assert intersection_star.y == Decimal("133.3010002459383107400476452")

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

    def test_boundary_stopped(self):
        """Test get intersection with 3 positive fixed sites."""
        # qr is stopped.
        # pq is normal.
        p = WeightedSite(Decimal(0), Decimal(20), Decimal(6))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        r = WeightedSite(Decimal(5), Decimal(13), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "10.17385250288240428062636055983603000640869140625"
        )
        assert intersection.y == Decimal(
            "23.5941894450834155350094079039990901947021484375"
        )
        assert intersection_star.x == Decimal(
            "10.17385250288240428062636055983603000640869140625"
        )
        assert intersection_star.y == Decimal("40.38425304626468173189701465")

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        # Viceversa
        intersections = boundary_pq_plus.get_intersections(boundary_qr_plus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert are_close(
            intersection.x,
            Decimal("10.17385250288240428062636055983603000640869140625"),
            Decimal("0.00000001"),
        )
        assert are_close(
            intersection.y,
            Decimal("23.5941894450834155350094079039990901947021484375"),
            Decimal("0.00000001"),
        )
        assert are_close(
            intersection_star.x,
            Decimal("10.17385250288240428062636055983603000640869140625"),
            Decimal("0.00000001"),
        )
        assert are_close(
            intersection_star.y,
            Decimal("40.38425304626468173189701465"),
            Decimal("0.00000001"),
        )

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        # qr is stopped.
        # pq is stopped.
        p = WeightedSite(Decimal(11), Decimal(14), Decimal(6))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        r = WeightedSite(Decimal(5), Decimal(13), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert are_close(
            intersection.x,
            Decimal("8.9482758620689590856045469990931451320648193359375"),
            Decimal("0.00000001"),
        )
        assert are_close(
            intersection.y,
            Decimal("11.5251044932079214078157747280783951282501220703125"),
            Decimal("0.00000001"),
        )
        assert are_close(
            intersection_star.x,
            Decimal("8.9482758620689590856045469990931451320648193359375"),
            Decimal("0.00000001"),
        )
        assert are_close(
            intersection_star.y,
            Decimal("20.73986415882965699538744224"),
            Decimal("0.00000001"),
        )

        # Viceversa
        intersections = boundary_pq_minus.get_intersections(boundary_qr_plus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert are_close(
            intersection.x,
            Decimal("8.9482758620689590856045469990931451320648193359375"),
            Decimal("0.00000001"),
        )
        assert are_close(
            intersection.y,
            Decimal("11.5251044932079214078157747280783951282501220703125"),
            Decimal("0.00000001"),
        )
        assert are_close(
            intersection_star.x,
            Decimal("8.9482758620689590856045469990931451320648193359375"),
            Decimal("0.00000001"),
        )
        assert are_close(
            intersection_star.y,
            Decimal("20.73986415882965699538744224"),
            Decimal("0.00000001"),
        )

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        p = WeightedSite(Decimal(27), Decimal(14), Decimal(6))
        q = WeightedSite(Decimal(16), Decimal(10), Decimal(2))
        r = WeightedSite(Decimal(5), Decimal(13), Decimal(5))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

    def test_sites_without_weight(self):
        """Test get intersection with 3 positive fixed sites."""
        p = WeightedSite(Decimal(40), Decimal(2), Decimal(0))
        q = WeightedSite(Decimal(38), Decimal(38), Decimal(1))
        r = WeightedSite(Decimal(20), Decimal(0), Decimal(0))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "28.102044708167113640229217708110809326171875"
        )
        assert intersection.y == Decimal(
            "19.979552926265565560015602386556565761566162109375"
        )
        assert intersection_star.x == Decimal(
            "28.102044708167113640229217708110809326171875"
        )
        assert intersection_star.y == Decimal("41.53936887136552600734798861")

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        p = WeightedSite(Decimal(40), Decimal(2), Decimal(0))
        q = WeightedSite(Decimal(38), Decimal(38), Decimal(0))
        r = WeightedSite(Decimal(20), Decimal(0), Decimal(0))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "28.160220994475139377755112946033477783203125"
        )
        assert intersection.y == Decimal(
            "19.397790055248616880589906941168010234832763671875"
        )
        assert intersection_star.x == Decimal(
            "28.160220994475139377755112946033477783203125"
        )
        assert intersection_star.y == Decimal("40.44211151511457928961840373")

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        p = WeightedSite(Decimal(40), Decimal(2), Decimal(1))
        q = WeightedSite(Decimal(38), Decimal(38), Decimal(0))
        r = WeightedSite(Decimal(20), Decimal(0), Decimal(0))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "29.237523029892987125322179053910076618194580078125"
        )
        assert intersection.y == Decimal(
            "18.887489091103322635945005458779633045196533203125"
        )
        assert intersection_star.x == Decimal(
            "29.237523029892987125322179053910076618194580078125"
        )
        assert intersection_star.y == Decimal("39.91292787117044096096486319")

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        p = WeightedSite(Decimal(40), Decimal(2), Decimal(1))
        q = WeightedSite(Decimal(38), Decimal(38), Decimal(0))
        r = WeightedSite(Decimal(20), Decimal(0), Decimal(1))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "28.218323696394005395404747105203568935394287109375"
        )
        assert intersection.y == Decimal(
            "18.81676302800800471004549763165414333343505859375"
        )
        assert intersection_star.x == Decimal(
            "28.218323696394005395404747105203568935394287109375"
        )
        assert intersection_star.y == Decimal("40.34994142860942754088607165")

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

    def test_horizonal_bisector(self):
        """Test get intersection with 3 positive fixed sites."""
        p = WeightedSite(Decimal(38), Decimal(2), Decimal(0))
        q = WeightedSite(Decimal(38), Decimal(38), Decimal(0))
        r = WeightedSite(Decimal(20), Decimal(0), Decimal(1))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "25.705669523894808747854767716489732265472412109375"
        )
        assert intersection.y == Decimal(
            "20.000000000000046185277824406512081623077392578125"
        )
        assert intersection_star.x == Decimal(
            "25.705669523894808747854767716489732265472412109375"
        )
        assert intersection_star.y == Decimal("41.79794856989274689184053680")

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        p = WeightedSite(Decimal(38), Decimal(2), Decimal(0))
        q = WeightedSite(Decimal(38), Decimal(38), Decimal(0))
        r = WeightedSite(Decimal(20), Decimal(0), Decimal(0))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal(
            "26.888888888888889283634853200055658817291259765625"
        )
        assert intersection.y == Decimal("20")
        assert intersection_star.x == Decimal(
            "26.888888888888889283634853200055658817291259765625"
        )
        assert intersection_star.y == Decimal("41.15317446917735752620224829")

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

    def test_vertical_bisector(self):
        """Test get intersection with 3 positive fixed sites."""
        p = WeightedSite(Decimal(38), Decimal(2), Decimal(0))
        q = WeightedSite(Decimal(20), Decimal(2), Decimal(0))
        r = WeightedSite(Decimal(20), Decimal(0), Decimal(0))
        bisector_pq = WeightedPointBisector(sites=(p, q))
        bisector_qr = WeightedPointBisector(sites=(q, r))
        boundary_pq_plus = WeightedPointBoundary(bisector_pq, True)
        boundary_pq_minus = WeightedPointBoundary(bisector_pq, False)
        boundary_qr_plus = WeightedPointBoundary(bisector_qr, True)
        boundary_qr_minus = WeightedPointBoundary(bisector_qr, False)
        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal("29")
        assert intersection.y == Decimal("1")
        assert intersection_star.x == Decimal("29")
        assert intersection_star.y == Decimal("10.05538513813741662657380817")

        intersections = boundary_qr_plus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 1
        intersection = intersections[0]
        intersection, intersection_star = intersection
        assert intersection.x == Decimal("29")
        assert intersection.y == Decimal("1")
        assert intersection_star.x == Decimal("29")
        assert intersection_star.y == Decimal("10.05538513813741662657380817")

        intersections = boundary_qr_plus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_minus)
        assert len(intersections) == 0

        intersections = boundary_qr_minus.get_intersections(boundary_pq_plus)
        assert len(intersections) == 0
