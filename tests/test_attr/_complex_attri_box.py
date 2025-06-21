"""
ComplexAttriBox provides the implementation of a complex number
using the AttriBox descriptor for real and imaginary parts.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from tests import ComplexBase
from worktoy.attr import AttriBox

from typing import TYPE_CHECKING
from worktoy.mcls import BaseMeta
from worktoy.static import overload
from worktoy.static.zeroton import THIS

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class ComplexAttriBox(ComplexBase, metaclass=BaseMeta):
  """Complex number representation. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public variables

  RE = AttriBox[float](0.0)
  IM = AttriBox[float](0.0)

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
