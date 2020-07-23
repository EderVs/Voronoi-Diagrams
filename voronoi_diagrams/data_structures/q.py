"""Q Queue implementation."""

# Standard Library
from typing import Any, Optional

# AVL
from .avl_tree import AVLTree, AVLNode

# Models
from voronoi_diagrams.models import Event


class QNode(AVLNode):
    """Queue Q AVLNode that contains an event in their values."""

    def __init__(self, value: Event, left=None, right=None) -> None:
        """List L AVL Node constructor."""
        super(QNode, self).__init__(value, left, right)

    def __str__(self):
        """Get string representation."""
        return str(self.value)

    def is_contained(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        if self.value.is_site == value.is_site:
            return value == self.value
        return False

    def is_left(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        event_point = self.value.get_event_point()
        other_event_point = value.get_event_point()
        if other_event_point.y == event_point.y:
            return other_event_point.x < event_point.x
        return other_event_point.y < event_point.y

    def is_right(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        event_point = self.value.get_event_point()
        other_event_point = value.get_event_point()
        if other_event_point.y == event_point.y:
            return other_event_point.x > event_point.x
        return other_event_point.y > event_point.y


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
        node = self.t.get_min_node()
        if node is None:
            return None
        event = node.value
        self.t.remove_node(node)
        return event

    def is_empty(self) -> bool:
        """Return True if the Queue is Empty."""
        return self.t.is_empty()
