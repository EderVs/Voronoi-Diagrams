"""AVL Tree Insert Tests."""
from typing import List, Any
from voronoi_diagrams.data_structures import AVLTree, IntNode


def create_tree(to_insert: List[int]) -> AVLTree:
    """Create a tree."""
    t = AVLTree(node_class=IntNode)
    for number in to_insert:
        t.insert(number)
    return t


def check_if_tree_is_balanced(t: AVLTree) -> None:
    """Check that the tree sent has all their factors correct.

    Contains assertions.
    """
    queue: List[Any] = list()
    queue.append(t.root)
    while len(queue) > 0:
        node = queue.pop(0)
        assert abs(node.factor) <= 1
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)


class TestInsert:
    """Insert in the AVL Tree."""

    def test_root(self) -> None:
        """Test that a root is added when the tree is empty."""
        t = create_tree([])
        assert t.root is None
        t.insert(1)
        assert t.root is not None and t.root.value == 1

    def test_case_1(self) -> None:
        """Test we have a turn left."""
        t = create_tree([1, 2, 3])
        check_if_tree_is_balanced(t)
        # Root is changed.
        assert t.root is not None and t.root.value == 2
        assert t.root.left is not None and t.root.left.value == 1
        assert t.root.right is not None and t.root.right.value == 3
        # Root is not changed.
        t.insert_many([4, 5])
        check_if_tree_is_balanced(t)
        assert t.root is not None and t.root.value == 2
        assert t.root.right is not None and t.root.right.value == 4

    def test_case_2(self) -> None:
        """Test we have a turn left."""
        t = create_tree([5, 4, 3])
        check_if_tree_is_balanced(t)
        # Root is changed.
        assert t.root is not None and t.root.value == 4
        assert t.root.left is not None and t.root.left.value == 3
        assert t.root.right is not None and t.root.right.value == 5
        # Root is not changed.
        t.insert_many([2, 1])
        check_if_tree_is_balanced(t)
        assert t.root is not None and t.root.value == 4
        assert t.root.left is not None and t.root.left.value == 2

    def test_case_3(self) -> None:
        """Test we have a turn left-right."""
        t = create_tree([2, 9, 5])
        check_if_tree_is_balanced(t)
        # Root is changed.
        assert t.root is not None and t.root.value == 5
        assert t.root.left is not None and t.root.left.value == 2
        assert t.root.right is not None and t.root.right.value == 9
        # Root is not changed.
        t.insert_many([11, 10])
        check_if_tree_is_balanced(t)
        assert t.root is not None and t.root.value == 5
        assert t.root.right is not None and t.root.right.value == 10
        assert t.root.right.left is not None and t.root.right.left.value == 9
        assert t.root.right.right is not None and t.root.right.right.value == 11

    def test_case_4(self) -> None:
        """Test we have a turn left-right."""
        t = create_tree([9, 2, 5])
        check_if_tree_is_balanced(t)
        # Root is changed.
        assert t.root is not None and t.root.value == 5
        assert t.root.left is not None and t.root.left.value == 2
        assert t.root.right is not None and t.root.right.value == 9
        # Root is not changed.
        t.insert_many([0, 1])
        check_if_tree_is_balanced(t)
        assert t.root is not None and t.root.value == 5
        assert t.root.left is not None and t.root.left.value == 1
        assert t.root.left.left is not None and t.root.left.left.value == 0
        assert t.root.left.right is not None and t.root.left.right.value == 2
