"""The 'fieldExample' function demonstrates the descriptor protocol
implementation provided by the Field class. This class requires that the
owning class implements accessor functions. These must be indicated by the
use of the 'GET', 'SET' and 'DELETE' decorators. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy import typeCast, maybe
from depr.desc import Field

pi = 3.14159265358979


class PlanePoint:
  """Represents are point in the plane using instances of 'Field' to
  implement x and y coordinates."""

  __fallback_x__ = 0
  __fallback_y__ = 0
  __x_value__ = None
  __y_value__ = None

  x = Field()
  y = Field()

  @x.GET
  def _getX(self, ) -> float:
    """Getter-function for x-value"""
    return typeCast(maybe(self.__x_value__, self.__fallback_x__), float)

  @x.SET
  def _setX(self, xValue: float) -> None:
    """Setter-function for x-value"""
    self.__x_value__ = typeCast(xValue, float)

  @y.GET
  def _getY(self) -> float:
    """Getter-function for y-value"""
    return typeCast(maybe(self.__y_value__, self.__fallback_y__), float)

  @y.SET
  def _setY(self, yValue: float) -> None:
    """Setter-function for y-value"""
    self.__y_value__ = typeCast(yValue, float)


class Circle:
  """Represents a circle in the plane using instances of 'Field' to
  implement a center point and a radius. Additionally, the class
  implements an instance of 'Field' to represent the area of the circle.
  The getter function calculates and returns the area. The setter function
  adjusts the radius as appropriate to achieve the given area."""

  __fallback_center__ = PlanePoint()
  __center_point__ = None
  __fallback_radius__ = 1
  __radius_value__ = None

  center = Field()
  radius = Field()
  area = Field()

  @center.GET
  def _getCenter(self) -> PlanePoint:
    """Getter-function for center-point"""
    return maybe(self.__center_point__, self.__fallback_center__)

  @center.SET
  def _setCenter(self, centerPoint: PlanePoint) -> None:
    """Setter-function for center-point"""
    self.__center_point__ = centerPoint

  @radius.GET
  def _getRadius(self) -> float:
    """Getter-function for radius-value"""
    return typeCast(maybe(self.__radius_value__, self.__fallback_radius__),
                    float)

  @radius.SET
  def _setRadius(self, radiusValue: float) -> None:
    """Setter-function for radius-value"""
    self.__radius_value__ = typeCast(radiusValue, float)

  @area.GET
  def _getArea(self) -> float:
    """Getter-function for area-value"""
    radius = self.radius
    return pi * radius ** 2

  @area.SET
  def _setArea(self, areaValue: float) -> None:
    """Setter-function for area-value"""
    radius = (areaValue / pi) ** 0.5
    self.radius = radius


def fieldExample() -> None:
  """The 'fieldExample' function demonstrates the descriptor protocol
  implementation provided by the Field class. """
  point = PlanePoint()
  print(point.x)  # 0
  print(point.y)  # 0
  point.x = 3
  point.y = 4
  print(point.x)  # 3.0
  print(point.y)  # 4.0

  circle = Circle()
  print(circle.center.x)  # 0
  print(circle.center.y)  # 0
  print(circle.radius)  # 1
  print(circle.area)  # 3.141592653589793
  circle.radius = 2
  print(circle.area)  # 12.566370614359172
  circle.area = 50
  print(circle.radius)  # 3.989422804014327
