"""
Point2DFix subclasses 'Point2D' and replaces the 'AttriBox' descriptors
with 'FixBox' descriptors to create immutable 2D points.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import FixBox
from . import Point2D

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Point2DFix(Point2D):
  """
  Point2DFix subclasses 'Point2D' and replaces the 'AttriBox' descriptors
  with 'FixBox' descriptors to create immutable 2D points.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  x = FixBox[float](0.0)
  y = FixBox[float](0.0)

  @classmethod
  def __cast_as__(cls, value: Any) -> Any:
    """A 'Point2D' of any kind casts to the immutable point at the same
    place, which is how a 'Circle' built on 'Point2D' fills a
    'FixBox[Point2DFix]'; anything else is refused."""
    if isinstance(value, Point2D):
      return cls(value.x, value.y)
    return NotImplemented
