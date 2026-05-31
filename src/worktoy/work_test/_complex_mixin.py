"""
ComplexMixin adds complex-number arithmetic dunders to a class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import TYPE_CHECKING, cast

from worktoy.desc import Field
from worktoy.waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Union, Self, Optional, Iterator
  from types import NotImplementedType as NotImpType
else:
  Self = object
  NotImpType = object


class ComplexMixin:
  """
  ComplexMixin is a mixin class for the purpose of complex number
  implementations.

  Subclasses can override the attributes 'REAL' and 'IMAG' to provide the
  real and imaginary parts of the complex number, respectively.
  Alternatively, subclasses can override the getter methods: '_getReal' and
  '_getImag' to compute the real and imaginary parts dynamically.

  The mixin provides the dunder methods for arithmetic operations related to
  complex numbers.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables
  __fallback_real__: float = 0.0
  __fallback_imag__: float = 0.0

  #  Private Variables
  __real_value__: Optional[float] = None
  __imag_value__: Optional[float] = None

  #  Public Variables
  REAL: Field[float] = Field()
  IMAG: Field[float] = Field()

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @REAL.GET
  def _getReal(self, **kwargs) -> float:
    if self.__real_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__real_value__ = self.__fallback_real__
      return self._getReal(_recursion=True)
    if isinstance(self.__real_value__, (float, int)):
      return float(self.__real_value__)
    raise TypeException('__real_value__', self.__real_value__, float)

  @IMAG.GET
  def _getImag(self, **kwargs) -> float:
    if self.__imag_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__imag_value__ = self.__fallback_imag__
      return self._getImag(_recursion=True)
    if isinstance(self.__imag_value__, (float, int)):
      return float(self.__imag_value__)
    raise TypeException('__imag_value__', self.__imag_value__, float)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @REAL.SET
  def _setReal(self, value: Any) -> None:
    if not isinstance(value, (float, int)):
      raise TypeException('REAL', value, float)
    self.__real_value__ = float(value)

  @IMAG.SET
  def _setImag(self, value: Any) -> None:
    if not isinstance(value, (float, int)):
      raise TypeException('IMAG', value, float)
    self.__imag_value__ = float(value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, ) -> None:
    if len(args) == 1:
      if isinstance(args[0], complex):
        self._setReal(args[0].real)
        self._setImag(args[0].imag)
      else:
        other = complex(args[0])
        self._setReal(other.real)
        self._setImag(other.imag)
    elif len(args) >= 1:
      self._setReal(float(args[0]))
      self._setImag(float(args[1]))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  HELPER METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _resolveOther(cls, other: Any) -> Union[NotImpType, Self]:
    """
    The '_resolveOther' method coerces 'other' to an instance of 'cls',
    accepting another instance, a real number, a builtin complex, or any
    iterable or single value the constructor admits, and returning
    'NotImplemented' when none of those work.
    """
    if isinstance(other, cls):
      return other
    if isinstance(other, (float, int)):
      return cls(float(other), 0.0)
    if isinstance(other, complex):
      return cls(other.real, other.imag)
    try:
      if isinstance(other, str):
        raise TypeError
      args = (*other,)
    except TypeError:
      try:
        resolved = cls(other)
      except (TypeError, ValueError):
        return NotImplemented
      else:
        return resolved
    else:
      try:
        resolved = cls(*args)
      except (TypeError, ValueError):
        return NotImplemented
      else:
        return resolved

  def conjugate(self) -> Self:
    """
    The 'conjugate' method returns the complex conjugate as a new
    instance.
    """
    cls = type(self)
    out = cls(self.REAL, -self.IMAG)
    return cast(Self, out)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __repr__(self) -> str:
    clsName = type(self).__name__
    if not self:
      return """%s()""" % clsName
    if abs(self.IMAG) < sys.float_info.epsilon:
      return """%s(%.3f)""" % (clsName, self.REAL)
    if abs(self.REAL) < sys.float_info.epsilon:
      return """%s(0.0, %.3f)""" % (clsName, self.IMAG)
    return """%s(%.3f, %.3f)""" % (clsName, self.REAL, self.IMAG)

  def __str__(self) -> str:
    if not self:
      return '0'
    if abs(self.IMAG) < sys.float_info.epsilon:
      return '%.3f' % self.REAL
    if abs(self.REAL) < sys.float_info.epsilon:
      return '%.3fJ' % self.IMAG
    sign = '-' if self.IMAG < 0 else '+'
    return """%.3f %s %.3fJ""" % (self.REAL, sign, abs(self.IMAG))

  def __complex__(self) -> complex:
    return complex(self.REAL, self.IMAG)

  def __bool__(self) -> bool:
    """
    A complex number is truthy when it is nonzero. Rather than an exact
    comparison to zero, the magnitude is tested against
    'sys.float_info.epsilon', so floating-point dust below that threshold
    still counts as zero.
    """
    return True if abs(self) > sys.float_info.epsilon else False

  def __eq__(self, other: Any) -> bool:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    real, imag = resolved
    if self.REAL == real and self.IMAG == imag:
      return True
    return False

  def __hash__(self) -> int:
    return hash(complex(self.REAL, self.IMAG))

  def __abs__(self) -> float:
    return (self.REAL ** 2 + self.IMAG ** 2) ** 0.5

  def __pos__(self) -> Self:
    return cast(Self, type(self)(self.REAL, self.IMAG))

  def __neg__(self) -> Self:
    return cast(Self, type(self)(-self.REAL, -self.IMAG))

  def __invert__(self) -> Self:
    return cast(Self, type(self)(self.REAL, -self.IMAG))

  def __add__(self, other: Any) -> Union[NotImpType, Self]:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    x, y = resolved
    return cast(Self, type(self)(self.REAL + x, self.IMAG + y))

  def __radd__(self, other: Any) -> Union[NotImpType, Self]:
    return self.__add__(other)

  def __sub__(self, other: Any) -> Union[NotImpType, Self]:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    x, y = resolved
    return cast(Self, type(self)(self.REAL - x, self.IMAG - y))

  def __rsub__(self, other: Any) -> Union[NotImpType, Self]:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    x, y = resolved
    return cast(Self, type(self)(x - self.REAL, y - self.IMAG))

  def __mul__(self, other: Any) -> Union[NotImpType, Self]:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    real, imag = resolved
    newReal = self.REAL * real - self.IMAG * imag
    newImag = self.REAL * imag + self.IMAG * real
    return cast(Self, type(self)(newReal, newImag))

  def __rmul__(self, other: Any) -> Union[NotImpType, Self]:
    return self.__mul__(other)

  def __truediv__(self, other: Any) -> Union[NotImpType, Self]:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    x, y = resolved
    factor = (x ** 2 + y ** 2)
    if abs(factor) < sys.float_info.epsilon:
      raise ZeroDivisionError('complex division by zero')
    newX = self.REAL * x + self.IMAG * y
    newY = self.IMAG * x - self.REAL * y
    return cast(Self, type(self)(newX / factor, newY / factor))

  def __rtruediv__(self, other: Any) -> Union[NotImpType, Self]:
    if not self:
      raise ZeroDivisionError
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return resolved / self

  def __pow__(self, other: Any) -> Union[NotImpType, Self]:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    x, y = resolved
    result = complex(self.REAL, self.IMAG) ** complex(x, y)
    return cast(Self, type(self)(result.real, result.imag))

  def __rpow__(self, other: Any) -> Union[NotImpType, Self]:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return resolved ** self

  def __iter__(self, ) -> Iterator[float]:
    yield self.REAL
    yield self.IMAG
