"""L list implementation."""

# Standard Library
from typing import Any, Optional, Tuple

# AVL
from .avl_tree import AVLTree, AVLNode

# Models
from voronoi_diagrams.models import Region, Event, Bisector, Site, Point, Boundary


class LNode(AVLNode):
    """List L AVLNode that contains Region in their values."""

    def __init__(self, value: Region, left=None, right=None) -> None:
        """List L AVL Node constructor."""
        super(LNode, self).__init__(value, left, right)

    def is_contained(self, value: Region, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        return self.value.is_contained(value.site.get_event_point())

    def is_left(self, value: Region, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        return self.value.is_left(value.site.get_event_point())

    def is_right(self, value: Region, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        return self.value.is_right(value.site.get_event_point())


class LList:
    """List L used in the Fortune's Algorithm."""

    t: AVLTree
    head: Optional[LNode]

    def __init__(self, root: Region):
        """Construct Tree t.

        The list must have a root region. If there is one region, this region must not have any
        boundaries.
        """
        self.t = AVLTree(node_class=LNode)
        self.head = self.t.insert(root)  # type: ignore

    def __str__(self):
        """Get string representation."""
        # No blank spaces after docstring.
        def get_region_str(region: Optional[Region]) -> str:
            """Get string representation of Region in l list."""
            if region is not None:
                return f"R({region.site.name})"
            else:
                return ""

        def get_boundary_str(boundary: Optional[Boundary]) -> str:
            """Get string representation of Boundary in l list."""
            if boundary is not None:
                return (
                    f"B{'+' if boundary.sign else '-'}("
                    f"{boundary.bisector.sites[0].name}, {boundary.bisector.sites[1].name})"
                )
            else:
                return "None"

        string = (
            f"[None, {get_region_str(self.head.value)}, "
            f"{get_boundary_str(self.head.value.right)}"
        )
        node = self.head.right_neighbor
        while node is not None:
            string += (
                f", {get_region_str(node.value)}, "
                f"{get_boundary_str(node.value.right)}"
            )
            node = node.right_neighbor
        string += "]"
        return string

    def __repr__(self):
        """Get representation."""
        return self.__str__()

    def search_region_node(self, region: Region) -> LNode:
        """Search the node of the region where a point is located given a y coordinate."""
        node = self.t.search(region)
        if node is None:
            # TODO: Create exception.
            raise Exception(
                "Cannot find a region with this point. Are your boundaries, "
                "regions and y coordinate right?"
            )
        return node  # type: ignore

    def search_region_contained(self, region: Region) -> Region:
        """Search the region where a point is located given a y coordinate."""
        return self.search_region_node(region).value

    def update_neighbors(
        self, left_node: Optional[LNode], right_node: Optional[LNode]
    ) -> None:
        """Update neighbors between 2 nodes."""
        if left_node is not None:
            left_node.right_neighbor = right_node
            if left_node.left_neighbor is None:
                self.head = left_node
        elif right_node is not None:
            self.head = right_node
        else:
            self.head = None

        if right_node is not None:
            right_node.left_neighbor = left_node

    def update_boundaries(
        self,
        left_node: Optional[LNode],
        boundary: Optional[Boundary],
        right_node: Optional[LNode],
    ) -> None:
        """Update boundary in between 2 nodes."""
        if left_node is not None:
            left_node.value.right = boundary

        if right_node is not None:
            right_node.value.left = boundary

    def update_regions(
        self, left_region: Region, center_region: Region, right_region: Region,
    ) -> Tuple[LNode, LNode, LNode]:
        """Update the L list given a site and the regions to put.

        - left_region is the Region that will be in the left. This region must have q as its site.
        - center_region is the Region that will be in the center. This region must have p as its
          site.
        - right_region is the Region that will be in the right. This region must have q as its site.
        """
        node = self.search_region_node(center_region)

        node.value = center_region

        # Insert in AVLTree
        # Insert in the left sub tree
        if node.left is not None:
            left_region_node = self.t.insert_all_right_from_node(left_region, node.left)
        else:
            self.t.length += 1
            node.length += 1
            left_region_node = LNode(left_region)
            left_region_node.parent = node
            node.left = left_region_node
            self.t.rebalance_to_node(left_region_node, node)

        # Insert in the right sub tree
        if node.right is not None:
            right_region_node = self.t.insert_all_left_from_node(
                right_region, node.right
            )
        else:
            self.t.length += 1
            node.length += 1
            right_region_node = LNode(right_region)
            right_region_node.parent = node
            node.right = right_region_node
            self.t.rebalance_to_node(right_region_node, node)

        self.t.rebalance_to_root(node)

        # Update like a list.
        left_neighbor = node.left_neighbor
        right_neighbor = node.right_neighbor
        if left_neighbor is None:
            self.head = left_region_node  # type: ignore
        self.update_neighbors(left_neighbor, left_region_node)  # type: ignore
        self.update_neighbors(left_region_node, node)  # type: ignore
        self.update_neighbors(node, right_region_node)  # type: ignore
        self.update_neighbors(right_region_node, right_neighbor)  # type: ignore
        return (left_region_node, node, right_region_node)  # type: ignore

    def remove_region(self, region_node: LNode, new_boundary: Optional[Boundary]):
        """Remove region in regionNode."""
        left_neighbor: LNode = region_node.left_neighbor  # type: ignore
        right_neighbor: LNode = region_node.right_neighbor  # type: ignore
        self.update_neighbors(left_neighbor, right_neighbor)
        self.update_boundaries(left_neighbor, new_boundary, right_neighbor)
        self.t.remove_node(region_node)
