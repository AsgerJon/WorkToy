"""
ComplexFields provides a complex number implementation for testing
'Field' descriptor class from the 'worktoy.desc' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from cmath import exp, log
from math import atan2
from typing import TYPE_CHECKING

from worktoy.core.sentinels import DELETED
from worktoy.desc import Field
from worktoy.keenum import AccessNum
from worktoy.utilities import maybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Iterator, TypeAlias

  AccessReg: TypeAlias = tuple[str, AccessNum, Any]
  AccessRegs: TypeAlias = tuple[AccessReg, ...]


class ComplexFields:
  """ComplexFields provides a complex number implementation for testing
  descriptor classes. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __access_registry__ = None
  __abs_cache__ = None

  #  Fallback Variables
  __fallback_real__ = 0.0
  __fallback_imag__ = 0.0

  #  Private Variables
  __real_part__ = None
  __imag_part__ = None

  #  Public Variables
  RE = Field()
  IM = Field()

  #  Virtual Variables
  ABS = Field()
  ARG = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @ABS.preGet
  def _preGetABS(self) -> None:
    self.__abs_cache__ = (self.RE ** 2 + self.IM ** 2) ** 0.5

  @RE.GET
  def _getReal(self) -> float:
    return maybe(self.__real_part__, self.__fallback_real__)

  @IM.GET
  def _getImag(self) -> float:
    return maybe(self.__imag_part__, self.__fallback_imag__)

  @ABS.GET
  def _getABS(self) -> float:
    return self.__abs_cache__

  @ARG.GET
  def _getARG(self) -> float:
    if self:
      return atan2(self.IM, self.RE)
    raise ZeroDivisionError

  def getAccessRegistry(self) -> AccessRegs:
    return maybe(self.__access_registry__, ())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _registerAccess(self, key: str, op: AccessNum, value: Any) -> None:
    existing = self.getAccessRegistry()
    entry = (key, op, value)
    self.__access_registry__ = (*existing, entry)

  @RE.onGet
  def _registerREonGet(self, value: float) -> None:
    self._registerAccess('RE', AccessNum.GET, value)

  @RE.onSet
  def _registerREonSet(self, value: float) -> None:
    self._registerAccess('RE', AccessNum.SET, value)

  @RE.onDelete
  def _registerREonDelete(self) -> None:
    self._registerAccess('RE', AccessNum.DELETE, None)

  @IM.onGet
  def _registerIMonGet(self, value: float) -> None:
    self._registerAccess('IM', AccessNum.GET, value)

  @IM.onSet
  def _registerIMonSet(self, value: float) -> None:
    self._registerAccess('IM', AccessNum.SET, value)

  @IM.preDelete
  @RE.preDelete
  def _noop(self) -> None:
    pass

  @IM.onDelete
  def _registerIMonDelete(self) -> None:
    self._registerAccess('IM', AccessNum.DELETE, None)

  @RE.SET
  def _setReal(self, value: float) -> None:
    self.__real_part__ = float(value)

  @IM.SET
  def _setImag(self, value: float) -> None:
    self.__imag_part__ = float(value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DELETERS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @RE.DELETE
  def _deleteReal(self) -> None:
    self.__real_part__ = DELETED

  @IM.DELETE
  def _deleteImag(self) -> None:
    self.__imag_part__ = DELETED

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
    except (ValueError, TypeError):
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

  def __init__(self, *args, **kwargs) -> None:
    if len(args) == 1:
      arg = complex(args[0])
      self.RE, self.IM = arg.real, arg.imag
    else:
      self.RE, self.IM, *_ = args
    self._noop()
