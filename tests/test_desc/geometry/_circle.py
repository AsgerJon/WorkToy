"""
Circle encapsulates the collection of points equidistant from a point
'center' by a distance 'radius'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import random
from typing import TYPE_CHECKING
import sys

from worktoy.desc import AttriBox, Field
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.utilities.mathematics import pi
from . import Point2D

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Iterator

eps = sys.float_info.epsilon


class Circle(BaseObject):
  """Circle is a simple circle class for testing purposes."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  center = AttriBox[Point2D]()
  radius = AttriBox[float](1.0)
  area = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @area.GET
  def _getArea(self) -> float:
    return pi * (self.radius ** 2)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __contains__(self, point: Point2D) -> bool:
    if isinstance(point, Point2D):
      return True if self.center.distance(point) < self.radius else False
    return False

  def __str__(self, ) -> str:
    infoSpec = """<%s: (x-%.3f) ** 2 + (y-%.3f) ** 2 = %.3f ** 2>"""
    clsName = type(self).__name__
    x0, y0, r = self.center.x, self.center.y, self.radius
    info = infoSpec % (clsName, x0, y0, r)
    return info

  def __repr__(self, ) -> str:
    infoSpec = """%s(%s, %.3f)"""
    clsName = type(self).__name__
    centerStr = repr(self.center)
    r = self.radius
    info = infoSpec % (clsName, centerStr, r)
    return info

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(Point2D, float)
  def __init__(self, center: Point2D, radius: float) -> None:
    self.center = center
    self.radius = radius

  @overload(float, float, float)
  def __init__(self, x: float, y: float, radius: float) -> None:
    self.center = Point2D(x, y)
    self.radius = radius

  @overload(Point2D)
  def __init__(self, center: Point2D) -> None:
    self.center = center

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.center = Point2D(x, y)

  @overload(float)
  def __init__(self, radius: float) -> None:
    self.radius = radius

  @overload()
  def __init__(self) -> None:
    pass

  @classmethod
  def rand(cls, *args, ) -> Self:
    a, b, *_ = (*args, 0.0, 1.0)
    minVal, maxVal = min(a, b), max(a, b)
    center = Point2D.rand(minVal, maxVal)
    minVal = max(0.0, minVal)
    radius = random() * (maxVal - minVal) + minVal
    return cls(center, radius)

  @classmethod
  def rands(cls, n: int, *args, ) -> Iterator[Self]:
    for _ in range(n):
      yield cls.rand(*args)
