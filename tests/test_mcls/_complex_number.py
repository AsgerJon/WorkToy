"""ComplexNumber implementation"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import random
from math import atan2

from worktoy.parse import maybe
from worktoy.waitaminute import DispatchException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

from worktoy.mcls import BaseMeta
from worktoy.static import overload, THIS

if TYPE_CHECKING:
  from typing import Any, Self


class Number:
  """Number descriptor"""

  __field_name__ = None
  __field_owner__ = None

  __fallback_value__ = 0
  __default_value__ = None

  def getPrivateName(self, ) -> str:
    """Getter-function for the private name."""
    return '__pvt_%s' % self.__field_name__

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the value of the field."""
    if instance is None:
      return self
    pvtName = self.getPrivateName()
    defVal = maybe(self.__default_value__, self.__fallback_value__)
    return getattr(instance, pvtName, defVal)

  def __set__(self, instance: object, value: Any) -> None:
    """Set the value of the field."""
    if instance is None:
      raise TypeError('Cannot set attribute on class')
    pvtName = self.getPrivateName()
    setattr(instance, pvtName, value)

  def __init__(self, *args) -> None:
    """Initialize the Number object."""
    for arg in args:
      if isinstance(arg, (int, float, complex)):
        self.__default_value__ = arg
        break


class ComplexNumber(metaclass=BaseMeta):
  """Complex number representation. """

  RE = Number(0.0)
  IM = Number(0.0)

  @classmethod
  def rand(cls, maxAbs: float = None) -> Self:
    """Generate a random complex number."""
    if maxAbs is None:
      return cls.rand(1.0)
    out = cls(random(), random())
    return maxAbs / abs(out) * out

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    """Initialize the complex number."""
    self.RE = x
    self.IM = y

  @overload(int, int)
  def __init__(self, x: int, y: int) -> None:
    """Initialize the complex number."""
    self.RE = float(x)
    self.IM = float(y)

  @overload(complex)
  def __init__(self, z: complex) -> None:
    """Initialize the complex number."""
    self.RE = z.real
    self.IM = z.imag

  @overload(THIS)
  def __init__(self, z: Self) -> None:
    """Initialize the complex number."""
    self.RE = z.RE
    self.IM = z.IM

  @overload(float)
  @overload(int)
  def __init__(self, x: int) -> None:
    """Initialize the complex number."""
    if TYPE_CHECKING:
      assert callable(self.__init__)
    self.__init__(float(x), 0.0)

  @overload(tuple)
  @overload(list)
  def __init__(self, args: Any) -> None:
    """Initialize the complex number."""
    if TYPE_CHECKING:
      assert callable(self.__init__)
    self.__init__(*args)

  @overload()
  def __init__(self) -> None:
    """Initialize the complex number."""
    if TYPE_CHECKING:
      assert callable(self.__init__)
    self.__init__(0.0, 0.0)

  def __abs__(self, ) -> float:
    """Get the absolute value of the complex number."""
    return (self.RE ** 2 + self.IM ** 2) ** 0.5

  def __bool__(self, ) -> bool:
    """Get the boolean value of the complex number."""
    return True if self.RE ** 2 + self.IM ** 2 > 1.0e-12 else False

  def __arg__(self, ) -> float:
    """Get the argument of the complex number."""
    if TYPE_CHECKING:
      assert isinstance(self, ComplexNumber)
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
    except DispatchException:
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
