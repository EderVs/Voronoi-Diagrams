"""Test update neighborgs."""
# Data structures
from voronoi_diagrams.data_structures import LList
from voronoi_diagrams.data_structures.models import Region, Site
from voronoi_diagrams.data_structures.l import LNode


def create_l_list(region: Region) -> LList:
    """Create an L List."""
    l_list = LList(region)
    return l_list


class TestUpdateNeighborgs:
    """Test Update neighborgs."""

    def setup(self):
        """Set up every region."""
        p = Site(0, 0)
        r_p = Region(p)
        self.l_list = create_l_list(r_p)

    def test_in_l_list_with_one_region_to_the_right(self):
        """Test with just an l list with just one region in it."""
        q = Site(2, 2)
        r_q = Site(2, 2)
        r_q_node = LNode(r_q)
        ex_head = self.l_list.head
        self.l_list.update_neighbors(self.l_list.head, r_q_node)
        assert self.l_list.head == ex_head
        assert ex_head.left_neighbor is None
        assert ex_head.right_neighbor is not None
        assert ex_head.right_neighbor == r_q_node
        assert r_q_node.left_neighbor is not None
        assert r_q_node.left_neighbor == ex_head

    def test_in_l_list_with_one_region_to_the_left(self):
        """Test with just an l list with just one region in it."""
        q = Site(2, 2)
        r_q = Site(2, 2)
        r_q_node = LNode(r_q)
        ex_head = self.l_list.head
        self.l_list.update_neighbors(r_q_node, self.l_list.head)
        assert self.l_list.head == r_q_node
        assert r_q_node.left_neighbor is None
        assert r_q_node.right_neighbor is not None
        assert r_q_node.right_neighbor == ex_head
        assert ex_head.left_neighbor is not None
        assert ex_head.left_neighbor == r_q_node
        assert ex_head.right_neighbor is None

    def test_in_the_middle(self):
        """Test with just an l list with just one region in it."""
        q = Site(2, 2)
        r_q = Site(2, 2)
        r_q_node = LNode(r_q)
        r = Site(2, 3)
        r_r = Site(2, 3)
        r_r_node = LNode(r_r)
        ex_head = self.l_list.head
        self.l_list.update_neighbors(r_q_node, ex_head)
        self.l_list.update_neighbors(r_q_node, r_r_node)
        self.l_list.update_neighbors(r_r_node, ex_head)
        assert self.l_list.head == r_q_node
        assert r_q_node.left_neighbor is None
        assert r_q_node.right_neighbor is not None
        assert r_q_node.right_neighbor == r_r_node
        assert r_r_node.left_neighbor is not None
        assert r_r_node.left_neighbor == r_q_node
        assert r_r_node.right_neighbor is not None
        assert r_r_node.right_neighbor == ex_head
        assert ex_head.left_neighbor is not None
        assert ex_head.left_neighbor == r_r_node
        assert ex_head.right_neighbor is None

    def test_none_cases(self):
        """Test with just an l list with just one region in it."""
        ex_head = self.l_list.head

        self.l_list.update_neighbors(None, ex_head)
        assert self.l_list.head == ex_head
        assert ex_head.left_neighbor is None

        self.l_list.update_neighbors(ex_head, None)
        assert self.l_list.head == ex_head
        assert ex_head.right_neighbor is None

        q = Site(2, 2)
        r_q = Site(2, 2)
        r_q_node = LNode(r_q)

        self.l_list.update_neighbors(ex_head, r_q_node)
        self.l_list.update_neighbors(None, r_q_node)
        assert self.l_list.head == r_q_node
        assert r_q_node.left_neighbor is None

        self.l_list.update_neighbors(ex_head, r_q_node)
        self.l_list.update_neighbors(r_q_node, None)
        assert self.l_list.head == ex_head
        assert r_q_node.right_neighbor is None

        self.l_list.update_neighbors(ex_head, r_q_node)
        self.l_list.update_neighbors(ex_head, None)
        assert self.l_list.head == ex_head
        assert ex_head.right_neighbor is None
