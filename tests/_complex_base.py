"""
ComplexBase provides an implementation of complex numbers that makes
use of the overload functionality provided by the 'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import atan2

from worktoy.static import AbstractObject

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

from worktoy.mcls import BaseMeta

if TYPE_CHECKING:
  from typing import Any, Self


class ComplexBase(AbstractObject):
  """Complex number representation. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables
  __fallback_real__ = 0.0
  __fallback_imag__ = 0.0

  #  Public variables
  RE = 0.0  # Real part of the complex number
  IM = 0.0  # Imaginary part of the complex number

  #  When testing descriptor classes, we will subclass this class and
  #  replace the above with instances of the descriptor being tested.

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    """
    The simplest constructor possible. When testing overloading,
    a subclass will implement overloaded constructors.
    """
    self.RE = kwargs.get('real', self.__fallback_real__)
    self.IM = kwargs.get('imag', self.__fallback_imag__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __abs__(self, ) -> float:
    """Get the absolute value of the complex number."""
    return (self.RE ** 2 + self.IM ** 2) ** 0.5

  def __bool__(self, ) -> bool:
    """Get the boolean value of the complex number."""
    return True if self.RE ** 2 + self.IM ** 2 > 1.0e-12 else False

  def __arg__(self, ) -> float:
    """Get the argument of the complex number."""
    if TYPE_CHECKING:
      assert isinstance(self, ComplexBase)
    if not self:
      raise ZeroDivisionError
    return atan2(self.IM, self.RE)

  def _resolveOther(self, *args) -> Self:
    """Attempts to resolve argument to same type as self. """
    cls = type(self)
    if len(args) == 1:
      if isinstance(args[0], cls):
        return args[0]
    try:
      return cls(*args)
    except TypeError:  # DispatchException is a subclass of TypeError
      return NotImplemented

  def __hash__(self, ) -> int:
    """Hashes the (real, imag) tuple"""
    return hash((self.RE, self.IM))

  def __eq__(self, other: Any) -> bool:
    """Compare two complex numbers."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return False if self - other else True

  def __str__(self, ) -> str:
    """Get the string representation of the complex number. This uses 'J'
    upper-case to represent the imaginary unit. The form is then:
    'x + yJ'. """
    infoSpec = """%s + %sJ""" if self.IM >= 0 else """%s - %sJ"""
    info = infoSpec % (str(self.RE), str(abs(self.IM)))
    return info

  def __repr__(self, ) -> str:
    """Provides a code representation that would instantiate this object
    if passed to 'eval()'. """
    infoSpec = """%s(%s, %s)"""
    info = infoSpec % (type(self).__name__, str(self.RE), str(self.IM))
    return info

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  ARITHMETIC   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __add__(self, other: Any) -> Self:
    """Add two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    return cls(self.RE + other.RE, self.IM + other.IM)

  def __iadd__(self, other: Any) -> Self:
    """Add two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    self.RE += other.RE
    self.IM += other.IM
    return self

  def __radd__(self, other: Any) -> Self:
    """Add two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return self + other

  def __neg__(self, ) -> Self:
    """Negate the complex number."""
    cls = type(self)
    return cls(-self.RE, -self.IM)

  def __sub__(self, other: Any) -> Self:
    """Subtract two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return self + (-other)

  def __isub__(self, other: Any) -> Self:
    """Subtract two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    self.RE -= other.RE
    self.IM -= other.IM
    return self

  def __rsub__(self, other: Any) -> Self:
    """Subtract two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return other + (-self)

  def __mul__(self, other) -> Self:
    """Multiply two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return cls(
        self.RE * other.RE - self.IM * other.IM,
        self.RE * other.IM + self.IM * other.RE
    )

  def __imul__(self, other: Self) -> Self:
    """Multiply two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    self.RE *= other.RE
    self.IM *= other.IM
    return self

  def __rmul__(self, other: Self) -> Self:
    """Multiply two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return self * other

  def __invert__(self, ) -> Self:
    """Invert the complex number."""
    if not self:
      raise ZeroDivisionError
    cls = type(self)
    return cls(self.RE / (abs(self) ** 2), -self.IM / (abs(self) ** 2))

  def __truediv__(self, other: Self) -> Self:
    """Divide two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    if not other:
      raise ZeroDivisionError
    return self * (~other)

  def __itruediv__(self, other: Self) -> Self:
    """Divide two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    if not other:
      raise ZeroDivisionError
    return self.__mul__(~other)

  def __rtruediv__(self, other: Self) -> Self:
    """Divide two complex numbers."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    if not self:
      raise ZeroDivisionError
    return other * (~self)
