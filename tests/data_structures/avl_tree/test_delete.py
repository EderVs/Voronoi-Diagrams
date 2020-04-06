"""AVL Tree Delete Tests."""
from typing import List, Any
from random import shuffle
from voronoi_diagrams.data_structures import AVLTree, IntNode
from utils import (
    create_tree,
    check_if_tree_is_balanced,
    check_if_tree_is_correct,
    remove_many,
)


class TestRemove:
    """Remove in the AVL Tree."""

    def test_root(self) -> None:
        """Test that a root is added when the tree is empty."""
        t = create_tree([1])
        assert t.root is not None
        t.remove(1)
        assert t.root is None

    def test_random(self) -> None:
        """Test with a random sort."""
        expected_list = [i for i in range(100)]
        for _ in range(100):
            random_list = expected_list.copy()
            shuffle(random_list)
            t = create_tree(random_list)
            check_if_tree_is_correct(t)
            check_if_tree_is_balanced(t)

            random_list = expected_list.copy()
            shuffle(random_list)
            remove_many(t, random_list)

    def test_remove_min(self) -> None:
        """Test with a random sort."""
        expected_list = [i for i in range(100)]
        for _ in range(100):
            random_list = expected_list.copy()
            shuffle(random_list)
            t = create_tree(random_list)

            for _ in range(len(expected_list)):
                min_value = t.get_min()
                assert min_value is not None
                t.remove(min_value)
                check_if_tree_is_correct(t)
                check_if_tree_is_balanced(t)
            assert t.root is None

        for _ in range(100):
            random_list = expected_list.copy()
            shuffle(random_list)
            t = create_tree(random_list)

            for _ in range(len(expected_list)):
                min_node = t.get_min_node()
                assert min_node is not None
                t.remove_node(min_node)
                check_if_tree_is_correct(t)
                check_if_tree_is_balanced(t)
            assert t.root is None
