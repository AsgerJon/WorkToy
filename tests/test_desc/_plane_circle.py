"""
PlaneCircle provides a plane circle with center implemented with
'AttriBox' using 'PlanePoint' and radius as a float.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.static import overload
from worktoy.core.sentinels import THIS
from worktoy.utilities import stringList

from . import PlanePoint

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional, Self


class PlaneCircle(BaseObject):
  """
  PlaneCircle provides a plane circle with center implemented with
  'AttriBox' using 'PlanePoint' and radius as a float.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  center = AttriBox[PlanePoint](.0, .0)
  radius = AttriBox[float](0.0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(PlanePoint, float)
  def __init__(self, *args, **kwargs) -> None:
    """
    Initializes the PlaneCircle with a center and radius.
    """
    self.center = args[0]
    self.radius = args[1]
    if kwargs:
      self.__init__(**kwargs)

  @overload(complex, float)
  def __init__(self, z: complex, r: float, **kwargs) -> None:
    """
    Initializes the PlaneCircle with a center and radius.
    """
    self.__init__(PlanePoint(z), r, **kwargs)

  @overload(float, float, float)
  def __init__(self, x: float, y: float, r: float, **kwargs) -> None:
    """
    Initializes the PlaneCircle with a center and radius.
    """
    self.__init__(PlanePoint(x, y), r, **kwargs)

  @overload(THIS)
  def __init__(self, **kwargs) -> None:
    """
    Initializes the PlaneCircle with a center and radius.
    """
    self.__init__(self.center, self.radius, **kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    """
    Initializes the PlaneCircle with a center and radius.
    """
    centerKeys = stringList("""center, """)
    radiusKeys = stringList("""radius, r""")
    radius, kwargs = self.parseKwargs(float, *radiusKeys, **kwargs)
    center, kwargs = self.parseKwargs(PlanePoint, *centerKeys, **kwargs)
    if center is not None and radius is not None:
      self.__init__(center, radius, **kwargs)
