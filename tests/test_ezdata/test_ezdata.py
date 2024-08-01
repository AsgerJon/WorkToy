"""TestEZData tests the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Self
from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.ezdata import EZData, DataMetaclass
from worktoy.text import monoSpace


class Point3D(EZData):
  """Point3D is a 3D point with x, y, and z coordinates."""

  x = AttriBox[int](-1)
  y = AttriBox[int](-1)
  z = AttriBox[int](-1)

  def __str__(self) -> str:
    """String representation"""
    return """(%d, %d, %d)""" % (self.x, self.y, self.z)

  def __repr__(self) -> str:
    """Code representation"""
    return """Point3D(x=%d, y=%d, z=%d)""" % (self.x, self.y, self.z)

  def __abs__(self, ) -> int:
    """Returns the square on the length of the vector from origin to self."""
    return self.x ** 2 + self.y ** 2 + self.z ** 2

  def __mul__(self, other: Self) -> int:
    """Implements the dot product"""
    return self.x * other.x + self.y * other.y + self.z * other.z

  def __matmul__(self, other: Self) -> Self:
    """Implements the cross product"""
    return Point3D(
        self.y * other.z - self.z * other.y,
        self.z * other.x - self.x * other.z,
        self.x * other.y - self.y * other.x
    )

  def __eq__(self, other: Self) -> bool:
    """Equality test for two points"""
    return False if abs(self @ other) else True


class TestEZData(TestCase):
  """TestEZData tests the EZData class."""

  def test_positional_args(self) -> None:
    """Tests that Point3D support any number of positional arguments"""
    point = Point3D()  # Nu arguments
    self.assertEqual(point.x, -1)
    self.assertEqual(point.y, -1)
    self.assertEqual(point.z, -1)
    point = Point3D(1)  # One argument
    self.assertEqual(point.x, 1)
    self.assertEqual(point.y, -1)
    self.assertEqual(point.z, -1)
    point = Point3D(1, 2)  # Two arguments
    self.assertEqual(point.x, 1)
    self.assertEqual(point.y, 2)
    self.assertEqual(point.z, -1)
    point = Point3D(1, 2, 3, )  # Three arguments
    self.assertEqual(point.x, 1)
    self.assertEqual(point.y, 2)
    self.assertEqual(point.z, 3)

  def test_keyword_args(self) -> None:
    """Tests that Point3D support any number of keyword arguments"""
    point = Point3D(x=1)  # One argument
    self.assertEqual(point.x, 1)
    self.assertEqual(point.y, -1)
    self.assertEqual(point.z, -1)
    point = Point3D(x=1, y=2)  # Two arguments
    self.assertEqual(point.x, 1)
    self.assertEqual(point.y, 2)
    self.assertEqual(point.z, -1)
    point = Point3D(x=1, y=2, z=3)  # Three arguments
    self.assertEqual(point.x, 1)
    self.assertEqual(point.y, 2)
    self.assertEqual(point.z, 3)

  def test_errors(self, ) -> None:
    """Tests that EZData correctly raises an error when a subclass tries
    to implement '__init__'."""
    with self.assertRaises(AttributeError) as context:
      class SusData(EZData):
        """This class will attempt to implement '__init__', which should
        raise an 'AttributeError'. """

        def __init__(self, *__, **_) -> None:
          EZData.__init__(self)  # keeps pycharm from complaining lol
          
    expectedMsg = monoSpace("""Reimplementing __init__ is not allowed for 
      EZData classes!""").lower()
    self.assertEqual(expectedMsg, context.exception.__str__().lower())

  def test_class_access(self, ) -> None:
    """Tests that the AttriBox instances are accessible from the class."""
    self.assertIs(Point3D.x.getFieldClass(), int)
    self.assertIs(Point3D.y.getFieldClass(), int)
    self.assertIs(Point3D.z.getFieldClass(), int)
