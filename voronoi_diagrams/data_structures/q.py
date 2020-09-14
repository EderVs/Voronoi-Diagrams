"""Q Queue implementation."""

# Standard Library
from typing import Any, Optional, List

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
        comparison = self.value.get_comparison(value)
        return comparison == 0

    def is_left(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        comparison = self.value.get_comparison(value)
        print("comparison")
        print(comparison)
        return comparison > 0

    def is_right(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        comparison = self.value.get_comparison(value)
        return comparison < 0


class QQueue:
    """Queue Q used in the Fortune's Algorithm."""

    t: AVLTree
    head: Optional[QNode]

    def __init__(self):
        """Construct Tree t."""
        self.t = AVLTree(node_class=QNode)

    def __str__(self) -> str:
        """Get string representation."""
        return f"Q: {str(self.get_all_events())}"

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

    def get_all_events(self) -> List[Event]:
        """Get all events sorted."""
        return self.t.dfs_inorder()
