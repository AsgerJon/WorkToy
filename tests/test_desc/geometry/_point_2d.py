"""
Point2D encapsulates a point in a two-dimensional Cartesian coordinate
system.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import random
from typing import TYPE_CHECKING
import sys

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Iterator

eps = sys.float_info.epsilon


class Point2D(BaseObject):
  """Point2D is a simple 2D point class for testing purposes."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.x = other.x
    self.y = other.y

  @overload()
  def __init__(self) -> None:
    pass

  @classmethod
  def rand(cls, *args) -> Self:
    a, b, *_ = (*args, 0.0, 1.0)
    minVal, maxVal = min(a, b), max(a, b)
    x = random() * (maxVal - minVal) + minVal
    y = random() * (maxVal - minVal) + minVal
    return cls(x, y)

  @classmethod
  def rands(cls, n: int, *args) -> Iterator[Self]:
    for _ in range(n):
      yield cls.rand(*args)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __neg__(self) -> Self:
    cls = type(self)
    return cls(-self.x, -self.y)

  def __add__(self, other: Self) -> Self:
    cls = type(self)
    if isinstance(other, cls):
      return cls(self.x + other.x, self.y + other.y)
    try:
      otherFloat = float(other)
    except (TypeError, ValueError):
      return NotImplemented
    else:
      return self + cls(otherFloat, otherFloat)

  def __sub__(self, other: Self) -> Self:
    cls = type(self)
    if isinstance(other, cls):
      return self + (-other)
    try:
      otherFloat = float(other)
    except (TypeError, ValueError):
      return NotImplemented
    else:
      return self - cls(otherFloat, otherFloat)

  def __complex__(self, ) -> complex:
    return self.x + self.y * 1j

  def __abs__(self) -> float:
    return (self.x ** 2 + self.y ** 2) ** 0.5

  def __bool__(self, ) -> bool:
    return True if abs(self) > eps else False

  def __eq__(self, other: Self) -> bool:
    cls = type(self)
    if isinstance(other, cls):
      return False if self - other else True
    return NotImplemented

  def __str__(self) -> str:
    infoSpec = """<%s: x=%.3f, y=%.3f>"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.x, self.y)
    return info

  def __repr__(self, ) -> str:
    infoSpec = """%s(%.3f, %.3f)"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.x, self.y)
    return info

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def distance(self, other: Self) -> float:
    """Calculate the Euclidean distance to another Point2D."""
    dx = self.x - other.x
    dy = self.y - other.y
    return (dx ** 2 + dy ** 2) ** 0.5
