"""Conic Section Models."""

# Standard Library
from typing import Optional, Tuple, Any, List

# Numpy
from numpy import roots, isrealobj

# Utils
from general_utils.numbers import are_close

# Math
from decimal import Decimal


class ConicSection:
    """Conic Section representation.

    The conic section is represented as:
        ax^2 + bxy + cy^2 + dx + ey + f = 0
    """

    a: Decimal
    b: Decimal
    c: Decimal
    d: Decimal
    e: Decimal
    f: Decimal

    def __init__(
        self, a: Decimal, b: Decimal, c: Decimal, d: Decimal, e: Decimal, f: Decimal
    ) -> None:
        """Conic Section constructor."""
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def y_formula(self, x: Decimal) -> Optional[Tuple[Decimal, Decimal]]:
        """Get y from x.

        If there is no solution then None is returned.
        The solutions are in a tuple.
        """
        x1 = self.b * x + self.e
        x2 = (x1 ** 2) - 4 * self.c * (self.a * (x ** 2) + self.d * x + self.f)
        if x2 < 0:
            # The sqrt is negative.
            return None

        y1 = (-x1 - x2.sqrt()) / (2 * self.c)
        y2 = (-x1 + x2.sqrt()) / (2 * self.c)
        return (y1, y2)

    def x_formula(self, y: Decimal) -> Optional[Tuple[Decimal, Decimal]]:
        """Get x from y.

        If there is no solution then None is returned.
        The solutions are in a tuple.
        """
        y1 = self.b * y + self.d
        y2 = (y1 ** 2) - 4 * self.a * (self.c * (y ** 2) + self.e * y + self.f)
        if y2 < 0:
            # The sqrt is negative.
            return None

        x1 = (-y1 - y2.sqrt()) / (2 * self.a)
        x2 = (-y1 + y2.sqrt()) / (2 * self.a)
        return (x1, x2)

    def __get_ys_of_intersections(
        self, x: Decimal, conic_section
    ) -> List[Tuple[Decimal, Decimal]]:
        """Get ys of intersections."""
        ys = self.y_formula(x)
        other_ys = conic_section.y_formula(x)
        intersections: List[Tuple[Decimal, Decimal]] = []
        if ys is None or other_ys is None:
            return []

        epsilon = Decimal("0.0001")
        for y in ys:
            for other_y in other_ys:
                if are_close(y, other_y, epsilon):
                    intersections.append((x, y))
        return intersections

    def __get_intersections(
        self,
        p1: Decimal,
        p2: Decimal,
        p3: Decimal,
        p4: Decimal,
        p5: Decimal,
        conic_section: Any,
    ) -> List[Tuple[Decimal, Decimal]]:
        xs = [Decimal(x) for x in roots([p1, p2, p3, p4, p5])]
        intersections: List[Tuple[Decimal, Decimal]] = []
        for x in xs:
            if isrealobj(x):
                intersections += self.__get_ys_of_intersections(x, conic_section)
        return intersections

    def get_intersection(self, conic_section: Any) -> List[Tuple[Decimal, Decimal]]:
        """Get the intersection of 2 conic sections.

        The solutions are returned in a list of max length 4.
        """
        # First Conic section
        cs_a = self.a
        cs_b = self.b
        cs_c = self.c
        cs_d = self.d
        cs_e = self.e
        cs_f = self.f
        # Second Conic section
        cs_g = conic_section.a
        cs_h = conic_section.b
        cs_i = conic_section.c
        cs_j = conic_section.d
        cs_k = conic_section.e
        cs_l = conic_section.f
        a = cs_i / cs_c
        b = cs_h - a * cs_b
        c = cs_k - a * cs_e
        d = 4 * cs_i
        e = (
            (cs_k ** 2)
            - (d * cs_l)
            - (c ** 2)
            - ((a ** 2) * (cs_e ** 2))
            + (4 * (a ** 2) * cs_c * cs_f)
        )
        f = (
            (cs_h ** 2)
            - (d * cs_g)
            - (b ** 2)
            - ((a ** 2) * (cs_b ** 2))
            + (4 * (a ** 2) * cs_c * cs_a)
        )
        g = (
            (2 * cs_h * cs_k)
            - (d * cs_j)
            - (2 * cs_b * cs_e * (a ** 2))
            + (4 * (a ** 2) * cs_c * cs_d)
            - (2 * b * c)
        )
        h = (2 * c * a) ** 2
        i = 2 * b * a
        j = 8 * b * (a ** 2) * c
        l1 = (cs_b ** 2) * (i ** 2)
        l2 = (2 * cs_b * cs_e * (i ** 2)) + ((cs_b ** 2) * j)
        l3 = ((cs_e ** 2) * (i ** 2)) + (2 * cs_b * cs_e * j) + ((cs_b ** 2) * h)
        l4 = ((cs_e ** 2) * j) + (2 * cs_b * cs_e * h)
        l5 = h * (cs_e ** 2)
        m1 = -(4 * cs_c * cs_a * (i ** 2))
        m2 = -((4 * cs_c * cs_d * (i ** 2)) + (4 * cs_c * cs_a * j))
        m3 = -(
            (4 * cs_c * cs_f * (i ** 2)) + (4 * cs_c * cs_d * j) + (4 * cs_c * cs_a * h)
        )
        m4 = -((4 * cs_c * cs_f * j) + (4 * cs_c * cs_d * h))
        m5 = -(4 * cs_c * cs_f * h)
        n1 = l1 + m1
        n2 = l2 + m2
        n3 = l3 + m3
        n4 = l4 + m4
        n5 = l5 + m5
        o1 = f ** 2
        o2 = 2 * f * g
        o3 = (2 * f * e) + (g ** 2)
        o4 = 2 * g * e
        o5 = e ** 2
        p1 = n1 - o1
        p2 = n2 - o2
        p3 = n3 - o3
        p4 = n4 - o4
        p5 = n5 - o5

        intersections = self.__get_intersections(p1, p2, p3, p4, p5, conic_section)
        return intersections
