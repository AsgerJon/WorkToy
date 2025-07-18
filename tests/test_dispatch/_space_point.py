"""
SpacePoint subclasses the PlanePoint class extending it to include the
z-coordinate. The purpose is to demonstrate how the overloading dispatcher
extends the overloading to cover more decorated functions, whilst
retaining those defined on the parent class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from . import PlanePoint

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class SpacePoint(PlanePoint):
  """
  SpacePoint subclasses the PlanePoint class extending it to include the
  z-coordinate. The purpose is to demonstrate how the overloading dispatcher
  extends the overloading to cover more decorated functions, whilst
  retaining those defined on the parent class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  __init__ = PlanePoint.__init__.clone()
  z = AttriBox[float](0.0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @__init__.overload(float, float, float)
  def __init__(self, x: float, y: float, z: float) -> None:
    super().__init__(x, y)
    self.z = z

  @__init__.overload(THIS)
  def __init__(self, other: Self) -> None:
    self.x = other.x
    self.y = other.y
    self.z = other.z

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self) -> str:
    infoSpec = """%s(%s, %s, %s)"""
    return infoSpec % (self.__class__.__name__, self.x, self.y, self.z)

  __repr__ = __str__
