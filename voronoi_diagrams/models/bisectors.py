"""Bisector representation."""

# Standard Library
from typing import Tuple, Optional, Any, List
from abc import ABC, abstractmethod

# Models
from .events import Site, WeightedSite, Coordinates
from .points import Point

# Conic Sections
from conic_sections.models import ConicSection

# Math
from decimal import Decimal

# Utils
from general_utils.numbers import are_close


class Bisector(ABC):
    """Bisector representation."""

    sites: Tuple[Site, Site]

    def __init__(self, sites: Tuple[Site, Site]) -> None:
        """Construct bisector."""
        if sites[0].point.y < sites[1].point.y or (
            sites[0].point.y == sites[1].point.y
            and sites[0].point.x <= sites[1].point.x
        ):
            sites = (sites[1], sites[0])
        self.sites = sites

    def __eq__(self, bisector: "Bisector") -> bool:
        """Equality between bisectors."""
        return self.sites == bisector.sites

    @abstractmethod
    def formula_x(self, y: Decimal) -> List[Decimal]:
        """Get x coordinate given a y coordinate."""
        raise NotImplementedError

    @abstractmethod
    def formula_y(self, x: Decimal) -> List[Decimal]:
        """Get y coordinate given a x coordinate."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Get bisector string representation."""
        return f"B({self.sites[0]}, {self.sites[1]})"

    def small_str(self) -> str:
        """Get bisector small string representation."""
        return f"B{self.get_sites_names()}"

    def get_sites_names(self) -> str:
        """Get bisector small string representation."""
        return f"({self.sites[0].name}, {self.sites[1].name})"

    def __repr__(self) -> str:
        """Get Bisector representation."""
        return self.__str__()

    @abstractmethod
    def get_intersections(self, bisector: "Bisector") -> List[Point]:
        """Get the points of intersection between two bisectors."""
        raise NotImplementedError

    @abstractmethod
    def are_same_slope(self, bisector: "Bisector") -> bool:
        """Compare if the given bisector slope is the same as the slope of this bisector."""
        raise NotImplementedError

    def get_middle_between_sites(self) -> Point:
        """Get Middle point between sites."""
        site1, site2 = self.sites
        point1 = Point(
            site1.get_x_frontier_pointing_to_point(site2.point),
            site1.get_y_frontier_pointing_to_point(site2.point),
        )
        point2 = Point(
            site2.get_x_frontier_pointing_to_point(site1.point),
            site2.get_y_frontier_pointing_to_point(site1.point),
        )
        point_x = min(point1.x, point2.x) + (abs(point1.x - point2.x) / 2)
        point_y = min(point1.y, point2.y) + (abs(point1.y - point2.y) / 2)
        return Point(point_x, point_y)

    def get_site(self) -> Site:
        """Get the site that is highest or more to the left."""
        return self.get_sites_tuple()[0]

    @abstractmethod
    def get_sites_tuple(self) -> Tuple[Site, Site]:
        """Get sites tuple sorted."""
        raise NotImplementedError

    def get_object_to_hash(self) -> Tuple[Coordinates, Coordinates]:
        """Get object to hash this site."""
        sites_tuple = self.get_sites_tuple()
        return (
            sites_tuple[0].get_object_to_hash(),
            sites_tuple[1].get_object_to_hash(),
        )

    @abstractmethod
    def is_vertical(self) -> bool:
        """Get if the bisector is vertical."""
        raise NotImplementedError

    def is_point_in_bisector(self, x: Decimal, y: Decimal) -> bool:
        """Get if the point is part of bisector.

        A point is in the bisector if the point is to the same distance to both sites.
        """
        site1, site2 = self.sites
        epsilon = Decimal("0.001")
        return are_close(
            site1.get_site_distance(x, y), site2.get_site_distance(x, y), epsilon,
        )


