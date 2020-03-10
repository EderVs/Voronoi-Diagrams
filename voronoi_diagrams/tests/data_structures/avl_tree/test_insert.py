"""AVL Tree Tests."""
from typing import List, Any
from voronoi_diagrams.data_structures import AVLTree, IntNode


def create_tree(to_insert: List) -> AVLTree:
    """Create a tree."""
    t = AVLTree(node_class=IntNode)
    for number in to_insert:
        t.insert(t)
    return t


def check_if_tree_is_balanced(t: AVLTree) -> None:
    """Check that the tree sent has all their factors correct.
    
    Contains assertions.
    """
    queue: List[Any] = list()
    queue.append(t.root)
    while queue is not []:
        node = queue.pop(0)
        assert abs(node.factor) <= 1
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)


def test_case_1() -> None:
    """Test we have a a turn left."""
    t = create_tree([1, 2, 3])
    check_if_tree_is_balanced(t)
    # Root is changed.
    assert t.root is not None and t.root.value == 2
    t.insert_many([4, 5])
    check_if_tree_is_balanced(t)
    assert t.root is not None and t.root.value == 2
    assert t.root.right is not None and t.root.right.value == 4
