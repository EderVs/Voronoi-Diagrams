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

    def __str__(self):
        """Get string representation."""
        return str(self.value)

    def is_contained(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        return value == self.value

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

    def __init__(self):
        """Construct Tree t."""
        self.t = AVLTree(node_class=QNode)

    def __str__(self) -> str:
        """Get string representation."""
        return str(self.t)

    def __repr__(self):
        """Get representation."""
        return self.__str__()

    def enqueue(self, event: Event):
        """Enqueue an event."""
        self.t.insert(event)

    def delete(self, event: Event):
        """Delete an event."""
        self.t.remove(event)

    def dequeue(self) -> Optional[Event]:
        """Get the next event.

        Get the minimun in y axis event and delete it.
        """
        node = self.t.get_min()
        if node is None:
            return None
        self.t.remove_node(node)
        return node.value