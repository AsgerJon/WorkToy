"""
TestEZUmbrella covers the more esoteric lines of code in the ezdata module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import trust
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.meta import ReservedName
from . import EZTest
from worktoy.ezdata import EZData, EZSlot

if TYPE_CHECKING:  # pragma: no cover
  pass


class RGB(EZData):
  red: int
  green: int
  blue: int


class TestEZUmbrella(EZTest):
  """
  TestEZUmbrella covers the more esoteric lines of code in the ezdata module.
  """

  def test_ez_slot(self) -> None:
    """
    Test that EZData classes can be created with slots.
    """
    ez = EZSlot('breh')
    ez.__type_value__ = None
    with self.assertRaises(AttributeError):
      _ = ez.typeValue
    ez.__deferred_type__ = 'int'
    self.assertEqual(ez._getDeferredType(), 'int')
    ez = EZSlot('breh')
    self.assertIsNone(ez._getDeferredType())
    setattr(ez, '__type_value__', int)
    self.assertIs(ez.typeValue, int)
    self.assertNotEqual(ez, 'lol')
    self.assertEqual(str(ez), repr(ez))

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
