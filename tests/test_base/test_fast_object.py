"""TestFastObject tests the FastObject class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.base import FastObject, overload
from worktoy.desc import AttriBox


class SpacePoint(FastObject):
  """SomeClass is a class that inherits from FastObject."""

  x = AttriBox[float](0)
  y = AttriBox[float](0)
  z = AttriBox[float](0)

  @overload(float, float, float)
  def __init__(self, x: float, y: float, z: float) -> None:
    self.x = x
    self.y = y
    self.z = z

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.__init__(x, y, 0)

  @overload(float)
  def __init__(self, x: float) -> None:
    self.__init__(x, 0, 0)

  @overload()
  def __init__(self) -> None:
    self.__init__(0, 0, 0)


class TestFastObject(TestCase):
  """TestFastObject tests the FastObject class. """

  def test_positional_args(self) -> None:
    """Tests that SpacePoint support any number of positional arguments"""
    point = SpacePoint()  # No arguments
    self.assertEqual(point.x, 0)
    self.assertEqual(point.y, 0)
    self.assertEqual(point.z, 0)

    point = SpacePoint(1)  # One argument
    self.assertEqual(point.x, 1)
    self.assertEqual(point.y, 0)
    self.assertEqual(point.z, 0)

    point = SpacePoint(1, 2)  # Two arguments
    self.assertEqual(point.x, 1)
    self.assertEqual(point.y, 2)
    self.assertEqual(point.z, 0)

    point = SpacePoint(1, 2, 3)  # Three arguments
    self.assertEqual(point.x, 1)
    self.assertEqual(point.y, 2)
    self.assertEqual(point.z, 3)
