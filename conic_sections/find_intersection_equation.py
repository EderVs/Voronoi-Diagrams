"""Find intersection of two hyperbolas equation"""
# Standard Library
from decimal import Decimal

# Models.
from voronoi_diagrams.models import (
    WeightedPointBisector,
    Point,
    WeightedSite,
)

# Plot.
from matplotlib import pyplot as plt
import numpy as np

# Utils.
from plots.utils.models.bisectors import plot_weighted_point_bisector
from plots.utils.models.sites import create_weighted_site
from general_utils.numbers import are_close


def test_equation(bisector1, bisector2, sign_1, sign_2, x):
    """Test equation with given x value."""
    epsilon = 0.00001

    if sign_1:
        value1 = bisector1.formula_y(x)[0]
    else:
        value1 = bisector1.formula_y(x)[2]
    if sign_2:
        value2 = bisector2.formula_y(x)[0]
    else:
        value2 = bisector2.formula_y(x)[1]
    assert are_close(value1, value2, epsilon,)

    # First Bisector
    cs_a = bisector1.a
    cs_b = bisector1.b
    cs_c = bisector1.c
    cs_d = bisector1.d
    cs_e = bisector1.e
    cs_f = bisector1.f
    # Second Bisector
    cs_g = bisector2.a
    cs_h = bisector2.b
    cs_i = bisector2.c
    cs_j = bisector2.d
    cs_k = bisector2.e
    cs_l = bisector2.f

    one_1 = 1 if sign_1 else -1
    one_2 = 1 if sign_2 else -1

    # Validate Equations.
    left = (
        -(cs_b * x + cs_e)
        + one_1
        * Decimal(
            (cs_b * x + cs_e) ** 2 - 4 * cs_c * (cs_a * (x ** 2) + cs_d * x + cs_f)
        ).sqrt()
    ) / (2 * cs_c)
    right = (
        -(cs_h * x + cs_k)
        + one_2
        * Decimal(
            (cs_h * x + cs_k) ** 2 - 4 * cs_i * (cs_g * (x ** 2) + cs_j * x + cs_l)
        ).sqrt()
    ) / (2 * cs_i)
    print("First")
    print(left, right)
    assert are_close(left, right, epsilon)
    # Substitute a
    a = cs_i / cs_c
    left = (
        -a * (cs_b * x + cs_e)
        + a
        * one_1
        * Decimal(
            (cs_b * x + cs_e) ** 2 - 4 * cs_c * (cs_a * (x ** 2) + cs_d * x + cs_f)
        ).sqrt()
        + (cs_h * x + cs_k)
    )
    right = (
        one_2
        * Decimal(
            (cs_h * x + cs_k) ** 2 - 4 * cs_i * (cs_g * (x ** 2) + cs_j * x + cs_l)
        ).sqrt()
    )
    print("Substitute a")
    print(left, right)
    assert are_close(left, right, epsilon)
    # Substitute b and c
    b = cs_h - a * cs_b
    c = cs_k - a * cs_e
    left = (
        b * x
        + c
        + a
        * one_1
        * Decimal(
            (cs_b * x + cs_e) ** 2 - 4 * cs_c * (cs_a * (x ** 2) + cs_d * x + cs_f)
        ).sqrt()
    )
    # Right is the same as before
    print("Substitute b and c")
    print(left, right)
    assert are_close(left, right, epsilon)
    # Substitute d
    d = 4 * cs_i
    left = (((one_1) * 2 * b * x * a) + ((one_1) * 2 * c * a)) * Decimal(
        (cs_b * x + cs_e) ** 2 - 4 * cs_c * (cs_a * (x ** 2) + cs_d * x + cs_f)
    ).sqrt()
    right = (
        ((cs_h * x + cs_k) ** 2)
        - (d * (cs_g * (x ** 2) + cs_j * x + cs_l))
        - ((b ** 2) * (x ** 2))
        - (c ** 2)
        - ((a ** 2) * ((cs_b * x + cs_e) ** 2))
        + (4 * (a ** 2) * cs_c * (cs_a * (x ** 2) + cs_d * x + cs_f))
        - (2 * b * x * c)
    )
    print("Substitute d")
    print(left, right)
    assert are_close(left, right, epsilon)
    # Substitute e, f and g
    # Left is the same
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
    right = (f * (x ** 2)) + (g * x) + e
    print("Substitute e, f and g")
    print(left, right)
    assert are_close(left, right, epsilon)
    # Substitute h, i and j
    h = (2 * c * a) ** 2
    i = 2 * b * a
    j = 8 * b * (a ** 2) * c
    left = (((i ** 2) * (x ** 2)) + (j * x) + h) * (
        (cs_b * x + cs_e) ** 2 - 4 * cs_c * (cs_a * (x ** 2) + cs_d * x + cs_f)
    )
    right = right ** 2
    # To keep epsilon short
    print("Substitute h, i and j")
    print(Decimal(left).sqrt(), Decimal(right).sqrt())
    assert are_close(Decimal(left).sqrt(), Decimal(right).sqrt(), epsilon)
    # Change before ln
    left = ((((i ** 2) * (x ** 2)) + (j * x) + h) * ((cs_b * x + cs_e) ** 2)) - (
        (((i ** 2) * (x ** 2)) + (j * x) + h)
        * (4 * cs_c * (cs_a * (x ** 2) + cs_d * x + cs_f))
    )
    print("Change before ln")
    print(Decimal(left).sqrt(), Decimal(right).sqrt()())
    assert are_close(Decimal(left).sqrt(), Decimal(right).sqrt(), epsilon)
    # Step 1 l1, l2, l3, l4, l5
    s1 = (((i ** 2) * (x ** 2)) + (j * x) + h) * ((cs_b * x + cs_e) ** 2)
    print("s1")
    print(s1)
    # Step 2 l1, l2, l3, l4, l5
    s2 = (((i ** 2) * (x ** 2)) + (j * x) + h) * (
        ((cs_b ** 2) * (x ** 2)) + (2 * cs_b * cs_e * x) + (cs_e ** 2)
    )
    print("s2")
    print(s1, s2)
    assert are_close(Decimal(s1).sqrt(), Decimal(s2).sqrt(), epsilon)
    # Step 3 l1, l2, l3, l4, l5
    s3 = (
        (
            ((i ** 2) * (x ** 2))
            * (((cs_b ** 2) * (x ** 2)) + (2 * cs_b * cs_e * x) + (cs_e ** 2))
        )
        + ((j * x) * (((cs_b ** 2) * (x ** 2)) + (2 * cs_b * cs_e * x) + (cs_e ** 2)))
        + (h * (((cs_b ** 2) * (x ** 2)) + (2 * cs_b * cs_e * x) + (cs_e ** 2)))
    )
    print("s3")
    print(s2, s3)
    assert are_close(Decimal(s2).sqrt(), Decimal(s3).sqrt(), epsilon)
    # Step 4 l1, l2, l3, l4, l5
    l1 = (cs_b ** 2) * (i ** 2)
    l2 = (2 * cs_b * cs_e * (i ** 2)) + ((cs_b ** 2) * j)
    l3 = ((cs_e ** 2) * (i ** 2)) + (2 * cs_b * cs_e * j) + ((cs_b ** 2) * h)
    l4 = ((cs_e ** 2) * j) + (2 * cs_b * cs_e * h)
    l5 = h * (cs_e ** 2)
    ln = (l1 * (x ** 4)) + (l2 * (x ** 3)) + (l3 * (x ** 2)) + (l4 * x) + l5
    print("s4")
    print(s3, ln)
    assert are_close(Decimal(s3).sqrt(), Decimal(ln).sqrt(), epsilon)
    # Substitute l1, l2, l3, l4, l5
    left = ln - (
        (((i ** 2) * (x ** 2)) + (j * x) + h)
        * (4 * cs_c * (cs_a * (x ** 2) + cs_d * x + cs_f))
    )
    # Right is the same
    print("Substitute l1, l2, l3, l4, l5")
    print(left, right)
    assert are_close(Decimal(left).sqrt(), Decimal(right).sqrt(), epsilon)
    # Substitute m1, m2, m3, m4, m5
    m1 = -(4 * cs_c * cs_a * (i ** 2))
    m2 = -((4 * cs_c * cs_d * (i ** 2)) + (4 * cs_c * cs_a * j))
    m3 = -((4 * cs_c * cs_f * (i ** 2)) + (4 * cs_c * cs_d * j) + (4 * cs_c * cs_a * h))
    m4 = -((4 * cs_c * cs_f * j) + (4 * cs_c * cs_d * h))
    m5 = -(4 * cs_c * cs_f * h)
    m = (m1 * (x ** 4)) + (m2 * (x ** 3)) + (m3 * (x ** 2)) + (m4 * x) + m5
    left = ln + m
    # Right is the same
    print("Substitute m1, m2, m3, m4, m5")
    print(left, right)
    assert are_close(Decimal(left).sqrt(), Decimal(right).sqrt(), epsilon)
    # Substitute n1, n2, n3, n4, n5
    n1 = l1 + m1
    n2 = l2 + m2
    n3 = l3 + m3
    n4 = l4 + m4
    n5 = l5 + m5
    left = (n1 * (x ** 4)) + (n2 * (x ** 3)) + (n3 * (x ** 2)) + (n4 * x) + n5
    # Right is the same
    print("Substitute n1, n2, n3, n4, n5")
    print(left, right)
    assert are_close(Decimal(left).sqrt(), Decimal(right).sqrt(), epsilon)
    # Substitute o1, o2, o3, o4, o5
    o1 = f ** 2
    o2 = 2 * f * g
    o3 = (2 * f * e) + (g ** 2)
    o4 = 2 * g * e
    o5 = e ** 2
    right = (o1 * (x ** 4)) + (o2 * (x ** 3)) + (o3 * (x ** 2)) + (o4 * x) + o5
    # left is the same
    print("Substitute o1, o2, o3, o4, o5")
    print(left, right)
    assert are_close(Decimal(left).sqrt(), Decimal(right).sqrt(), epsilon)
    # Substitute p1, p2, p3, p4, p5
    p1 = n1 - o1
    p2 = n2 - o2
    p3 = n3 - o3
    p4 = n4 - o4
    p5 = n5 - o5
    left = (p1 * (x ** 4)) + (p2 * (x ** 3)) + (p3 * (x ** 2)) + (p4 * x) + p5
    right = 0
    # left is the same
    print("Substitute p1, p2, p3, p4, p5")
    print(left, right)
    assert are_close(left, right, 0.1)


