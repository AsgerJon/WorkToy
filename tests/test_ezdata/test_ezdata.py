"""TestEZData tests the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import randint, sample
from typing import TYPE_CHECKING, Self

from worktoy.desc import AttriBox
from worktoy.ezdata import EZData, BeginFields, EndFields
from worktoy.worktest import WorkTest


class Point3D(EZData):
  """Point3D is a 3D point with x, y, and z coordinates."""

  BeginFields
  x = AttriBox[int](-1)
  y = AttriBox[int](-1)
  z = AttriBox[int](-1)
  EndFields

  if TYPE_CHECKING:
    x: int
    y: int
    z: int

    def __init__(self, *args, **kwargs) -> None:
      """TYPE_CHECKING"""

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


class TestEZData(WorkTest):
  """TestEZData tests the EZData class."""

  def test_class_instantiation_positional(self, ) -> None:
    """Tests if the Point3D class gets instantiated on any number of
    positional arguments. """
    X = [randint(0, 255) for _ in range(10)]
    for i in range(10):
      x = sample(X, i)
      point = Point3D(*x, )
      expected = [*x, -1, -1, -1][:3]
      self.assertEqual((point.x, point.y, point.z), (*expected,))

  def test_class_instantiation_keyword(self) -> None:
    """Tests if the Point3D class gets instantiated on any number of
    keyword arguments. """
    Q = [randint(0, 255) for _ in range(10)]
    for i in range(4):
      q = sample(Q, i)
      p = (*q, -1, -1, -1)
      kwargs = [('x', p[0]), ('y', p[1]), ('z', p[2])][:min(i, 3)]
      kwargs = {k: v for (k, v) in kwargs}
      point = Point3D(**kwargs)
      expected = p[:3]
      self.assertEqual((point.x, point.y, point.z), (*expected,))
