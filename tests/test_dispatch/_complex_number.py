"""
ComplexNumber provides testing of the inline function overloader.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox, Field
from worktoy.dispatch import Dispatcher
from worktoy.utilities.mathematics import atan2, exp, log

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Iterator


class ComplexNumber:
  """
  ComplexNumber provides testing of the inline function overloader.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables

  #  Public Variables
  RE = AttriBox[float](0.0)
  IM = AttriBox[float](0.0)

  #  Virtual Variables
  ABS = Field()
  ARG = Field()

  #  Overloaded Functions
  __init__ = Dispatcher()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @ABS.GET
  def _getABS(self) -> float:
    return (self.RE ** 2 + self.IM ** 2) ** 0.5

  @ARG.GET
  def _getARG(self) -> float:
    if self:
      return atan2(self.IM, self.RE)
    raise ZeroDivisionError

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __bool__(self, ) -> bool:
    return True if self.ABS > 1e-16 else False

  def __complex__(self, ) -> complex:
    return self.RE + self.IM * 1j

  def __iter__(self, ) -> Iterator[float]:
    yield self.RE
    yield self.IM

  def __repr__(self, ) -> str:
    infoSpec = """%s(%s, %s)"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, *self,)
    return info

  def __str__(self, ) -> str:
    if not self:
      return '0'
    if abs(self.IM) < 1e-16:
      return """%f""" % (self.RE,)
    if abs(self.RE) < 1e-16:
      return """%fJ""" % (self.IM,)
    spec = """%f + %fJ""" if self.IM > 0 else """%f - %fJ"""
    return spec % (self.RE, abs(self.IM),)

  def __hash__(self, ) -> int:
    return hash((*self,))

  def cast(self, other: Any) -> Self:
    cls = type(self)
    if isinstance(other, cls):
      return other
    try:
      other = cls(other)
    except (ValueError, TypeError) as exception:
      return NotImplemented
    else:
      return other

  def __eq__(self, other: Any) -> bool:
    other = self.cast(other)
    if other is NotImplemented:
      return NotImplemented
    return True if (self - other).ABS < 1e-16 else False

  def __add__(self, other: Any) -> Self:
    other = self.cast(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    x, y = self.RE + other.RE, self.IM + other.IM
    return cls(x, y)

  def __neg__(self, ) -> Self:
    cls = type(self)
    return cls(-self.RE, -self.IM)

  def __sub__(self, other: Any) -> Self:
    other = self.cast(other)
    if other is NotImplemented:
      return NotImplemented
    return self + (-other)

  def __mul__(self, other: Any) -> Self:
    other = self.cast(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    x = self.RE * other.RE - self.IM * other.IM
    y = self.RE * other.IM + self.IM * other.RE
    return cls(x, y)

  def __invert__(self, ) -> Self:
    if not self:
      raise ZeroDivisionError
    cls = type(self)
    return cls(self.RE / self.ABS ** 2, -self.IM / self.ABS ** 2)

  def __truediv__(self, other: Any) -> Self:
    other = self.cast(other)
    if other is NotImplemented:
      return NotImplemented
    if not other:
      raise ZeroDivisionError
    if not self:
      return self
    return self * (~other)

  def __pow__(self, other: Any) -> Self:
    other = self.cast(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    logX = other.RE * log(self.ABS) - other.IM * self.ARG
    logY = other.RE * self.ARG + other.IM * log(self.ABS)
    return cls(exp(logX + logY * 1j), )

  def __abs__(self, ) -> float:
    return self.ABS

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @__init__.overload(float, float)
  def __init__(self, RE: float, IM: float) -> None:
    self.RE = RE
    self.IM = IM

  @__init__.overload(complex)
  def __init__(self, z: complex) -> None:
    self.__init__(z.real, z.imag)

  @__init__.overload(THIS)
  def __init__(self, other: Self) -> None:
    self.__init__(other.RE, other.IM)

  @__init__.overload(float)
  def __init__(self, RE: float) -> None:
    self.__init__(RE, 0.0)

  @__init__.overload()
  def __init__(self) -> None:
    self.__init__(0.0, 0.0)

  @__init__.finalize
  def __init__(self, *args, **kwargs) -> None:
    pass
