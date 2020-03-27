"""Q Queue implementation."""

# Standard Library
from typing import Any, Optional

# AVL
from .avl_tree import AVLTree, AVLNode

# Models
from .models import Event


class QNode(AVLNode):
    """Queue Q AVLNode that contains an event in their values."""

    def __init__(self, value: Event, left=None, right=None) -> None:
        """List L AVL Node constructor."""
        super(QNode, self).__init__(value, left, right)
        # Just renaming for clarity.
        self.event: Event = self.value

    def is_contained(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        return (
            value.point.y == self.value.point.y and value.point.x == self.value.point.x
        )

    def is_left(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        if value.point.y == self.value.point.y:
            return value.point.x < self.value.point.x
        return value.point.y < self.value.point.y

    def is_right(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        if value.point.y == self.value.point.y:
            return value.point.x > self.value.point.x
        return value.point.y > self.value.point.y


class QQueue:
    """Queue Q used in the Fortune's Algorithm."""

    t: AVLTree
    head: Optional[QNode]

    def __init__(self, root: Event):
        """Construct Tree t."""
        self.t = AVLTree(node_class=QNode)
        self.head = self.t.insert(root)  # type: ignore

    def __str__(self) -> str:
        """Get string representation."""
        return str(self.t)

    def __repr__(self):
        """Get representation."""
        return self.__str__()
