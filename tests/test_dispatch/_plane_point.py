"""
SigFuncClass provides a class with a 'Dispatcher' descriptor based on the
'sigFuncDict' dictionary.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class PlanePoint:
  """
  SigFuncClass provides a class with a 'Dispatcher' descriptor based on the
  'sigFuncDict' dictionary.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  from worktoy.dispatch import Dispatcher
  __init__ = Dispatcher()

  #  Public Variables
  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @__init__.overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

  @__init__.overload(complex)
  def __init__(self, x: complex) -> None:
    self.x = x.real
    self.y = x.imag

  @__init__.overload(THIS)
  def __init__(self, other: Self) -> None:
    self.x = other.x
    self.y = other.y

  @__init__.overload()
  def __init__(self) -> None:
    self.x = 0.0
    self.y = 0.0

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self) -> str:
    infoSpec = """%s(%s, %s)"""
    return infoSpec % (self.__class__.__name__, self.x, self.y)

  __repr__ = __str__
