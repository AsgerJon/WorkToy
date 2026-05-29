"""
Point2D subclasses 'EZData' and provides a simple two-dimensional point
implementation with 'x' and 'y' coordinates as 'float' fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from worktoy.ezdata import EZData, EZField

if TYPE_CHECKING:  # pragma: no cover
  from typing import Union, Self
  from types import NotImplementedType as NotImpType
else:
  NotImpType = type(NotImplemented)


class Point2D(EZData):
  """
  Point2D subclasses 'EZData' and provides a simple two-dimensional point
  implementation with 'x' and 'y' coordinates as 'float' fields.
  """

  x = EZField[float](0.0)
  y = EZField[float](0.0)

  def __abs__(self, ) -> float:
    """Returns the distance of the point from the origin."""
    return (self.x ** 2 + self.y ** 2) ** 0.5

  def __bool__(self, ) -> bool:
    return True if abs(self) > sys.float_info.epsilon else False

  def __neg__(self, ) -> Self:
    """Returns a new 'Point2D' with the coordinates negated."""
    cls = type(self)
    return cls(-self.x, -self.y)

  def __pos__(self, ) -> Self:
    """Returns a new 'Point2D' with the coordinates unchanged."""
    cls = type(self)
    return cls(+self.x, +self.y)

  def __add__(self, other: Self) -> Union[NotImpType, Self]:
    cls = type(self)
    if not isinstance(other, cls):
      return NotImplemented
    return cls(self.x + other.x, self.y + other.y)

  def __sub__(self, other: Self) -> Union[NotImpType, Self]:
    cls = type(self)
    if not isinstance(other, cls):
      return NotImplemented
    return self + (-other)

  def __matmul__(self, other: Self) -> Union[NotImpType, float, Self]:
    cls = type(self)
    if isinstance(other, cls):
      vector = self - other
      if TYPE_CHECKING:  # pragma: no cover
        assert isinstance(vector, Point2D)
      return abs(vector)
    if isinstance(other, float):
      return self * other
    return NotImplemented

  def __mul__(self, scalar: float) -> Union[NotImpType, float, Self]:
    """Returns a new 'Point2D' with the coordinates multiplied by
    'scalar'."""
    cls = type(self)
    if isinstance(scalar, (int, float)):
      return cls(self.x * scalar, self.y * scalar)
    if isinstance(scalar, Point2D):
      return self.x * scalar.x + self.y * scalar.y
    return NotImplemented

  def __rmul__(self, scalar: float) -> Union[NotImpType, float, Self]:
    """Returns a new 'Point2D' with the coordinates multiplied by
    'scalar'."""
    return self * scalar
