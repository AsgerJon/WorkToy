"""
TestAttriBox tests specific functionality of the 'AttriBox' descriptor not
covered by the contextual tests in 'DescTest'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
import sys

from worktoy.desc import AttriBox
from worktoy.waitaminute import TypeException
from . import DescTest
from .geometry import Circle, Point2D

if TYPE_CHECKING:  # pragma: no cover
  pass

eps = sys.float_info.epsilon


class TestAttriBox(DescTest):
  """
  TestAttriBox tests specific functionality of the 'AttriBox' descriptor not
  covered by the contextual tests in 'DescTest'.
  """

  def test_init(self) -> None:
    """
    Testing that 'AttriBox' descriptors actively instantiate when owning
    classes instantiate.
    """
    points = Point2D.rands(69, -0.1337, 80085)
    for point in points:
      self.assertIsInstance(point.x, float)
      self.assertIsInstance(point.y, float)
    circles = Circle.rands(69, -0.1337, 80085)
    for circle in circles:
      self.assertIsInstance(circle.radius, float)
      self.assertIsInstance(circle.center, Point2D)

  def test_good_set(self, ) -> None:
    """
    Testing setting functions as intended.
    """
    point2D = Point2D(69, 420)
    self.assertEqual(point2D.x, 69)
    self.assertEqual(point2D.y, 420)
    point2D.x = -1337
    point2D.y = 80085
    self.assertEqual(point2D.x, -1337)
    self.assertEqual(point2D.y, 80085)

  def test_bad_set(self, ) -> None:
    """
    Testing that setting to incompatible types raises appropriate errors.
    """
    point2D = Point2D(69, 420)
    self.assertEqual(point2D.x, 69)
    self.assertEqual(point2D.y, 420)

    def _1337() -> None:
      """Imma a float, trust me bro!"""
      pass

    with self.assertRaises(TypeException) as context:
      point2D.x = _1337() or _1337
    e = context.exception
    self.assertEqual(e.varName, 'value')
    self.assertEqual(e.actualObject, _1337)
    self.assertEqual(e.actualType, type(_1337))
    self.assertEqual(e.expectedTypes, (float,))

  def test_good_delete(self, ) -> None:
    """
    Testing that deleting attributes works as intended.
    """
    point2D = Point2D(69, 420)
    self.assertEqual(point2D.x, 69)
    self.assertEqual(point2D.y, 420)
    del point2D.x
    del point2D.y
    with self.assertRaises(AttributeError) as context:
      _ = point2D.x
    e = context.exception
    self.assertIn(self.attrErrTrace, str(e))
    with self.assertRaises(AttributeError) as context:
      _ = point2D.y
    e = context.exception
    self.assertIn(self.attrErrTrace, str(e))

  def test_bad_delete(self, ) -> None:
    """
    Testing that deleting attributes that are not set raises appropriate
    errors.
    """
    point2D = Point2D(69, 420)
    self.assertEqual(point2D.x, 69)
    self.assertEqual(point2D.y, 420)
    del point2D.x
    del point2D.y
    with self.assertRaises(AttributeError) as context:
      del point2D.x
    e = context.exception
    self.assertEqual('x', str(e))
    with self.assertRaises(AttributeError) as context:
      del point2D.y
    e = context.exception
    self.assertEqual('y', str(e))

  def test_gymnastics(self) -> None:
    """
    Covering certain edge cases.
    """

    class Bar:
      foo = AttriBox[int]()

    bar = Bar()
    setattr(Bar.foo, '__context_instance__', bar)
    setattr(Bar.foo, '__context_owner__', Bar)
    with self.assertRaises(RecursionError):
      Bar.foo.__instance_get__(_recursion=True)
    with self.assertRaises(RecursionError):
      Bar.foo.__instance_set__('baz', _recursion=True)
