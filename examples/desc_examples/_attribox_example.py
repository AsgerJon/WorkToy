"""The 'attriboxExample' function demonstrates the descriptor protocol
implementation provided by the AttriBox class. This class provides
accessor functions by itself. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy import AttriBox, Field

pi = 3.14159265358979


class PlanePoint:
  """This class represents a point in the plane using instances of
  'AttriBox' to implement x and y coordinates. """

  x = AttriBox[float](0)
  y = AttriBox[float](0)


class Circle:
  """This class represents plane circles using instances of 'AttriBox' to
  implement a center point and a radius. Additionally, the class
  implements an instance of 'Field' to represent the area of the circle.
  The getter function calculates and returns the area. The setter function
  adjusts the radius as appropriate to achieve the given area. This
  advanced accessor functions are not supported by 'AttriBox', but are
  supported by the 'Field' class."""

  center = AttriBox[PlanePoint](PlanePoint())
  radius = AttriBox[float](1)
  area = Field()

  @area.GET
  def _getArea(self) -> float:
    """Getter-function for the area of the circle."""
    return pi * self.radius ** 2

  @area.SET
  def _setArea(self, area: float) -> None:
    """Setter-function for the area of the circle."""
    self.radius = (area / pi) ** 0.5


def attriboxExample() -> None:
  """The 'attriboxExample' function demonstrates how to use the AttriBox
  class."""
  p = PlanePoint()
  print(p.x)  # 0
  print(p.y)  # 0

  c = Circle()
  print(c.center.x)  # 0
  print(c.center.y)  # 0
  print(c.radius)  # 1
  print(c.area)  # 3.141592653589793
  c.radius = 2
  print(c.area)  # 12.566370614359172
  c.area = 50
  print(c.radius)  # 3.989422804014327
