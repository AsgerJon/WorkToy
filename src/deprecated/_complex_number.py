"""ComplexNumber implementation"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import atan2, sin, cos

from worktoy.mcls import BaseMeta
from worktoy.static import overload
from worktoy.static.zeroton import THIS

from worktoy.waitaminute import DispatchException
from . import Number

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False
if TYPE_CHECKING:
  from typing import Any, Self


class ComplexNumber(metaclass=BaseMeta):
  """Complex number representation. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public variables

  RE = Number(0.0)
  IM = Number(0.0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def fromPolar(cls, r: float, theta: float) -> Self:
    """Create a complex number from polar coordinates."""
    return cls(r * cos(theta), r * sin(theta))

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

  def __str__(self, ) -> str:
    """
    String representation of the complex number.
    """
    infoSpec = """%s + %sJ"""
    return infoSpec % (self.RE, self.IM)

  def __repr__(self, ) -> str:
    """
    Code representation of the complex number.
    """
    infoSpec = """%s(%s, %s)"""
    clsName = type(self).__name__
    return infoSpec % (clsName, self.RE, self.IM)

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
    r2 = abs(self) ** 2
    return cls(self.RE / r2, -self.IM / r2)

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

  def toPolar(self, ) -> tuple[float, float]:
    """Convert the complex number to polar coordinates."""
    if TYPE_CHECKING:
      assert isinstance(self, ComplexNumber)
    if self:
      return abs(self), self.__arg__()
    raise ZeroDivisionError

  def __complex__(self, ) -> complex:
    """Convert the complex number to a complex type."""
    if TYPE_CHECKING:
      assert isinstance(self, ComplexNumber)
    return self.RE + self.IM * 1j