class PointBisector(Bisector):
    """Bisector defined by point sites."""

    def __init__(self, sites: Tuple[Site, Site]):
        """Construct bisector of Point sites Bisector."""
        super(PointBisector, self).__init__(sites)

    def formula_x(self, y: Decimal) -> List[Decimal]:
        """Get x coordinate given the y coordinate.

        In this case is a line.
        """
        p_site = self.sites[0]
        p = p_site.point
        q_site = self.sites[1]
        q = q_site.point

        if q.y == p.y:
            distance = p_site.get_site_distance(q.x, q.y)
            return [min(p.x, q.x) + (distance / 2)]
        if q.x == p.x:
            return []

        a = (2 * q.y - 2 * p.y) * y + (p.y ** 2 - q.y ** 2) - (q.x ** 2 - p.x ** 2)
        b = 2 * p.x - 2 * q.x
        return [a / b]

    def formula_y(self, x: Decimal) -> List[Decimal]:
        """Get y coordinate given the x coordinate.

        In this case is a line.
        """
        p_site = self.sites[0]
        p = p_site.point
        q_site = self.sites[1]
        q = q_site.point

        if q.x == p.x:
            distance = p_site.get_distance_to_site_point_from_point(q.x, q.y)
            return [min(p.y, q.y) + (distance / 2)]
        if q.y == p.y:
            return []

        a = Decimal(-((q.x - p.x) / (q.y - p.y)))
        b = Decimal((q.x ** 2 - p.x ** 2 + q.y ** 2 - p.y ** 2) / (2 * (q.y - p.y)))
        return [a * x + b]

    def is_vertical(self) -> bool:
        """Get if the bisector is vertical."""
        p, q = self.sites
        return q.point.y == p.point.y

    def is_horizontal(self) -> bool:
        """Get if the bisector is horizontal."""
        p, q = self.sites
        return q.point.x == p.point.x

    def get_intersections(self, bisector: "PointBisector") -> List[Point]:
        """Get the point of intersection between two bisectors."""
        # No blank spaces after docstring.
        def f_aux_1(xi: Decimal, xj: Decimal, yi: Decimal, yj: Decimal) -> Decimal:
            """Auxiliar function."""
            return (xj ** 2 - xi ** 2 + yj ** 2 - yi ** 2) / (2 * (yj - yi))

        def f_aux_2(xi: Decimal, xj: Decimal, yi: Decimal, yj: Decimal) -> Decimal:
            """Auxiliar function."""
            return (xj - xi) / (yj - yi)

        def get_x(
            xi: Decimal,
            xj: Decimal,
            xk: Decimal,
            xl: Decimal,
            yi: Decimal,
            yj: Decimal,
            yk: Decimal,
            yl: Decimal,
        ) -> Decimal:
            return (f_aux_1(xk, xl, yk, yl) - f_aux_1(xi, xj, yi, yj)) / (
                f_aux_2(xk, xl, yk, yl) - f_aux_2(xi, xj, yi, yj)
            )

        if self.is_vertical() and bisector.is_vertical():
            return []
        elif self.is_vertical() or bisector.is_vertical():
            return self._get_intersections_when_one_is_vertical(bisector)

        if self.is_horizontal() and bisector.is_horizontal():
            return []
        elif self.is_horizontal() or bisector.is_horizontal():
            return self._get_intersections_when_one_is_horizontal(bisector)

        x1 = self.sites[0].point.x
        x2 = self.sites[1].point.x
        y1 = self.sites[0].point.y
        y2 = self.sites[1].point.y

        x3 = bisector.sites[0].point.x
        x4 = bisector.sites[1].point.x
        y3 = bisector.sites[0].point.y
        y4 = bisector.sites[1].point.y

        if self.are_same_slope(bisector):
            return []

        x = get_x(x1, x2, x3, x4, y1, y2, y3, y4)
        return [Point(x, self.formula_y(x)[0])]

    def _get_intersections_when_one_is_vertical(
        self, bisector: "PointBisector"
    ) -> List[Point]:
        vertical = self
        other = bisector
        if bisector.is_vertical():
            vertical = bisector
            other = self
        x = vertical.get_middle_between_sites().x
        ys = other.formula_y(x)
        if len(ys) == 0:
            return []
        return [Point(x, ys[0])]

    def _get_intersections_when_one_is_horizontal(
        self, bisector: "PointBisector"
    ) -> List[Point]:
        horizontal = self
        other = bisector
        if bisector.is_horizontal():
            horizontal = bisector
            other = self
        y = horizontal.get_middle_between_sites().y
        xs = other.formula_x(y)
        if len(xs) == 0:
            return []
        return [Point(xs[0], y)]

    def are_same_slope(self, bisector: "PointBisector") -> bool:
        """Compare if the given bisector slope is the same as the slope of this bisector."""
        p_1 = self.sites[0].point
        p_2 = self.sites[1].point
        q_1 = bisector.sites[0].point
        q_2 = bisector.sites[1].point
        delta_y_is_zero = p_1.y - p_2.y == 0 and q_1.y - q_2.y == 0
        delta_x_is_zero = p_1.x - p_2.x == 0 and q_1.x - q_2.x == 0
        both_deltas_are_the_same = (
            p_1.y - p_2.y == q_1.y - q_2.y and p_1.x - p_2.x == q_1.x - q_2.x
        )
        return delta_y_is_zero or delta_x_is_zero or both_deltas_are_the_same

    def get_sites_tuple(self) -> Tuple[Site, Site]:
        """Get the site tuple sorted.

        First checks that the y coordinates of each event point and returns first the highest.
        If both event points are cohorizontal then returns first the one more to the left.
        """
        site1, site2 = self.sites
        event1, event2 = site1.get_event_point(), site2.get_event_point()
        if (event1.y > event2.y) or (event1.y == event2.y and event1.x <= event2.x):
            return (site1, site2)
        else:
            return (site2, site1)


