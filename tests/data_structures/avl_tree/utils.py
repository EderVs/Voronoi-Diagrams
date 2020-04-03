"""AVL Tree utils in Tests."""
from typing import List, Any
from random import shuffle
from voronoi_diagrams.data_structures import AVLTree, IntNode


def create_tree(to_insert: List[int]) -> AVLTree:
    """Create a tree."""
    t = AVLTree(node_class=IntNode)
    for number in to_insert:
        t.insert(number)
    return t


def remove_many(t: AVLTree, int_list: List[int]) -> None:
    """Remove a list of ints in a tree."""
    for value in int_list:
        t.remove(value)
        check_if_tree_is_balanced(t)
        check_if_tree_is_correct(t)


def check_if_tree_is_correct(t: AVLTree) -> None:
    """Check that the tree sent has all nodes in their place.

    Contains assertions.
    """
    queue: List[Any] = list()
    if t.root is None:
        return
    queue.append(t.root)
    while len(queue) > 0:
        node = queue.pop(0)
        if node.left is not None:
            assert node.left.parent.value == node.value
            assert node.left.value <= node.value
            queue.append(node.left)
        if node.right is not None:
            assert node.right.parent.value == node.value
            assert node.right.value > node.value
            queue.append(node.right)


def check_if_tree_is_balanced(t: AVLTree) -> None:
    """Check that the tree sent has all their factors correct.

    Contains assertions.
    """
    queue: List[Any] = list()
    if t.root is None:
        return
    queue.append(t.root)
    while len(queue) > 0:
        node = queue.pop(0)
        assert abs(node.factor) <= 1
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
