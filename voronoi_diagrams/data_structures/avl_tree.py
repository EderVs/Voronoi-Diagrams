"""AVL Tree."""
# Standard Library
from typing import Any, Optional, Iterable


class AVLNode:
    """AVL Node.

    Factor is used to balance the tree.
    """

    factor: int = 0
    value: Any = None
    length: int = 1
    level: int = 1
    left: Optional["AVLNode"] = None
    right: Optional["AVLNode"] = None
    parent: Optional["AVLNode"] = None
    left_neighbor: Optional["AVLNode"] = None
    right_neighbor: Optional["AVLNode"] = None

    def __init__(self, value: Any, left=None, right=None, parent=None) -> None:
        """AVL Node constructor."""
        self.value = value
        self.left = left
        self.right = right

        if left is not None:
            self.length += left.length
        if right is not None:
            self.length += right.length

    def has_left(self) -> bool:
        """Return if has left child."""
        return self.left is not None

    def has_right(self) -> bool:
        """Return if has right child."""
        return self.right is not None

    def is_contained(self, value: Any, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        raise NotImplementedError

    def is_left(self, value: Any, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        raise NotImplementedError

    def is_right(self, value: Any, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        raise NotImplementedError

    def __str__(self):
        """Get String representation."""
        return f"N({self.value}, l:{self.level}, {self.left}, {self.right})"

    def __repr__(self):
        """Get representation."""
        return self.__str__()


class IntNode(AVLNode):
    """Integer AVLNode."""

    def __init__(self, value: int, left=None, right=None) -> None:
        """Integer AVL Node constructor."""
        super(IntNode, self).__init__(value, left, right)

    def is_contained(self, value: int, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        return value == self.value

    def is_left(self, value: int, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        return value < self.value

    def is_right(self, value: int, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        return value > self.value


class AVLTree:
    """AVL Tree."""

    length: int = 0
    root: Optional[AVLNode] = None

    def __init__(self, node_class=AVLNode):
        """Create AVLTree."""
        self.NODE_CLASS = node_class

    def __str__(self):
        """Get string representation."""
        return str(self.root)

    def __repr__(self):
        """Get representation."""
        return self.__str__()

    def get_node_length(self, node: Optional[AVLNode]) -> int:
        """Get Node length."""
        if node is None:
            return 0
        return node.length

    def get_node_level(self, node: Optional[AVLNode]) -> int:
        """Get Node Level in the Tree."""
        if node is None:
            return 0
        return node.level

    def update_node_length(self, node: Optional[AVLNode]) -> None:
        """Update Node length with the sum of the their childs + 1."""
        if node is not None:
            node.length = (
                self.get_node_length(node.left) + self.get_node_length(node.right) + 1
            )

    def update_node_factor(self, node: Optional[AVLNode]) -> None:
        """Update Node factor with the difference between children lengths."""
        if node is None:
            return
        node.factor = self.get_node_level(node.right) - self.get_node_level(node.left)

    def update_node_level(self, node: Optional[AVLNode]) -> None:
        """Update Node level based on the max of the level of the children + 1."""
        if node is None:
            return
        node.level = (
            max(self.get_node_level(node.left), self.get_node_level(node.right)) + 1
        )

    def turn_left(self, node: AVLNode) -> None:
        """Turn left the sub-tree in the node sent."""
        right = node.right
        if right is None:
            return

        right_left = right.left
        node.right = right_left
        if right_left is not None:
            right_left.parent = node
        right.parent = node.parent
        if node.parent is None:
            self.root = right
        else:
            is_left_child = node.parent.left == node
            if is_left_child:
                node.parent.left = right
            else:
                node.parent.right = right

        node.parent = right
        right.left = node
        self.update_node_length(node)
        self.update_node_length(right)
        self.update_node_level(node)
        self.update_node_level(right)
        self.update_node_factor(node)
        self.update_node_factor(right)

    def turn_right(self, node: AVLNode) -> None:
        """Turn left the sub-tree in the node sent."""
        left = node.left
        if left is None:
            return

        left_right = left.right
        node.left = left_right
        if left_right is not None:
            left_right.parent = node
        left.parent = node.parent

        if node.parent is None:
            self.root = left
        else:
            is_left_child = node.parent.left == node
            if is_left_child:
                node.parent.left = left
            else:
                node.parent.right = left

        node.parent = left
        left.right = node

        self.update_node_length(node)
        self.update_node_length(left)
        self.update_node_level(node)
        self.update_node_level(left)
        self.update_node_factor(node)
        self.update_node_factor(left)

    def rebalance_node(self, node: AVLNode) -> Optional[AVLNode]:
        """Rebalance node.

        Return the new root of the sub-tree.
        """
        if abs(node.factor) <= 1:
            return node
        # Weighted to the right
        if node.factor >= 2:
            child = node.right
            if child is not None and child.factor == -1:
                # Double rotation
                self.turn_right(child)
                child = child.parent
            self.turn_left(node)
        # Weighted to the left
        else:
            child = node.left
            if child is not None and child.factor == 1:
                # Double rotation
                self.turn_left(child)
                child = child.parent
            self.turn_right(node)
        return child

    def rebalance_to_root(self, node: AVLNode) -> None:
        """Rebalance tree from the node given to the root."""
        actual: Optional[AVLNode] = node
        while actual is not None:
            self.update_node_level(actual)
            self.update_node_factor(actual)
            actual = self.rebalance_node(actual)
            if actual is not None:
                actual = actual.parent

    def rebalance_to_node(self, node_start: AVLNode, node_finish: AVLNode) -> None:
        """Rebalance tree from node given to other node given.

        node_finish must be an ancestor of node_start if not it will rebalance to the root.
        node_finish is exclusive.
        """
        actual: Optional[AVLNode] = node_start
        while actual is not None:
            self.update_node_level(actual)
            self.update_node_factor(actual)

            if actual == node_finish:
                self.rebalance_node(actual)
                break

            actual = self.rebalance_node(actual)
            if actual is not None:
                actual = actual.parent

    def insert_many(self, values: Iterable[Any]) -> None:
        """Insert many values."""
        for value in values:
            self.insert(value)

    def insert_from_node(
        self, value: Any, from_node: AVLNode, *args: Any, **kwargs: Any,
    ) -> AVLNode:
        """Insert value with a Node in the Tree."""
        self.length += 1
        # Update length of all node above
        actual_parent: Optional[AVLNode] = from_node.parent
        while actual_parent is not None:
            actual_parent.length += 1
            actual_parent = actual_parent.parent

        node = self.NODE_CLASS(value, *args, **kwargs)

        actual_node: Optional[AVLNode] = from_node
        last_node: AVLNode = from_node
        is_left_child = False
        # Get to a leaf.
        while actual_node is not None:
            actual_node.length += 1
            last_node = actual_node
            if actual_node.is_contained(value) or actual_node.is_left(value):
                actual_node = actual_node.left
                is_left_child = True
            else:
                actual_node = actual_node.right
                is_left_child = False

        node.parent = last_node
        if is_left_child:
            last_node.left = node
        else:
            last_node.right = node

        self.rebalance_to_node(node, from_node)

        return node

    def insert(self, value: Any, *args: Any, **kwargs: Any) -> AVLNode:
        """Insert value with a Node in the Tree."""
        if self.root is None:
            node = self.NODE_CLASS(value, *args, **kwargs)
            self.root = node
            self.length += 1
            return self.root

        node = self.insert_from_node(value, self.root)

        return node

    def get_max_node_in_subtree(self, node: AVLNode) -> AVLNode:
        """Get max Node in a subtree."""
        while node.right is not None:
            node = node.right
        return node

    def get_min_node_in_subtree(self, node: AVLNode) -> AVLNode:
        """Get min Node in a subtree."""
        while node.left is not None:
            node = node.left
        return node

    def get_max_node(self) -> Optional[AVLNode]:
        """Get max Node in a subtree."""
        if self.root is None:
            return None
        return self.get_max_node_in_subtree(self.root)

    def get_min_node(self) -> Optional[AVLNode]:
        """Get min Node in a subtree."""
        if self.root is None:
            return None
        return self.get_min_node_in_subtree(self.root)

    def get_max(self) -> Optional[AVLNode]:
        """Get max value in a subtree."""
        if self.root is None:
            return None
        max_node = self.get_max_node_in_subtree(self.root)
        if max_node is None:
            return None
        return max_node.value

    def get_min(self) -> Optional[AVLNode]:
        """Get min value in a subtree."""
        if self.root is None:
            return None
        min_node = self.get_min_node_in_subtree(self.root)
        if min_node is None:
            return None
        return min_node.value

    def search(self, value: Any) -> Optional[AVLNode]:
        """Search value in the Tree and return the AVLNode."""
        actual = self.root
        while actual is not None:
            if actual.is_contained(value):
                return actual
            if actual.is_left(value):
                actual = actual.left
            else:
                actual = actual.right
        return None

    def remove_node_without_right(self, node: AVLNode) -> Optional[AVLNode]:
        """Remove node in the Tree without right child.

        Returns the sub_tree to be rebalanced.
        """
        if node.parent is None:
            self.root = node.left
            return self.root

        # Node has parent.
        is_left_child = node.parent.left == node
        if is_left_child:
            node.parent.left = node.left
        else:
            node.parent.right = node.left

        if node.left is None:
            return None
        node.left.parent = node.parent
        return node.left

    def remove_node_without_left(self, node: AVLNode) -> Optional[AVLNode]:
        """Remove node in the Tree without left child."""
        if node.parent is None:
            self.root = node.right
            return self.root

        is_left_child = node.parent.left == node
        if is_left_child:
            node.parent.left = node.right
        else:
            node.parent.right = node.right

        if node.right is None:
            return None
        node.right.parent = node.parent
        return node.right

    def remove_node(self, node: AVLNode) -> None:
        """Remove node in the Tree."""
        replace_node: AVLNode
        if node.left is not None:
            is_replace_left = True
            replace_node = self.get_max_node_in_subtree(node.left)
        elif node.right is not None:
            is_replace_left = False
            replace_node = self.get_min_node_in_subtree(node.right)
        else:
            replace_node = node
            is_replace_left = True

        # Update the values
        node.value = replace_node.value

        if is_replace_left:
            to_rebalance = self.remove_node_without_right(replace_node)
        else:
            to_rebalance = self.remove_node_without_left(replace_node)
        if to_rebalance is not None:
            self.rebalance_node(to_rebalance)

    def remove(self, value: Any) -> bool:
        """Search and remove value in the Tree."""
        node = self.search(value)
        if node is None:
            return False

        self.remove_node(node)
        return True

    def is_empty(self) -> bool:
        """Return True if the Tree is Empty."""
        return self.root is None
