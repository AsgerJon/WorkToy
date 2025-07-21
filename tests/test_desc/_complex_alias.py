"""
ComplexAlias provides a complex number implementation using the 'Alias'
descriptor class from the 'worktoy.desc' module. Since 'Alias' simply adds
another named reference to an existing object, it must subclass another of
the complex number implementations. For no particular reason, it
subclasses 'ComplexBox', which uses the 'AttriBox' descriptor for its
real and imaginary parts.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import Alias
from worktoy.utilities.mathematics import exp, log
from . import ComplexBox

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class ComplexAlias(ComplexBox):
  """
  ComplexAlias provides a complex number implementation using the 'Alias'
  descriptor class from the 'worktoy.desc' module. Since 'Alias' simply adds
  another named reference to an existing object, it must subclass another of
  the complex number implementations. For no particular reason, it
  subclasses 'ComplexBox', which uses the 'AttriBox' descriptor for its
  real and imaginary parts.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Virtual Variables
  x = Alias('RE')
  y = Alias('IM')

  def __bool__(self, ) -> bool:
    return True if self.ABS > 1e-16 else False

  def __complex__(self, ) -> complex:
    return self.x + self.y * 1j

  def __iter__(self, ) -> Iterator[float]:
    yield self.x
    yield self.y

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
    spec = """%f + %fJ""" if self.y > 0 else """%f - %fJ"""
    return spec % (self.x, abs(self.y),)

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
    x, y = self.x + other.x, self.y + other.y
    return cls(x, y)

  def __neg__(self, ) -> Self:
    cls = type(self)
    return cls(-self.x, -self.y)

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
    x = self.x * other.x - self.y * other.y
    y = self.x * other.y + self.y * other.x
    return cls(x, y)

  def __invert__(self, ) -> Self:
    if not self:
      raise ZeroDivisionError
    cls = type(self)
    return cls(self.x / self.ABS ** 2, -self.y / self.ABS ** 2)

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
    logX = other.x * log(self.ABS) - other.y * self.ARG
    logY = other.x * self.ARG + other.y * log(self.ABS)
    return cls(exp(logX + logY * 1j), )

  def __abs__(self, ) -> float:
    return self.ABS

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    if len(args) == 1:
      arg = complex(args[0])
      self.x, self.y = arg.real, arg.imag
    else:
      self.x, self.y, *_ = args
