"""
Circle subclasses 'EZData' and provides a keyword-only subclass
encapsulating the collection of 'Point2D' objects equidistant from a
shared 'Point2D' object.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from math import cos, sin

from worktoy.desc import Field
from worktoy.ezdata import EZData, EZField
from . import Point2D

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Circle(EZData, kwOnly=True):
  """
  Circle subclasses 'EZData' and provides a keyword-only subclass
  encapsulating the collection of 'Point2D' objects equidistant from a
  shared 'Point2D' object.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Attributes

  center = EZField[Point2D](0, 0)
  radius = EZField[float](1)

  #  Virtual Variables
  area: Field[float] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __contains__(self, item: Any) -> bool:
    """
    This method checks if a given 'item' is contained within the circle.
    If 'item' is an instance of 'Point2D', it checks if the distance from
    the circle's center to the point is less than the radius. If 'item' is
    an instance of 'Circle', it must be entirely contained within the
    current circle.
    """
    if isinstance(item, Point2D):
      return True if self.center @ item < self.radius else False
    cls = type(self)
    if isinstance(item, cls):
      dc = self.center @ item.center
      return True if dc + item.radius < self.radius else False
    return False

  def __getitem__(self, angle: float) -> Point2D:
    """
    This method returns a 'Point2D' on the circumference of the circle at a
    given 'angle' in radians.
    """
    return self.center + self.radius * Point2D(cos(angle), sin(angle))
