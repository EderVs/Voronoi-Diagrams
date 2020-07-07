"""Conic Section Models."""

# Standard Library
from typing import Optional, Tuple, Any, List

# Numpy
from numpy import roots

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

    def y_formula(self, x: Decimal) -> List[Decimal]:
        """Get y from x.

        If there is no solution then None is returned.
        The solutions are in a tuple.
        """
        b = self.b * x + self.e
        a = self.c
        c = (self.a * (x ** 2)) + (self.d * x) + (self.f)
        xs = roots([a, b, c])
        to_return = []
        for x in xs:
            if x.imag == 0:
                to_return.append(Decimal(x.real))
        return to_return

    def x_formula(self, y: Decimal) -> List[Decimal]:
        """Get x from y.

        If there is no solution then None is returned.
        The solutions are in a tuple.
        """
        y1 = self.b * y + self.d
        b = y1
        a = self.a
        c = self.c * (y ** 2) + self.e * y + self.f
        xs = roots([a, b, c])
        to_return = []
        for x in xs:
            if x.imag == 0:
                to_return.append(Decimal(x.real))
        return to_return

    def __get_ys_of_intersections(
        self, x: Decimal, conic_section
    ) -> List[Tuple[Decimal, Decimal]]:
        """Get ys of intersections."""
        ys = self.y_formula(x)
        other_ys = conic_section.y_formula(x)
        intersections: List[Tuple[Decimal, Decimal]] = []
        if len(ys) == 0 or len(other_ys) == 0:
            return []

        epsilon = Decimal("0.0001")
        for y in ys:
            for other_y in other_ys:
                if are_close(y, other_y, epsilon):
                    intersections.append((x, y))
        return intersections

    def __get_intersections(
        self, ps: List[Decimal], conic_section: Any,
    ) -> List[Tuple[Decimal, Decimal]]:
        """Get intersections using polinomial roots."""
        intersections: List[Tuple[Decimal, Decimal]] = []
        for x in roots(ps):
            if Decimal(x.imag) < Decimal("0.00001"):
                intersections += self.__get_ys_of_intersections(
                    Decimal(x.real), conic_section
                )
        return intersections

    def __get_intersections_of_vertical(
        self, ps: List[Decimal], conic_section: Any
    ) -> List[Tuple[Decimal, Decimal]]:
        """Get intersections of a vertical line."""
        intersections = []
        for x in roots(ps):
            if x.imag == 0:
                other_ys = conic_section.y_formula(Decimal(x))
                for other_y in other_ys:
                    intersections.append((Decimal(x), Decimal(other_y)))
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
        if (cs_b == 0 and cs_c == 0 and cs_e == 0) and (
            cs_h == 0 and cs_i == 0 and cs_k == 0
        ):
            return []
        elif (cs_b == 0 and cs_c == 0 and cs_e == 0) or (
            cs_h == 0 and cs_i == 0 and cs_k == 0
        ):
            if cs_h == 0 and cs_i == 0 and cs_k == 0:
                cs_a = conic_section.a
                cs_d = conic_section.d
                cs_f = conic_section.f
                conic_section = self
            intersections = self.__get_intersections_of_vertical(
                [cs_a, cs_d, cs_f], conic_section
            )
        elif cs_c == 0 and cs_i == 0:
            a1 = cs_a * cs_h
            a2 = cs_a * cs_k + cs_d * cs_h
            a3 = cs_d * cs_k + cs_f * cs_h
            a4 = cs_f * cs_k
            b1 = cs_g * cs_b
            b2 = cs_g * cs_e + cs_j * cs_b
            b3 = cs_j * cs_e + cs_l * cs_b
            b4 = cs_l * cs_e
            c1 = a1 - b1
            c2 = a2 - b2
            c3 = a3 - b3
            c4 = a4 - b4
            intersections = self.__get_intersections([c1, c2, c3, c4], conic_section)
        elif cs_c == 0 or cs_i == 0:
            if cs_i == 0:
                # Changing variables.
                cs_a = conic_section.a
                cs_b = conic_section.b
                cs_d = conic_section.d
                cs_e = conic_section.e
                cs_f = conic_section.f
                cs_g = self.a
                cs_h = self.b
                cs_i = self.c
                cs_j = self.d
                cs_k = self.e
                cs_l = self.f
            a = 2 * cs_i
            b = cs_b * cs_h
            c = (cs_b * cs_k) + (cs_e * cs_h)
            d = cs_e * cs_k
            e = (-a * cs_a) + b
            f = (-a * cs_d) + c
            g = (-a * cs_f) + d
            h1 = (cs_b ** 2) * (cs_h ** 2)
            h2 = (2 * (cs_b ** 2) * cs_h * cs_k) + (2 * cs_b * cs_e * (cs_h ** 2))
            h3 = (
                ((cs_b ** 2) * (cs_k ** 2))
                + (4 * cs_b * cs_e * cs_h * cs_k)
                + ((cs_e ** 2) * (cs_h ** 2))
            )
            h4 = (2 * cs_b * cs_e * (cs_k ** 2)) + (2 * (cs_e ** 2) * cs_h * cs_k)
            h5 = (cs_e ** 2) * (cs_k ** 2)
            i1 = 4 * (cs_b ** 2) * cs_i * cs_g
            i2 = (4 * (cs_b ** 2) * cs_i * cs_j) + (8 * cs_b * cs_e * cs_i * cs_g)
            i3 = (
                (4 * (cs_b ** 2) * cs_i * cs_l)
                + (8 * cs_b * cs_e * cs_i * cs_j)
                + (4 * (cs_e ** 2) * cs_i * cs_g)
            )
            i4 = (8 * cs_b * cs_e * cs_i * cs_l) + (4 * (cs_e ** 2) * cs_i * cs_j)
            i5 = 4 * (cs_e ** 2) * cs_i * cs_l
            j1 = h1 - i1
            j2 = h2 - i2
            j3 = h3 - i3
            j4 = h4 - i4
            j5 = h5 - i5
            k1 = (e ** 2) - j1
            k2 = (2 * e * f) - j2
            k3 = (f ** 2) + (2 * e * g) - j3
            k4 = (2 * f * g) - j4
            k5 = (g ** 2) - j5
            intersections = self.__get_intersections(
                [k1, k2, k3, k4, k5], conic_section
            )
        else:
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
                (4 * cs_c * cs_f * (i ** 2))
                + (4 * cs_c * cs_d * j)
                + (4 * cs_c * cs_a * h)
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

            intersections = self.__get_intersections(
                [p1, p2, p3, p4, p5], conic_section
            )
        return intersections

    def get_changes_of_sign_in_x(self) -> List[Decimal]:
        """Get changes of sign in the y_formula."""
        a = self.b ** 2 - 4 * self.c * self.a
        b = 2 * self.b * self.e - 4 * self.c * self.d
        c = self.e ** 2 - 4 * self.c * self.f
        xs = []
        for x in roots([a, b, c]):
            if x.imag == 0:
                xs.append(Decimal(x.real))
        return xs
