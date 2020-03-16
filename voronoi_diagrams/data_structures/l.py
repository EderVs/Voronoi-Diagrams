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
        return self.value.is_contained(value.point)

    def is_left(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        return self.value.is_left(value.point)

    def is_right(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        return self.value.is_right(value.point)


class ListL:
    """List L used in the Fortune's Algorithm."""

    t: AVLTree

    def __init__(self):
        """Construct Tree t."""
        self.t = AVLTree()
