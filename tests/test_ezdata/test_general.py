"""
These tests are made by chat-GPT 4.1
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import EZTest
from worktoy.ezdata import EZData

if TYPE_CHECKING:  # pragma: no cover
  pass


class Point2D(EZData):
  """
  Point2D represents a 2D point with integer coordinates.
  """
  x = 0
  y = 0


class Rectangle(EZData):
  """
  Rectangle represents a rectangle with position and size.
  """
  x = 1
  y = 2
  width = 3
  height = 4


class MixedTypes(EZData):
  """
  MixedTypes accepts an int, a float, and a string with defaults.
  """
  i = 1
  f = 2.0
  s = 'abc'


class NoFields(EZData):
  """
  NoFields demonstrates the empty case.
  """
  pass


class BoolFields(EZData):
  """
  BoolFields demonstrates booleans.
  """
  yes = True
  no = False


class TestEZDataRepr(EZTest):
  """Tests repr format for EZData subclasses."""

  def testPoint2DRepr(self) -> None:
    """repr(Point2D) returns valid instantiating code."""
    pt = Point2D(7, 9)
    code = repr(pt)
    self.assertEqual(code, "Point2D(7, 9)")

  def testRectangleRepr(self) -> None:
    """repr(Rectangle) returns valid instantiating code."""
    rect = Rectangle(5, 6, 7, 8)
    code = repr(rect)
    self.assertEqual(code, "Rectangle(5, 6, 7, 8)")

  def testRectangleDefaultRepr(self) -> None:
    """Default Rectangle gives correct repr."""
    rect = Rectangle()
    code = repr(rect)
    self.assertEqual(code, "Rectangle(1, 2, 3, 4)")

  def testReprRoundTrip(self) -> None:
    """repr() output can be eval'd to recreate an equal object."""
    pt = Point2D(2, 3)
    pt2 = eval(repr(pt))
    self.assertEqual(pt, pt2)
    rect = Rectangle(8, 9, 10, 11)
    rect2 = eval(repr(rect))
    self.assertEqual(rect, rect2)

  def testMixedTypesDefaultRepr(self) -> None:
    """repr(MixedTypes()) gives correct code string."""
    obj = MixedTypes()
    self.assertEqual(repr(obj), "MixedTypes(1, 2.0, 'abc')")

  def testMixedTypesCustomRepr(self) -> None:
    """repr with custom values and types."""
    obj = MixedTypes(99, 4.5, 'xyz')
    self.assertEqual(repr(obj), "MixedTypes(99, 4.5, 'xyz')")
    obj2 = MixedTypes(i=-5, f=0.1, s='')
    self.assertEqual(repr(obj2), "MixedTypes(-5, 0.1, '')")

  def testNoFieldsRepr(self) -> None:
    """repr(NoFields()) is simple and callable."""
    obj = NoFields()
    self.assertEqual(repr(obj), "NoFields()")
    obj2 = eval(repr(obj))
    self.assertIsInstance(obj2, NoFields)

  def testBoolFieldsRepr(self) -> None:
    """repr(BoolFields) returns correct boolean values."""
    obj = BoolFields()
    self.assertEqual(repr(obj), "BoolFields(True, False)")
    obj2 = BoolFields(False, True)
    self.assertEqual(repr(obj2), "BoolFields(False, True)")

  def testPartialKeywordInitRepr(self) -> None:
    """Partial initialization fills remaining defaults in order."""
    obj = MixedTypes(f=1.23)
    self.assertEqual(obj.i, 1)
    self.assertEqual(obj.f, 1.23)
    self.assertEqual(obj.s, 'abc')
    self.assertEqual(repr(obj), """MixedTypes(1, 1.23, 'abc')""")

  def testStringEscaping(self) -> None:
    """repr properly escapes string quotes."""
    obj = MixedTypes(2, 3.0, 'hello')
    self.assertEqual(repr(obj), """MixedTypes(2, 3.0, 'hello')""")
