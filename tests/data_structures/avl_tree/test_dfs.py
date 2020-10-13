"""AVL Tree DFS Tests."""
from typing import List, Any
from random import shuffle
from voronoi_diagrams.data_structures import AVLTree, IntNode
from .test_insert import create_tree


class TestInorder:
    """DFS Inorder in the AVL Tree."""

    def test_range(self) -> None:
        """Test range."""
        expected_list = [i for i in range(100)]
        random_list = expected_list.copy()
        shuffle(random_list)
        t = create_tree(random_list)
        assert t.dfs_inorder() == expected_list
