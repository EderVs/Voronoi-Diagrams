"""L list implementation."""

# Standard Library
from typing import Any

# AVL
from .avl_tree import AVLTree, AVLNode

# Models
from .models import Region, Event, Bisector, Site, Point


class LNode(AVLNode):
    """List L AVLNode that contains Region in their values."""

    def __init__(self, value: Region, left=None, right=None) -> None:
        """List L AVL Node constructor."""
        super(LNode, self).__init__(value, left, right)
        # Just renaming for clarity.
        self.region: Region = self.value

    def is_contained(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is contained in the Node."""
        return self.region.is_contained(value.point)

    def is_left(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the left of Node."""
        return self.region.is_left(value.point)

    def is_right(self, value: Event, *args: Any, **kwargs: Any) -> bool:
        """Value is to the right of Node."""
        return self.region.is_right(value.point)


class ListL:
    """List L used in the Fortune's Algorithm."""

    t: AVLTree

    def __init__(self, root: Region):
        """Construct Tree t.

        The list must have a root region. If there is one region, this region must not have any
        boundaries.
        """
        self.t = AVLTree(node_class=LNode)
        self.t.insert(root)

    def _search_region_node(self, event: Event) -> LNode:
        """Search the node of the region where a point is located given a y coordinate."""
        node = self.t.search(event)
        if node is None:
            # TODO: Create exception.
            raise Exception(
                "Cannot find a region with this point. Are your boundaries, "
                "regions and y coordinate right?"
            )
        return node  # type: ignore

    def search_region_contained(self, event: Event) -> Region:
        """Search the region where a point is located given a y coordinate."""
        return self._search_region_node(event).region

    def update_with_site(
        self,
        site_p: Site,
        region_left: Region,
        region_center: Region,
        region_right: Region,
    ):
        """Update the L list given a site and the y coordinate.

        Suppose p is the site given.
        1.- Search for the Region where the site is contained. Suppose that the site of the region
            found is q and and lets name the Region Rq.
        2.- Let Rp the Region of p. Update the node that contains the Rq with -> Rq, Rp, Rq.
            Each Region will update its boundaries.
        3.- Return the intersections to be deleted.
        """
        node = self._search_region_node(site_p)
        # TODO: Update this node with the regions.
