"""TestEmptyField tests the EmptyField class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from worktoy.desc import EmptyField
from worktoy.text import typeMsg, monoSpace
from worktoy.worktest import WorkTest


class Point3D:
  """Point3D is a simple 3D point class."""

  __x_value__ = None
  __y_value__ = None
  __z_value__ = None

  x = EmptyField()  # get, set and delete supported
  y = EmptyField()  # get only supported
  z = EmptyField()  # not even get supported

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

  @x.DELETE
  def _delX(self) -> None:
    """Delete the x coordinate."""
    if self.__x_value__ is None:
      e = """The x coordinate has not been assigned!"""
      raise AttributeError(e)
    del self.__x_value__

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
    self.__class__.z.__deleter_name__ = 'yolo'
    setattr(self.__class__, 'yolo', 'LMAO')


class TestEmptyField(WorkTest):
  """TestEmptyField tests the EmptyField class."""

  def setUp(self, ) -> None:
    """Sets up each test method."""
    self.point = Point3D(69, 420)

  def test_instance(self) -> None:
    """Tests the accessor functions"""
    self.assertEqual(self.point.x, 69)
    self.point.x = 1337
    self.assertEqual(self.point.x, 1337)
    del self.point.x
    self.assertRaises(AttributeError, lambda: self.point.x)
    self.assertEqual(self.point.y, 420)
    with self.assertRaises(AttributeError, ) as context:
      self.point.y = 69
    actual = str(context.exception)
    expected = "The field instance at name: 'y' does not have a setter!"
    self.assertEqual(actual, expected)
    with self.assertRaises(AttributeError, ) as context:
      del self.point.y
    actual = str(context.exception)
    expected = "The field instance at name: 'y' does not have a deleter!"
    self.assertEqual(actual, expected)
    with self.assertRaises(AttributeError) as context:
      print(self.point.z)
    actual = str(context.exception)
    expected = "The field instance at name: 'z' does not have a getter!"
    self.assertEqual(actual, expected)
    with self.assertRaises(AttributeError) as context:
      self.point.z = 69
    actual = str(context.exception)
    expected = "The field instance at name: 'z' does not have a setter!"
    self.assertEqual(actual, expected)
    with self.assertRaises(TypeError) as context:
      del self.point.z
    actual = str(context.exception)
    expected = typeMsg('deleter', 'LMAO', Callable)
    self.assertEqual(actual, expected)
