"""
PlanePoint provides a point in two-dimensional space using cartesian
coordinates implemented with 'AttriBox'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attr import AttriBox
from worktoy.mcls import BaseObject
from worktoy.static import overload
from worktoy.static.zeroton import THIS
from worktoy.text import stringList

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self


class PlanePoint(BaseObject):
  """
  PlanePoint provides a point in two-dimensional space using cartesian
  coordinates implemented with 'AttriBox'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float, float)
  def __init__(self, x: float, y: float, **kwargs) -> None:
    """
    Initialize the PlanePoint with x and y coordinates.

    :param x: The x-coordinate of the point.
    :param y: The y-coordinate of the point.
    """
    self.x = x
    self.y = y
    if kwargs:
      self.__init__(**kwargs)

  @overload(THIS)
  def __init__(self, other: Self, **kwargs) -> None:
    """
    Initialize the PlanePoint with another PlanePoint.

    :param other: Another PlanePoint instance.
    """
    self.__init__(other.x, other.y)
    if kwargs:
      self.__init__(**kwargs)

  @overload(complex)
  def __init__(self, z: complex, **kwargs) -> None:
    """
    Initialize the PlanePoint with a complex number.

    :param z: A complex number representing the point.
    """
    self.__init__(z.real, z.imag)
    if kwargs:
      self.__init__(**kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    """
    Initialize the PlanePoint with default coordinates (0.0, 0.0).
    """
    xKeys = stringList("""x, X, xCoord, xCoordinate, xPos, xPosition""")
    yKeys = stringList("""y, Y, yCoord, yCoordinate, yPos, yPosition""")
    _x, kwargs = self.parseKwargs(float, int, *xKeys, **kwargs)
    _y, kwargs = self.parseKwargs(float, int, *yKeys, **kwargs)
    if _x is not None and _y is not None:
      self.__init__(_x, _y)
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
