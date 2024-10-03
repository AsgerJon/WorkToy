"""TestCLSOverload tests if Overload descriptors defined entirely in class
bodies work correctly."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.meta import Overload
from worktoy.base import BaseObject


class Point(BaseObject):
  """Plane point"""

  distance = Overload()
  __init__ = Overload()

  x = AttriBox[float]()
  y = AttriBox[float]()

  @__init__.overload(complex)
  def _(self, *args) -> None:
    """Constructor for the Point class."""
    self.__init__(int(args[0].real), int(args[0].imag))

  @__init__.overload(float, float)
  def _(self, *args) -> None:
    """Constructor for the Point class."""
    self.x = args[0]
    self.y = args[1]

  @distance.overload()
  def __(self, ) -> float:
    return (self.x - 0) ** 2 + (self.y - 0) ** 2

  @distance.overload(complex)
  def __(self, z: complex) -> float:
    return (self.x - z.real) ** 2 + (self.y - z.imag) ** 2

  @distance.overload(float, float)
  def __(self, x: float, y: float) -> float:
    return (self.x - x) ** 2 + (self.y - y) ** 2


class TestCLSOverload(TestCase):
  """TestCLSOverload tests if Overload descriptors defined entirely in class
  bodies work correctly. """

  def setUp(self) -> None:
    """Sets up each test"""
    self.intPoint = Point(3, 4)
    self.complexPoint = Point(3 + 4j)
    self.point = Point(5., 12.)

  def test_init(self) -> None:
    """Testing that points have initialized correctly"""
    self.assertEqual(self.intPoint.x, 3)
    self.assertEqual(self.intPoint.y, 4)
    self.assertEqual(self.complexPoint.x, 3)
    self.assertEqual(self.complexPoint.y, 4)

  def test_distance(self) -> None:
    """Testing that distance measures correctly"""
    self.assertEqual(self.intPoint.distance(), 25.0)
    self.assertEqual(self.complexPoint.distance(), 25.0)
    self.assertEqual(self.point.distance(), 169.0)
    self.assertEqual(self.point.distance(8 + 16 * 1j), 25)
    self.assertEqual(self.point.distance(5, 12), 0.0)
    self.assertEqual(self.point.distance(10, 24), 13 * 13)
