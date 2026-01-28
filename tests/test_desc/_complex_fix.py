"""
ComplexFix provides a complex number implementation for testing the
'FixBox' descriptor class from the 'worktoy.desc' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from random import random
from typing import TYPE_CHECKING

from worktoy.desc import FixBox, Field
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.utilities import stringList
from worktoy.utilities.mathematics import atan2, exp, log

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Iterator


class ComplexFix(BaseObject):
  """
  ComplexFix provides a complex number implementation for testing the
  'FixBox' descriptor class from the 'worktoy.desc' module.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __real_keys__ = stringList("""real, x, RE, cos""")
  __imag_keys__ = stringList("""imag, y, IM, sin""")
  __key_groups__ = __real_keys__, __imag_keys__

  #  Fallback Variables
  __fallback_real__ = 0.0
  __fallback_imag__ = 0.0

  #  Private Variables
  __real_part__ = None
  __imag_part__ = None

  #  Public Variables
  RE = FixBox[float](0.0)
  IM = FixBox[float](0.0)

  #  Virtual Variables
  ABS = Field()
  ARG = Field()

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

  def __pos__(self) -> Self:
    """
    Returns the conjugate of the complex number.
    """
    cls = type(self)
    return cls(self.RE, -self.IM)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float, float)
  def __init__(self, realPart: float, imagPart: float) -> None:
    self.RE = realPart
    self.IM = imagPart

  @overload(complex)
  def __init__(self, other: complex) -> None:
    self.RE = other.real
    self.IM = other.imag

  @overload()
  def __init__(self, **kwargs) -> None:
    _x, _y = None, None
    for group in self.__key_groups__:
      for key in group:
        if key in kwargs:
          value = kwargs.pop(key)
          if key in self.__real_keys__:
            _x = value
          else:
            _y = value
          break
    if _x is not None:
      self.RE = _x
    if _y is not None:
      self.IM = _y

  @classmethod
  def rand(cls, *args, ) -> Self:
    a, b, *_ = (*args, 0.0, 1.0)
    minVal, maxVal = min(a, b), max(a, b)
    realVal = (maxVal - minVal) * random() + minVal
    imagVal = (maxVal - minVal) * random() + minVal
    return cls(realVal, imagVal)

  @classmethod
  def rands(cls, n: int, *args, ) -> Iterator[Self]:
    for _ in range(n):
      yield cls.rand(*args, )
