"""TestField tests the EmptyField class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from unittest import TestCase

from worktoy.desc import Field
from worktoy.text import typeMsg


class Point3D:
  """Point3D is a simple 3D point class."""

  __x_value__ = None
  __y_value__ = None
  __z_value__ = None

  x = Field()  # get, set and delete supported
  y = Field()  # get only supported
  z = Field()  # not even get supported

  @x.GET
  def _getX(self) -> float:
    """Return the x coordinate."""
    if self.__x_value__ is None:
      e = """The x coordinate has not been assigned!"""
      raise AttributeError(e)
    if isinstance(self.__x_value__, int):
      return float(self.__x_value__)
    if isinstance(self.__x_value__, float):
      return self.__x_value__
    e = typeMsg('__x_value__', self.__x_value__, float)
    raise TypeError(e)

  @x.SET
  def _setX(self, x: float) -> None:
    """Set the x coordinate."""
    if not isinstance(x, (int, float)):
      e = typeMsg('x', x, float)
      raise TypeError(e)
    self.__x_value__ = float(x)

  @y.GET
  def _getY(self) -> float:
    """Return the y coordinate."""
    if self.__y_value__ is None:
      e = """The y coordinate has not been assigned!"""
      raise AttributeError(e)
    if isinstance(self.__y_value__, int):
      return float(self.__y_value__)
    if isinstance(self.__y_value__, float):
      return self.__y_value__
    e = typeMsg('__y_value__', self.__y_value__, float)
    raise TypeError(e)

  def __init__(self, *args) -> None:
    """Constructor for the Point3D class."""
    for arg in args:
      if isinstance(arg, int):
        arg = float(arg)
      if isinstance(arg, float):
        if self.__x_value__ is None:
          self.__x_value__ = arg
        elif self.__y_value__ is None:
          self.__y_value__ = arg
          break
    else:
      if self.__x_value__ is None:
        self.__x_value__, self.__y_value__ = 69., 420.
      elif self.__y_value__ is None:
        self.__y_value__ = 420.


class TestField(TestCase):
  """TestField tests the EmptyField class."""

  def setUp(self, ) -> None:
    """Sets up each test method."""
    self.point = Point3D(69, 420)

  def test_getters(self) -> None:
    """Tests the getter functions"""
    self.assertEqual(self.point.x, 69.)
    self.assertEqual(self.point.y, 420.)

  def test_setters(self) -> None:
    """Tests the setter functions"""
    roll = float(randint(0, 255))
    self.point.x = roll
    self.assertEqual(self.point.x, roll)

  def test_errors(self) -> None:
    """Tests the error handling"""
    with self.assertRaises(TypeError):
      self.point.y = 1337
    with self.assertRaises(TypeError):
      del self.point.x
