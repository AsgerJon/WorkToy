"""TestEZData tests EZData dataclasses."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import typeCast, overload, THIS
from worktoy.ezdata import EZData
from worktoy.waitaminute import NumCastException

try:
  from typing import Self
except ImportError:
  Self = object


class PlanePoint(EZData):
  """Represents a point in the plane"""

  x = 0
  y = 0

  @overload(int, int)
  def __init__(self, *args) -> None:
    self.x, self.y = args

  @overload(float, float)
  def __init__(self, *args) -> None:
    self.x, self.y = args

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.x, self.y = z.real, z.imag

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.x, self.y = other.x, other.y

  @overload()
  def __init__(self) -> None:
    pass

  @overload.fallback
  def __init__(self, *args, **kwargs) -> None:
    if len(args) == 2:
      _x = float(args[0])
      _y = float(args[1])
      self.__init__(_x, _y)
    else:
      self.__init__()


class TestEZData(TestCase):
  """TestEZData tests EZData dataclasses."""

  def test_init_normal(self) -> None:
    """Testing that the class initializes correctly when receiving
    arguments of supported type signatures. """

    # p1 = PlanePoint(1, 2)
    # p2 = PlanePoint()
    # p3 = PlanePoint(3.0, 4.0)
    # p4 = PlanePoint(3 + 4j)
    # p5 = PlanePoint(p4)
    # p6 = PlanePoint('1', '2')
    #
    # self.assertEqual(p1.x, 1)
    # self.assertEqual(p1.y, 2)
    # self.assertEqual(p2.x, 0)
    # self.assertEqual(p2.y, 0)
    # self.assertEqual(p3.x, 3.0)
    # self.assertEqual(p3.y, 4.0)
    # self.assertEqual(p4.x, 3.0)
    # self.assertEqual(p4.y, 4.0)
    # self.assertEqual(p5.x, 3.0)
    # self.assertEqual(p5.y, 4.0)
    # self.assertEqual(p6.x, 1)
    # self.assertEqual(p6.y, 2)
