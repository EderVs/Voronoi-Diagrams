"""Plot WeightedPointBoundary."""
from voronoi_diagrams.models import (
    Point,
    WeightedSite,
    WeightedPointBisector,
    WeightedPointBoundary,
)
from plots.plot_utils.models.boundaries import plot_boundary
from plotly import graph_objects as go
from decimal import Decimal

p1 = Point(Decimal("2"), Decimal("10.7"))
w1 = Decimal("3.1")
p2 = Point(Decimal("6"), Decimal("10.6"))
w2 = Decimal("0")
s1 = WeightedSite(p1.x, p1.y, w1)
s2 = WeightedSite(p2.x, p2.y, w2)
b = WeightedPointBisector([s1, s2])
b_plus = WeightedPointBoundary(b, True)
b_minus = WeightedPointBoundary(b, False)
figure = go.Figure()
xlim = (-100, 100)
ylim = (-100, 100)
plot_boundary(figure, b_minus, xlim, ylim, WeightedPointBisector)
plot_boundary(figure, b_plus, xlim, ylim, WeightedPointBisector)
figure.show()
