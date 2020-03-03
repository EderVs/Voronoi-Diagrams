"""AVL Tree."""
# Standard Library
from typing import Any, Optional


class AVLNode:
    """AVL Node.

    Factor is used to balance the tree.
    """

    factor: int = 0
    value: Any = None
    left: Optional[AVLNode] = None
    right: Optional[AVLNode] = None

    def __init__(self, factor, value, left=None, right=None):
        """AVL Node constructor."""
        self.factor = factor
        self.value = value