x1 = 3
y1 = -4
w1 = 2
p1 = create_weighted_site(x1, y1, w1)
x2 = 3
y2 = 1
w2 = 1
p2 = create_weighted_site(x2, y2, w2)
x3 = 0.5
y3 = -1
w3 = 1.5
p3 = create_weighted_site(x3, y3, w3)
p1_p2_bisector = WeightedPointBisector(sites=(p1, p2))
p2_p3_bisector = WeightedPointBisector(sites=(p2, p3))
# We know that these 2 bisector have an intersection in (3,0)
x_1 = 3

print("#1")
test_equation(p1_p2_bisector, p2_p3_bisector, False, False, x_1)

x1 = -3.5
y1 = 0
w1 = 2
p1 = create_weighted_site(x1, y1, w1)
x2 = 0
y2 = -2.5
w2 = 1
p2 = create_weighted_site(x2, y2, w2)
x3 = 0
y3 = 2
w3 = 1.5
p3 = create_weighted_site(x3, y3, w3)
p1_p2_bisector = WeightedPointBisector(sites=(p1, p2))
p2_p3_bisector = WeightedPointBisector(sites=(p2, p3))
# We know that these 2 bisector have an intersection in (0,0)
x_2 = 0

print("#2")
test_equation(p1_p2_bisector, p2_p3_bisector, True, False, x_2)

