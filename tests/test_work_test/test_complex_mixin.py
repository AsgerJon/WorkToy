"""
TestComplexMixin tests 'ComplexMixin' from 'worktoy.work_test'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys

from worktoy.waitaminute import TypeException
from worktoy.work_test import ComplexMixin
from . import WorkTestTest, SimpleComplex, WrongComplex


class TestComplexMixin(WorkTestTest):
  """
  'ComplexMixin' gives a class the arithmetic of 'complex' from the two
  fields 'REAL' and 'IMAG', the worked example the bank runs against.
  The tests pin the constructors, the fields and their refusals, the
  coercion of an operand, every operator with instances, numbers,
  builtin complexes and the operands it refuses, the two texts, the
  equality that takes numbers and implementations alone, the hash of
  'complex', the truth test against machine epsilon, and iteration.
  """

  def test_constructors(self) -> None:
    zero = SimpleComplex()
    self.assertEqual((zero.REAL, zero.IMAG), (0.0, 0.0))
    one = SimpleComplex(1 + 2j)
    self.assertEqual((one.REAL, one.IMAG), (1.0, 2.0))
    parsed = SimpleComplex('1+2j')
    self.assertEqual((parsed.REAL, parsed.IMAG), (1.0, 2.0))
    real = SimpleComplex(3)
    self.assertEqual((real.REAL, real.IMAG), (3.0, 0.0))
    both = SimpleComplex(1, 2)
    self.assertEqual((both.REAL, both.IMAG), (1.0, 2.0))
    self.assertIs(type(both.REAL), float)
    self.assertIs(type(both.IMAG), float)
    with self.assertRaises(TypeError) as context:
      SimpleComplex(1, 2, 3)
    self.assertEqual(str(context.exception), 'SimpleComplex takes at most '
                                             'two components, the real and '
                                             'the imaginary part, but '
                                             'received 3.')
    with self.assertRaises(ValueError):
      SimpleComplex('abc')

  def test_fields(self) -> None:
    value = SimpleComplex()
    value.REAL = 2
    value.IMAG = 3.5
    self.assertEqual((value.REAL, value.IMAG), (2.0, 3.5))
    with self.assertRaises(TypeException) as context:
      value.REAL = 'x'
    self.assertTypeRefused(context.exception, 'REAL', 'x', float)
    with self.assertRaises(TypeException) as context:
      value.IMAG = None
    self.assertTypeRefused(context.exception, 'IMAG', None, float)
    self.assertEqual((value.REAL, value.IMAG), (2.0, 3.5))
    value.__real_value__ = 'x'
    with self.assertRaises(TypeException) as context:
      _ = value.REAL
    self.assertTypeRefused(context.exception, '__real_value__', 'x', float)
    value.__imag_value__ = 'y'
    with self.assertRaises(TypeException) as context:
      _ = value.IMAG
    self.assertTypeRefused(context.exception, '__imag_value__', 'y', float)
    blank = SimpleComplex()
    with self.assertRaises(RecursionError) as context:
      blank._getReal(_recursion=True)
    self.assertEqual(context.exception.args, ())
    with self.assertRaises(RecursionError) as context:
      blank._getImag(_recursion=True)
    self.assertEqual(context.exception.args, ())
    self.assertEqual((blank.REAL, blank.IMAG), (0.0, 0.0))
    self.assertEqual(blank._getReal(_recursion=True), 0.0)
    self.assertEqual(blank._getImag(_recursion=True), 0.0)

  def test_coercion(self) -> None:
    value = SimpleComplex(1, 2)
    self.assertIs(SimpleComplex._resolveOther(value), value)
    cases = (
      (3, SimpleComplex(3, 0)), (1.5, SimpleComplex(1.5, 0)),
      (1 + 1j, SimpleComplex(1, 1)), ('2+3j', SimpleComplex(2, 3)),
      ((1, 1), SimpleComplex(1, 1)), ([4, 5], SimpleComplex(4, 5)),
      (WrongComplex(6, 7), SimpleComplex(6, 7)),
    )
    for other, expected in cases:
      with self.subTest(other=repr(other)):
        resolved = SimpleComplex._resolveOther(other)
        self.assertIs(type(resolved), SimpleComplex)
        self.assertEqual(resolved, expected)
    for other in ('abc', object(), [1, 2, 3], ('a', 'b'), None):
      with self.subTest(other=repr(other)):
        self.assertIs(SimpleComplex._resolveOther(other), NotImplemented)

  def test_arithmetic(self) -> None:
    a = SimpleComplex(3, 4)
    b = SimpleComplex(1, 2)
    self.assertEqual(a + b, SimpleComplex(4, 6))
    self.assertEqual(a + 2, SimpleComplex(5, 4))
    self.assertEqual(2 + a, SimpleComplex(5, 4))
    self.assertEqual(a + (1 + 2j), SimpleComplex(4, 6))
    self.assertEqual(a + WrongComplex(1, 1), SimpleComplex(4, 5))
    self.assertEqual(a - b, SimpleComplex(2, 2))
    self.assertEqual(10 - a, SimpleComplex(7, -4))
    self.assertEqual(a * b, SimpleComplex(-5, 10))
    self.assertEqual(2 * a, SimpleComplex(6, 8))
    quotient = a / b
    self.assertAlmostEqual(quotient.REAL, 2.2)
    self.assertAlmostEqual(quotient.IMAG, -0.4)
    self.assertEqual(2 / SimpleComplex(1, 1), SimpleComplex(1, -1))
    self.assertEqual(1 / SimpleComplex(2, 0), SimpleComplex(0.5, 0))
    self.assertEqual(SimpleComplex(1, 1) / 2, SimpleComplex(0.5, 0.5))
    square = SimpleComplex(0, 1) ** 2
    self.assertAlmostEqual(square.REAL, -1.0)
    self.assertAlmostEqual(square.IMAG, 0.0)
    cube = 2 ** SimpleComplex(3, 0)
    self.assertAlmostEqual(cube.REAL, 8.0)
    self.assertAlmostEqual(cube.IMAG, 0.0)
    self.assertEqual(a.conjugate(), SimpleComplex(3, -4))
    self.assertEqual(+a, a)
    self.assertIsNot(+a, a)
    self.assertEqual(-a, SimpleComplex(-3, -4))
    self.assertEqual(~a, SimpleComplex(3, -4))
    self.assertEqual(abs(a), 5.0)
    self.assertEqual(complex(a), 3 + 4j)
    self.assertEqual([*a], [3.0, 4.0])
    for result in (a + b, a - b, a * b, a / b, a ** 2, a.conjugate()):
      with self.subTest(result=repr(result)):
        self.assertIs(type(result), SimpleComplex)

  def test_operators_refuse_strangers(self) -> None:
    a = SimpleComplex(3, 4)
    for other in ('x', None, object()):
      with self.subTest(other=repr(other)):
        self.assertIs(a.__add__(other), NotImplemented)
        self.assertIs(a.__radd__(other), NotImplemented)
        self.assertIs(a.__sub__(other), NotImplemented)
        self.assertIs(a.__rsub__(other), NotImplemented)
        self.assertIs(a.__mul__(other), NotImplemented)
        self.assertIs(a.__rmul__(other), NotImplemented)
        self.assertIs(a.__truediv__(other), NotImplemented)
        self.assertIs(a.__rtruediv__(other), NotImplemented)
        self.assertIs(a.__pow__(other), NotImplemented)
        self.assertIs(a.__rpow__(other), NotImplemented)
        self.assertIs(a.__eq__(other), NotImplemented)
        with self.assertRaises(TypeError):
          _ = a + other
        with self.assertRaises(TypeError):
          _ = other - a
        with self.assertRaises(TypeError):
          _ = a * other
        with self.assertRaises(TypeError):
          _ = other / a
        with self.assertRaises(TypeError):
          _ = a ** other
    with self.assertRaises(ZeroDivisionError) as context:
      _ = a / 0
    self.assertEqual(str(context.exception), 'complex division by zero')
    with self.assertRaises(ZeroDivisionError) as context:
      _ = a / SimpleComplex()
    self.assertEqual(str(context.exception), 'complex division by zero')
    small = a / SimpleComplex(1e-9, 0)
    self.assertAlmostEqual(small.REAL, 3e9, delta=1.0)

  def test_texts(self) -> None:
    cases = (
      (SimpleComplex(), 'SimpleComplex()', '0'),
      (SimpleComplex(1), 'SimpleComplex(1.000)', '1.000'),
      (SimpleComplex(0, 2), 'SimpleComplex(0.0, 2.000)', '2.000J'),
      (SimpleComplex(1, -2), 'SimpleComplex(1.000, -2.000)',
       '1.000 - 2.000J'),
      (SimpleComplex(1, 2), 'SimpleComplex(1.000, 2.000)',
       '1.000 + 2.000J'),
      (SimpleComplex(1e-20, 1e-20), 'SimpleComplex()', '0'),
      (ComplexMixin(2, 0), 'ComplexMixin(2.000)', '2.000'),
      (SimpleComplex(1, 0.5), 'SimpleComplex(1.000, 0.500)',
       '1.000 + 0.500J'),
      (SimpleComplex(1, -0.5), 'SimpleComplex(1.000, -0.500)',
       '1.000 - 0.500J'),
    )
    for value, expectedRepr, expectedStr in cases:
      with self.subTest(expectedRepr=expectedRepr):
        self.assertEqual(repr(value), expectedRepr)
        self.assertEqual(str(value), expectedStr)

  def test_epsilon_boundary(self) -> None:
    #  A part equal to machine epsilon is not below it, so it shows, and
    #  a magnitude equal to it is not above it, so the value is zero.
    epsilon = sys.float_info.epsilon
    self.assertEqual(repr(SimpleComplex(1, epsilon)),
                     'SimpleComplex(1.000, 0.000)')
    self.assertEqual(str(SimpleComplex(1, epsilon)), '1.000 + 0.000J')
    self.assertEqual(repr(SimpleComplex(epsilon, 1)),
                     'SimpleComplex(0.000, 1.000)')
    self.assertEqual(str(SimpleComplex(epsilon, 1)), '0.000 + 1.000J')
    self.assertFalse(SimpleComplex(epsilon, 0))
    self.assertEqual(abs(SimpleComplex(epsilon, 0)), epsilon)
    self.assertTrue(SimpleComplex(2 * epsilon, 0))
    self.assertEqual(repr(SimpleComplex(epsilon, 0)), 'SimpleComplex()')

  def test_equality_hash_and_truth(self) -> None:
    self.assertEqual(SimpleComplex(1, 2), SimpleComplex(1, 2))
    self.assertNotEqual(SimpleComplex(1, 2), SimpleComplex(2, 1))
    self.assertNotEqual(SimpleComplex(1, 2), SimpleComplex(1, 3))
    self.assertNotEqual(SimpleComplex(1, 3), SimpleComplex(1, 2))
    self.assertNotEqual(SimpleComplex(1, 2), SimpleComplex(2, 2))
    self.assertNotEqual(SimpleComplex(2, 2), SimpleComplex(1, 2))
    self.assertEqual(SimpleComplex(1, 2), 1 + 2j)
    self.assertEqual(SimpleComplex(3), 3)
    self.assertEqual(SimpleComplex(1.5), 1.5)
    self.assertEqual(SimpleComplex(1, 2), WrongComplex(1, 2))
    self.assertIs(SimpleComplex(1, 2).__eq__((1, 2)), NotImplemented)
    self.assertFalse(SimpleComplex(1, 2) == (1, 2))
    self.assertFalse(SimpleComplex(1, 2) == '1+2j')
    self.assertEqual(hash(SimpleComplex(1, 2)), hash(1 + 2j))
    self.assertEqual(len({SimpleComplex(1, 2), SimpleComplex(1, 2)}), 1)
    self.assertFalse(SimpleComplex())
    self.assertTrue(SimpleComplex(1e-10))
    self.assertFalse(SimpleComplex(1e-20, 1e-20))
    self.assertTrue(SimpleComplex(0, -1))

  def test_random_round_trips(self) -> None:
    self.randomFloat.size = 8
    for x, y in zip(self.randomFloat.row, self.randomFloat.row):
      with self.subTest(x=x, y=y):
        value = SimpleComplex(x, y)
        self.assertEqual(value, complex(x, y))
        self.assertEqual(SimpleComplex(complex(x, y)), value)
        self.assertEqual(value.conjugate().conjugate(), value)
        self.assertEqual(value + value, 2 * value)
        self.assertEqual(value - value, SimpleComplex())
        self.assertAlmostEqual(abs(value), abs(complex(x, y)))
