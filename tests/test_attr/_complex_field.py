"""
ComplexField provides the implementation of a complex number
using the Field descriptor for real and imaginary parts.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import atan2

from tests import ComplexBase
from worktoy.attr import Field
from worktoy.parse import maybe
from worktoy.waitaminute import WriteOnceError

from typing import TYPE_CHECKING
from worktoy.mcls import BaseMeta
from worktoy.static import overload
from worktoy.static.zeroton import THIS

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class ComplexField(ComplexBase, metaclass=BaseMeta):
  """Complex number representation. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

  @RE.GET
  def _getReal(self) -> float:
    """Get the real part of the complex number."""
    return maybe(self.__real_part__, self.__fallback_real__)

  @IM.GET
  def _getImag(self) -> float:
    """Get the imaginary part of the complex number."""
    return maybe(self.__imag_part__, self.__fallback_imag__)

  @ABS.GET
  def _getAbs(self) -> float:
    """Get the absolute value of the complex number."""
    return (self.RE ** 2 + self.IM ** 2) ** 0.5

  @ARG.GET
  def _getArg(self) -> float:
    """Get the argument of the complex number."""
    return atan2(self.IM, self.RE)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @RE.SET
  def _setReal(self, value: float) -> None:
    """
    Write-once setter for the real part of the complex number.
    """
    if self.__real_part__ is None:
      self.__real_part__ = value
    else:
      raise WriteOnceError('__real_part__', self.__real_part__, value)

  @IM.SET
  def _setImag(self, value: float) -> None:
    """
    Write-once setter for the imaginary part of the complex number.
    """
    if self.__imag_part__ is None:
      self.__imag_part__ = value
    else:
      raise WriteOnceError('__imag_part__', self.__imag_part__, value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    if TYPE_CHECKING:  # pragma: no cover
      assert callable(self.__init__)
    self.__init__(float(x), 0.0)

  @overload(tuple)
  @overload(list)
  def __init__(self, args: Any) -> None:
    """Initialize the complex number."""
    if TYPE_CHECKING:  # pragma: no cover
      assert callable(self.__init__)
    self.__init__(*args)

  @overload()
  def __init__(self) -> None:
    """Initialize the complex number."""
    if TYPE_CHECKING:  # pragma: no cover
      assert callable(self.__init__)
    self.__init__(0.0, 0.0)