class WeightedPointBisector(Bisector):
    """Bisector defined by weighted sites."""

    sites: Tuple[WeightedSite, WeightedSite]
    a: Decimal
    b: Decimal
    c: Decimal
    d: Decimal
    e: Decimal
    conic_section: ConicSection
    # In case that the sites have the same weights.
    point_bisector: Optional[PointBisector]

    def __init__(self, sites: Tuple[WeightedSite, WeightedSite]):
        """Construct bisector of weighted sites.

        In this case the Sites are WeightedSites.
        """
        super(WeightedPointBisector, self).__init__(sites)
        p, q = sites
        self.point_bisector = None
        if p.weight == q.weight:
            # We take the points without weights.
            new_p = Site(p.point.x, p.point.y, p.name,)
            new_q = Site(q.point.x, q.point.y, q.name,)
            # We use the PointBisector of the points without weights.
            self.point_bisector = PointBisector(sites=(new_p, new_q))
        self._set_polynomial_parameters()
        self.conic_section = ConicSection(
            self.a, self.b, self.c, self.d, self.e, self.f
        )

    def is_vertical(self) -> bool:
        """Get if the bisector is vertical."""
        p_site, q_site = self.sites
        return q_site.point.y == p_site.point.y and q_site.weight == p_site.weight

    def _set_polynomial_parameters(self) -> None:
        """Set parameters of general conic formula.

        Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0
        """
        p = self.sites[0]
        q = self.sites[1]
        px = p.point.x
        py = p.point.y
        pw = p.weight
        qx = q.point.x
        qy = q.point.y
        qw = q.weight
        if self.point_bisector:
            # The bisector is a line.
            self.a = Decimal(0)
            self.b = Decimal(0)
            self.c = Decimal(0)
            self.d = Decimal(2 * qx - 2 * px)
            self.e = Decimal(2 * qy - 2 * py)
            self.f = Decimal((px ** 2) + (py ** 2) - (qx ** 2) - (qy ** 2))
        else:
            r = (qx ** 2) + (qy ** 2) - (px ** 2) - (py ** 2) - ((pw - qw) ** 2)
            s = 4 * ((pw - qw) ** 2)
            self.a = Decimal(s - (((2 * px) - (2 * qx)) ** 2))
            self.b = Decimal((-2) * ((2 * px) - (2 * qx)) * ((2 * py) - (2 * qy)))
            self.c = Decimal(s - (((2 * py) - (2 * qy)) ** 2))
            self.d = Decimal((-2 * px * s) - (2 * ((2 * px) - (2 * qx)) * r))
            self.e = Decimal((-2 * py * s) - (2 * ((2 * py) - (2 * qy)) * r))
            self.f = Decimal((s * (px ** 2)) + (s * (py ** 2)) - (r ** 2))

    def formula_x(self, y: Decimal) -> List[Decimal]:
        """Get x coordinate given the y coordinate.

        In this case is an hyperbola.
        """
        if self.point_bisector:
            return self.point_bisector.formula_x(y)

        return_values = []
        xs = self.conic_section.x_formula(y)
        for x in xs:
            if self.is_point_in_bisector(x, y) and x not in return_values:
                return_values.append(x)

        return return_values

    def formula_y(self, x: Decimal) -> List[Decimal]:
        """Get y coordinate given the x coordinate.

        In this case is an hyperbola
        """
        if self.point_bisector:
            return self.point_bisector.formula_y(x)

        return_values = []
        ys = self.conic_section.y_formula(x)
        for y in ys:
            if self.is_point_in_bisector(x, y) and y not in return_values:
                return_values.append(y)

        return return_values

    def get_intersections(self, bisector: "WeightedPointBisector") -> List[Point]:
        """Get the point of intersection between two Weighted Point Bisectors."""
        all_intersections = self.conic_section.get_intersections(bisector.conic_section)
        valid_intersections = []
        epsilon = Decimal("0.001")
        for x, y in all_intersections:
            if self.is_point_in_bisector(x, y) and bisector.is_point_in_bisector(x, y):
                for valid_intersection in valid_intersections:
                    if are_close(valid_intersection.x, x, epsilon) and are_close(
                        valid_intersection.y, y, epsilon
                    ):
                        break
                else:
                    valid_intersections.append(Point(x, y))
        return valid_intersections

    def are_same_slope(self, bisector: "WeightedPointBisector") -> bool:
        """Compare if the given bisector slope is the same as the slope of this bisector."""
        return False

    def get_vertical_tangents(self) -> List[Decimal]:
        """Get vertical tangents in the bisector."""
        if self.point_bisector:
            return []

        xs = self.conic_section.get_vertical_tangents()
        valid_xs = []
        for x in xs:
            decimals = Decimal("4")
            multiplier = Decimal("10") ** decimals
            truncated_x = Decimal(int(x * multiplier) / multiplier)
            ys = self.formula_y(truncated_x)
            if len(ys) >= 1:
                valid_xs.append(x)
            else:
                # Second chance.
                ys = self.formula_y(truncated_x + Decimal("0.0001"))
                if len(ys) >= 1:
                    valid_xs.append(x)
                else:
                    # Third Chance
                    ys = self.formula_y(truncated_x - Decimal("0.0001"))
                    if len(ys) >= 1:
                        valid_xs.append(x)

        return valid_xs

    def get_sites_tuple(self) -> Tuple[WeightedSite, WeightedSite]:
        """Get site tuple sorted.

        First checks that the y coordinates of each event point and returns first the highest.
        If both event points are cohorizontal then returns first the one with more weight.
        If both sites have the same weight then returns first the one more the left.
        """
        site1, site2 = self.sites
        event1, event2 = site1.get_event_point(), site2.get_event_point()
        if (
            (event1.y > event2.y)
            or (event1.y == event2.y and site1.weight > site2.weight)
            or (
                event1.y == event2.y
                and site1.weight == site2.weight
                and event1.x <= event2.x
            )
        ):
            return (site1, site2)
        else:
            return (site2, site1)
