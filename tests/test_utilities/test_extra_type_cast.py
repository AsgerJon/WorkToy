"""
TestExtraTypeCast provides more unittests for the typeCast function,
which is used to cast values to specific types.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import UtilitiesTest
from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException


class Dummy:
  def __str__(self) -> str:
    return "dummy"


class Troll:
  def __str__(self) -> tuple:
    return (1, 2)


class TypeCastTestCase(UtilitiesTest):
  """
  Unittests for the typeCast function. Tests all major branches,
  including success and failure cases.
  """

  def testCoverage(self):
    """Ensure all branches of typeCast are covered."""
    with self.assertRaises(TypeError):
      _ = str(Troll())
    you = Dummy()
    self.assertEqual(str(you), "dummy")

  def testStrCast(self):
    """Casts to str. Includes bytes/bytearray, failure for bad type."""
    self.assertEqual(typeCast(str, 'hello'), 'hello')
    self.assertEqual(typeCast(str, b'abc'), 'abc')
    self.assertEqual(typeCast(str, bytearray(b'xyz')), 'xyz')
    with self.assertRaises(TypeCastException):
      typeCast(str, 123)
    with self.assertRaises(TypeCastException):
      typeCast(str, Dummy())
    with self.assertRaises(TypeCastException):
      typeCast(str, Troll())

  def testBoolCast(self):
    """Casts to bool. Only 0, 1, True, False allowed."""
    self.assertIs(typeCast(bool, 0), False)
    self.assertIs(typeCast(bool, 1), True)
    self.assertIs(typeCast(bool, True), True)
    self.assertIs(typeCast(bool, False), False)
    with self.assertRaises(TypeCastException):
      typeCast(bool, 2)
    with self.assertRaises(TypeCastException):
      typeCast(bool, "True")
    with self.assertRaises(TypeCastException):
      typeCast(bool, [0])

  def testIntCast(self):
    """Casts to int. Accepts int, float (only if integer), complex (real
    only, integer); refuses str."""
    self.assertEqual(typeCast(int, 5), 5)
    self.assertEqual(typeCast(int, 7.0), 7)
    self.assertEqual(typeCast(int, complex(9, 0)), 9)
    with self.assertRaises(TypeCastException):
      typeCast(int, "42")
    with self.assertRaises(TypeCastException):
      typeCast(int, 3.14)
    with self.assertRaises(TypeCastException):
      typeCast(int, complex(1, 2))
    with self.assertRaises(TypeCastException):
      typeCast(int, "notanumber")

  def testFloatCast(self):
    """Casts to float. Accepts float, int, complex (real only); refuses
    str."""
    self.assertEqual(typeCast(float, 2.5), 2.5)
    self.assertEqual(typeCast(float, 4), 4.0)
    self.assertEqual(typeCast(float, complex(8, 0)), 8.0)
    with self.assertRaises(TypeCastException):
      typeCast(float, "3.14")
    with self.assertRaises(TypeCastException):
      typeCast(float, complex(1, 1))
    with self.assertRaises(TypeCastException):
      typeCast(float, "xyz")

  def testComplexCast(self):
    """Casts to complex. Accepts complex, int, float; refuses str."""
    self.assertEqual(typeCast(complex, 3), 3.0 + 0j)
    self.assertEqual(typeCast(complex, 2.5), 2.5 + 0j)
    self.assertEqual(typeCast(complex, complex(4, 1)), 4 + 1j)
    with self.assertRaises(TypeCastException):
      typeCast(complex, "1+2j")
    with self.assertRaises(TypeCastException):
      typeCast(complex, "notcomplex")

  def testContainersNotCast(self):
    """Containers are no cast targets: an instance passes, and every
    other container, a dict's items and a scalar are refused."""
    for target in (list, tuple, set, frozenset):
      with self.subTest(target=target.__name__):
        value = target((1, 2))
        self.assertIs(typeCast(target, value), value)
        others = ([1, 2], (1, 2), {1, 2}, frozenset([1, 2]), {'a': 1}, 123)
        for other in others:
          if isinstance(other, target):
            continue
          with self.assertRaises(TypeCastException):
            typeCast(target, other)

  def testDictCast(self):
    """Casts to dict. Only other dict-like objects accepted."""
    d = {'a': 1, 'b': 2}
    self.assertEqual(typeCast(dict, d), d)

    class CustomDict(dict):
      pass

    self.assertEqual(typeCast(dict, CustomDict({'x': 10})), {'x': 10})
    with self.assertRaises(TypeCastException):
      typeCast(dict, 123)
    with self.assertRaises(TypeCastException):
      typeCast(dict, [1, 2])

  def testTypeCast(self):
    """Casts to type. Only classes accepted."""
    self.assertIs(typeCast(type, int), int)

    class MyClass:
      pass

    self.assertIs(typeCast(type, MyClass), MyClass)
    with self.assertRaises(TypeCastException):
      typeCast(type, 123)

  def testNoConstructorFallback(self):
    """A class without '__cast_as__' is refused; its constructor is never
    called on the value."""

    class Foo:
      def __init__(self, x):
        raise AssertionError('constructor called')  # pragma: no cover

    with self.assertRaises(TypeCastException):
      typeCast(Foo, 5)
