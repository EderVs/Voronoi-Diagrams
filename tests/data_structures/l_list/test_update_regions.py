"""Test update regions."""
# Standard Library
from typing import List, Optional

# Data structures
from voronoi_diagrams.data_structures import LList
from voronoi_diagrams.data_structures.l import LNode
from tests.data_structures.avl_tree.test_insert import check_if_tree_is_balanced

# Models
from voronoi_diagrams.models import (
    Region,
    Site,
    PointBisector,
    Site,
    PointBoundary,
    Region,
)


def create_l_list(region: Region) -> LList:
    """Create an L List."""
    l_list = LList(region)
    return l_list


def validate_l_list_with_expected_list(
    l_list: LList, expected_list: List[Region]
) -> None:
    """Validate l list with expected list."""
    actual_node: Optional[LNode] = l_list.head
    actual_region_index = 0
    while actual_node is not None:
        assert actual_node.value == expected_list[actual_region_index]
        if actual_node.right_neighbor is None:
            break
        actual_node = actual_node.right_neighbor  # type: ignore
        actual_region_index += 1
    assert actual_region_index == len(expected_list) - 1

    while actual_node is not None:
        assert actual_node.value == expected_list[actual_region_index]
        if actual_node.left_neighbor is None:
            break
        actual_node = actual_node.left_neighbor  # type: ignore
        actual_region_index -= 1
    assert actual_region_index == 0


class TestUpdateRegions:
    """Test Update regions."""

    def setup(self) -> None:
        """Set up every region."""
        self.p = Site(0, 0)
        self.r_p = Region(self.p, None, None)
        self.l_list = create_l_list(self.r_p)

    def test_in_l_list_with_one_region(self) -> None:
        """Test with just an l list with just one region in it."""
        q = Site(2, 2)

        bisector = PointBisector((self.p, q))

        boundary_minus = PointBoundary(bisector, False)
        boundary_plus = PointBoundary(bisector, True)

        left_region = Region(self.p, None, boundary_minus)
        center_region = Region(q, boundary_minus, boundary_plus)
        right_region = Region(self.p, boundary_plus, None)
        expected_list = [left_region, center_region, right_region]

        self.l_list.update_regions(left_region, center_region, right_region)

        head = self.l_list.head
        assert head is not None
        assert head.value == left_region

        validate_l_list_with_expected_list(self.l_list, expected_list)
        check_if_tree_is_balanced(self.l_list.t)

    def test_in_l_list_in_middle(self) -> None:
        """Test with just an l list with just one region in it."""
        q = Site(2, 2)
        r = Site(2, 3)

        bisector_pq = PointBisector((self.p, q))
        bisector_qr = PointBisector((q, r))

        boundary_pq_minus = PointBoundary(bisector_pq, False)
        boundary_pq_plus = PointBoundary(bisector_pq, True)
        boundary_qr_minus = PointBoundary(bisector_qr, False)
        boundary_qr_plus = PointBoundary(bisector_qr, True)

        r_p_left = Region(self.p, None, boundary_pq_minus)
        r_q = Region(q, boundary_pq_minus, boundary_pq_plus)
        r_p_right = Region(self.p, boundary_pq_plus, None)

        self.l_list.update_regions(r_p_left, r_q, r_p_right)

        r_q_left = Region(q, boundary_pq_minus, boundary_qr_minus)
        r_r = Region(r, boundary_qr_minus, boundary_qr_plus)
        r_q_right = Region(q, boundary_qr_plus, boundary_pq_plus)

        self.l_list.update_regions(r_q_left, r_r, r_q_right)

        expected_list = [r_p_left, r_q_left, r_r, r_q_right, r_p_right]

        head = self.l_list.head
        assert head is not None
        assert head.value == r_p_left

        validate_l_list_with_expected_list(self.l_list, expected_list)
        check_if_tree_is_balanced(self.l_list.t)

    def test_in_l_list_to_left(self) -> None:
        """Test updating the left part."""
        q = Site(2, 2)
        r = Site(0, 3)

        bisector_pq = PointBisector((self.p, q))
        bisector_pr = PointBisector((self.p, r))

        boundary_pq_minus = PointBoundary(bisector_pq, False)
        boundary_pq_plus = PointBoundary(bisector_pq, True)
        boundary_pr_minus = PointBoundary(bisector_pr, False)
        boundary_pr_plus = PointBoundary(bisector_pr, True)

        r_p_left = Region(self.p, None, boundary_pq_minus)
        r_q = Region(q, boundary_pq_minus, boundary_pq_plus)
        r_p_right = Region(self.p, boundary_pq_plus, None)

        self.l_list.update_regions(r_p_left, r_q, r_p_right)

        r_p_left_left = Region(self.p, None, boundary_pr_minus)
        r_r = Region(r, boundary_pr_minus, boundary_pr_plus)
        r_p_left_right = Region(self.p, boundary_pr_plus, boundary_pq_minus)

        self.l_list.update_regions(r_p_left_left, r_r, r_p_left_right)

        expected_list = [r_p_left_left, r_r, r_p_left_right, r_q, r_p_right]

        head = self.l_list.head
        assert head is not None
        assert head.value == r_p_left_left

        validate_l_list_with_expected_list(self.l_list, expected_list)
        check_if_tree_is_balanced(self.l_list.t)

    def test_in_l_list_to_right(self) -> None:
        """Test updating the right part."""
        q = Site(2, 2)
        r = Site(6, 3)

        bisector_pq = PointBisector((self.p, q))
        bisector_pr = PointBisector((self.p, r))

        boundary_pq_minus = PointBoundary(bisector_pq, False)
        boundary_pq_plus = PointBoundary(bisector_pq, True)
        boundary_pr_minus = PointBoundary(bisector_pr, False)
        boundary_pr_plus = PointBoundary(bisector_pr, True)

        r_p_left = Region(self.p, None, boundary_pq_minus)
        r_q = Region(q, boundary_pq_minus, boundary_pq_plus)
        r_p_right = Region(self.p, boundary_pq_plus, None)

        self.l_list.update_regions(r_p_left, r_q, r_p_right)

        r_p_right_left = Region(self.p, boundary_pq_plus, boundary_pr_minus)
        r_r = Region(r, boundary_pr_minus, boundary_pr_plus)
        r_p_right_right = Region(self.p, boundary_pr_plus, None)

        self.l_list.update_regions(r_p_right_left, r_r, r_p_right_right)

        expected_list = [r_p_left, r_q, r_p_right_left, r_r, r_p_right_right]

        head = self.l_list.head
        assert head is not None
        assert head.value == r_p_left

        validate_l_list_with_expected_list(self.l_list, expected_list)
        check_if_tree_is_balanced(self.l_list.t)
