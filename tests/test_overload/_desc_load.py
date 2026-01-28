"""
DescLoad implements the same testing scheme as the 'NumLoad' class,
but where the 'NumLoad' class implements the overloading functionality
through the metaclass, 'DescLoad' implements the overloading functionality
through the 'descriptor' protocol. The primary concern is the case where
the attempting to cast an argument to a type, arises from a prior attempt
to instantiate that type.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.desc import Field, FixBox
from worktoy.dispatch import Dispatcher
from worktoy.utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator, Self


class DescLoad:
  """
  DescLoad implements the same testing scheme as the 'NumLoad' class,
  but where the 'NumLoad' class implements the overloading functionality
  through the metaclass, 'DescLoad' implements the overloading functionality
  through the 'descriptor' protocol. The primary concern is the case where
  the attempting to cast an argument to a type, arises from a prior attempt
  to instantiate that type.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __loaded_object__ = None

  #  Public Variables
  loaded = Field()
  x = FixBox[int](0)
  y = FixBox[int](0)
  z = FixBox[int](0)
  u = FixBox[int](0)
  v = FixBox[int](0)
  w = FixBox[int](0)

  #  Overload Variables
  __init__ = Dispatcher()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @loaded.GET
  def _getLoaded(self) -> Any:
    return self.__loaded_object__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @__init__.overload()
  def __init__(self, ) -> None:
    infoSpec = """@__init__.overload() = ()"""
    info = infoSpec
    self.__loaded_object__ = textFmt(info)

  @__init__.overload(int)
  def __init__(self, x: int, ) -> None:
    infoSpec = """@__init__.overload(int) = (%d)"""
    info = infoSpec % x
    self.__loaded_object__ = textFmt(info)
    self.x = x

  @__init__.overload(int, int)
  def __init__(self, x: int, y: int) -> None:
    infoSpec = """@__init__.overload(int, int) = (%d, %d)"""
    info = infoSpec % (x, y)
    self.__loaded_object__ = textFmt(info)
    self.x, self.y = x, y

  @__init__.overload(int, int, int)
  def __init__(self, x: int, y: int, z: int) -> None:
    infoSpec = """@__init__.overload(int, int, int) = (%d, %d, %d)"""
    info = infoSpec % (x, y, z)
    self.__loaded_object__ = textFmt(info)
    self.x, self.y, self.z = x, y, z

  @__init__.overload(int, int, int, int)
  def __init__(self, *args) -> None:
    infoSpec = """@__init__.overload(int, int, int, int) = (%d, %d, %d, 
    %d)"""
    x, y, z, u = args
    info = infoSpec % (x, y, z, u)
    self.__loaded_object__ = textFmt(info)
    self.x, self.y, self.z, self.u = x, y, z, u

  @__init__.overload(int, int, int, int, int)
  def __init__(self, *args) -> None:
    infoSpec = """@__init__.overload(int, int, int, int, int) = (%d, %d, %d, 
    %d, %d)"""
    x, y, z, u, v = args
    info = infoSpec % (x, y, z, u, v)
    self.__loaded_object__ = textFmt(info)
    self.x, self.y, self.z, self.u, self.v = x, y, z, u, v

  @__init__.overload(int, int, int, int, int, int)
  def __init__(self, *args) -> None:
    x, y, z, u, v, w = args
    infoSpec = """@__init__.overload(int, int, int, int, int, int) = (%d, 
    %d, %d, %d, %d, %d)"""
    info = infoSpec % (x, y, z, u, v, w)
    self.__loaded_object__ = textFmt(info)
    self.x, self.y, self.z, self.u, self.v, self.w = x, y, z, u, v, w

  @__init__.overload(THIS)
  def __init__(self, other: Self) -> None:
    self.__init__(*other, )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self, ) -> Iterator[int]:
    yield self.x
    yield self.y
    yield self.z
    yield self.u
    yield self.v
    yield self.w

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, type(self)):
      return NotImplemented
    for a, b in zip(self, other):
      if a != b:
        return False
    return True

  def __str__(self) -> str:
    return str(self.__loaded_object__)

  __repr__ = __str__
