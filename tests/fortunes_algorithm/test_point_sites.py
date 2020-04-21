"""Test Algorithm using Point Sites."""
# Standard
from typing import List, Any

# Models
from voronoi_diagrams.data_structures.models import Site, PointBisector

# Algorithm
from voronoi_diagrams.fortunes_algorithm import FortunesAlgorithm, VoronoiDiagram


class TestBoundaryFormulas:
    """Test formula."""

    def test_point_formulas_positive_fixed_values(self):
        """Create Diagram of 2 sites."""
        p = Site(0, 0)
        q = Site(2, 2)
        sites = (p, q)
        bisector = PointBisector(sites)
        voronoi_diagram = FortunesAlgorithm.calculate_voronoi_diagram(sites)
        assert len(voronoi_diagram.bisectors) == 1
        assert set(voronoi_diagram.bisectors[0].sites) == set(bisector.sites)
        assert len(voronoi_diagram.vertex) == 0
