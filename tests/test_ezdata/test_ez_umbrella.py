"""
TestEZUmbrella covers the more esoteric lines of code in the ezdata module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute import TypeException
from worktoy.waitaminute.meta import ReservedName
from . import EZTest
from worktoy.ezdata import EZData, EZSlot, trust

if TYPE_CHECKING:  # pragma: no cover
  pass


class RGB(EZData):
  red = 255
  green = 255
  blue = 255


class TestEZUmbrella(EZTest):
  """
  TestEZUmbrella covers the more esoteric lines of code in the ezdata module.
  """

  def test_ez_struct(self) -> None:
    """
    Test that EZData classes can be created with slots.
    """

    class Foo(EZData):
      x = 0
      y = 1
      note = 'lol'

      @trust
      def __init__(self, *_) -> None:
        """ignored"""

      def __str__(self) -> str:
        infoSpec = """%s(%s, %s)"""
        return infoSpec % (self.__class__.__name__, self.x, self.y)

      __repr__ = __str__

    foo = Foo(None)
    self.assertEqual(str(foo), repr(foo))
    with self.assertRaises(TypeException) as context:
      _ = Foo(lambda: None, 69)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, 'arg')
    self.assertEqual(e.actualType, type(lambda: None))
    self.assertEqual(e.expectedTypes, (int,))

    with self.assertRaises(TypeException) as context:
      _ = Foo(69, 420, lambda: None, 69)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    foo2 = Foo(breh=69, )

    with self.assertRaises(ValueError):
      foo3 = Foo(x='sixty-nine')

    foo4 = Foo('69', '420', 'test')

    with self.assertRaises(TypeException) as context:
      foo5 = Foo(69, 420, note=object)
    e = context.exception
    self.assertEqual(str(e), repr(e))

    foo6 = Foo(69, y='420', note=str(object))

    with self.assertRaises(ReservedName) as context:
      class Trololololo(EZData):
        def __init__(self, *_) -> None:
          """ignored"""
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.resName, '__init__')

  def test_get_item_negative_indices(self) -> None:
    """
    Testing negative indices in __getitem__
    """

    class Point(EZData):
      x = 69
      y = 420
      z = 1337

    #  would have used Point()[-1 - 1337 * 3] but despite being correct,
    #  raises RecursionError, as it requires more than 1000 recursions.
    #  The fun police wins again.
    self.assertEqual(Point()[-1 - 420 * 3], 1337)
    self.assertEqual(Point()[-2 - 420 * 3], 420)
    self.assertEqual(Point()[-69 * 3], 69)

  def test_set_item_negative_indices(self) -> None:
    """
    Testing negative indices in __setitem__
    """

    class Point3D(EZData):
      x = 0
      y = 0
      z = 0

    point = Point3D()
    self.assertEqual(point.x, 0)
    self.assertEqual(point.y, 0)
    self.assertEqual(point.z, 0)
    point[-1 - 3] = 420
    point[-2 - 69 * 3] = 69
    point[-420 * 3] = 1
    self.assertEqual(point.x, 1)
    self.assertEqual(point.y, 69)
    self.assertEqual(point.z, 420)

  def test_ez_slot(self) -> None:
    """
    Test that EZSlot classes can be created with slots.
    """

    ez = EZSlot('breh')
    setattr(ez, '__type_value__', int)
    self.assertNotEqual(ez, object)
    self.assertEqual(str(ez), repr(ez))