x1 = -3
y1 = 1
w1 = 2 * Decimal(2).sqrt()
p1 = create_weighted_site(x1, y1, w1)
x2 = 6
y2 = 10
w2 = Decimal(2).sqrt()
p2 = create_weighted_site(x2, y2, w2)
x3 = -4
y3 = 0
w3 = 3 * Decimal(2).sqrt()
p3 = create_weighted_site(x3, y3, w3)
p1_p2_bisector = WeightedPointBisector(sites=(p1, p2))
p2_p3_bisector = WeightedPointBisector(sites=(p2, p3))
# We know that these 2 bisector have an intersection in (2,6)
x_3 = 2

print("#3")
test_equation(p1_p2_bisector, p2_p3_bisector, False, False, x_3)

x1 = 7
y1 = 1
w1 = 2 * Decimal(2).sqrt()
p1 = create_weighted_site(x1, y1, w1)
x2 = 6
y2 = 10
w2 = Decimal(2).sqrt()
p2 = create_weighted_site(x2, y2, w2)
x3 = -4
y3 = 0
w3 = 3 * Decimal(2).sqrt()
p3 = create_weighted_site(x3, y3, w3)
p1_p2_bisector = WeightedPointBisector(sites=(p1, p2))
p2_p3_bisector = WeightedPointBisector(sites=(p2, p3))
# We know that these 2 bisector have an intersection in (2,6)
x_4 = 2

print("#4")
test_equation(p1_p2_bisector, p2_p3_bisector, False, False, x_4)
