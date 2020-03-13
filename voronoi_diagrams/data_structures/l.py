"""L list implementation."""

# Standard Library
from typing import Any

# AVL
from . import AVLTree, AVLNode

# Models
from .models import Region, Event


class LNode(AVLNode):
    """List L AVLNode that contains Region in their values."""

    def __init__(self, value: Region, left=None, right=None) -> None:
        """List L AVL Node constructor."""
        super(LNode, self).__init__(value, left, right)
        # Just renaming for clarity.
        self.region: Region = self.value

    def is_contained(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        point = value.point
        is_left_contained = True
        is_right_contained = True
        if self.region.left is None and self.region.right is None:
            return True
        if self.region.right is not None:
            is_right_contained = self.region.right.get_point_comparison(point) <= 0
        if self.region.left is not None:
            is_left_contained = self.region.left.get_point_comparison(point) >= 0
        return is_left_contained and is_right_contained

    def is_left(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        if self.region.left is None:
            return False
        point = value.point
        return self.region.left.get_point_comparison(point) < 0

    def is_right(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        if self.region.right is None:
            return False
        point = value.point
        return self.region.right.get_point_comparison(point) > 0


class ListL:
    """List L used in the Fortune's Algorithm."""

    t: AVLTree

    def __init__(self):
        """Construct Tree t."""
        self.t = AVLTree()
