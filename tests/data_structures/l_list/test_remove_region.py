"""Test remove region."""
# Standard Library
from typing import List, Optional

# Data structures
from voronoi_diagrams.data_structures import LList
from voronoi_diagrams.data_structures.l import LNode

# Models
from voronoi_diagrams.models import (
    Region,
    Site,
    PointBisector,
    Site,
    PointBoundary,
    Region,
)

from tests.data_structures.avl_tree.test_insert import check_if_tree_is_balanced


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
    if len(expected_list) == 0:
        assert actual_region_index == len(expected_list)
    else:
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

    def test_remove_last_region(self) -> None:
        """Test remove the only region in a l list."""
        node = self.l_list.head
        assert node is not None

        self.l_list.remove_region(node, None)
        expected_list: List[Region] = []

        assert self.l_list.head is None

        validate_l_list_with_expected_list(self.l_list, expected_list)
        check_if_tree_is_balanced(self.l_list.t)

    def test_remove_region_in_middle_right(self) -> None:
        """Test with a list with 3 regions to the right."""
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
        r_p_right_right = Region(q, boundary_pr_plus, None)

        (
            r_p_right_left_node,
            r_r_node,
            r_p_right_right_node,
        ) = self.l_list.update_regions(r_p_right_left, r_r, r_p_right_right)

        bisector_qr = PointBisector((q, r))
        boundary_qr_minus = PointBoundary(bisector_qr, False)

        self.l_list.remove_region(r_p_right_left_node, boundary_qr_minus)
        expected_list: List[Region] = [r_p_left, r_q, r_r, r_p_right_right]

        head = self.l_list.head
        assert head is not None

        validate_l_list_with_expected_list(self.l_list, expected_list)
        check_if_tree_is_balanced(self.l_list.t)

    def test_remove_region_in_middle_left(self) -> None:
        """Test with a list with 3 regions to the left."""
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
        r_p_left_right = Region(q, boundary_pr_plus, boundary_pq_minus)

        (
            r_p_left_left_node,
            r_r_node,
            r_p_left_right_node,
        ) = self.l_list.update_regions(r_p_left_left, r_r, r_p_left_right)

        bisector_qr = PointBisector((q, r))
        boundary_qr_plus = PointBoundary(bisector_qr, True)

        self.l_list.remove_region(r_p_left_right_node, boundary_qr_plus)
        expected_list: List[Region] = [r_p_left_left, r_r, r_q, r_p_right]

        head = self.l_list.head
        assert head is not None
        assert head == r_p_left_left_node

        validate_l_list_with_expected_list(self.l_list, expected_list)
        check_if_tree_is_balanced(self.l_list.t)
