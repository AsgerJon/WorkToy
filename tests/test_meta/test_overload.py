"""TestOverload tests the overloading functionality of the BaseMetaclass.
The tests focus on the color class defined above. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.base import BaseObject, overload
from worktoy.desc import AttriBox

try:
  from typing import Callable
except ImportError:
  Callable = object


class Point2D(BaseObject):
  """Plane point"""

  x = AttriBox[float](0)
  y = AttriBox[float](0)

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

  @overload(float)
  def __init__(self, x: float) -> None:
    self.x = x
    self.y = 0

  @overload()
  def __init__(self) -> None:
    self.x = 0
    self.y = 0


class TestOverload(TestCase):
  """TestOverload tests the overloading functionality of the BaseMetaclass.
  The tests focus on the color class defined above. """

  def setUp(self) -> None:
    """Sets up each test"""
    self.point2Dxy = Point2D(69, 420)
    self.point2Dx = Point2D(69)
    self.point2D = Point2D()

  def test_init(self) -> None:
    """Testing that points have initialized correctly"""
    self.assertEqual(self.point2Dxy.x, 69)
    self.assertEqual(self.point2Dxy.y, 420)
    self.assertEqual(self.point2Dx.x, 69)
    self.assertEqual(self.point2Dx.y, 0)
    self.assertEqual(self.point2D.x, 0)
    self.assertEqual(self.point2D.y, 0)
