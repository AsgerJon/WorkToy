"""OverloadExample demonstrates usage of overload. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy import maybe

try:
  from typing import TYPE_CHECKING, Any
except ImportError:
  TYPE_CHECKING = False
  Any = object

if TYPE_CHECKING:
  ListStr = list[str]
else:
  ListStr = object


class OverloadExample:
  """OverloadExample demonstrates usage of overload. """

  __local_out__ = None
  __local_err__ = None

  def _resetLocals(self, ) -> None:
    """Resets the local output and error"""
    self.__local_out__ = None
    self.__local_err__ = None

  def _getLocalOut(self, ) -> ListStr:
    """Getter-function for local output"""
    return maybe(self.__local_out__, [])

  def _getLocalErr(self, ) -> ListStr:
    """Getter-function for local error"""
    return maybe(self.__local_err__, '')

  def _localPrint(self, line: str) -> None:
    """Adds line to local output"""
    existing = self._getLocalOut()
    self.__local_out__ = [*existing, line]

  def _localError(self, line: str) -> None:
    """Sets the local error"""
    existing = self._getLocalErr()
    self.__local_err__ = [*existing, line]

  def setup(self) -> Any:
    """Setup example function"""
    self._resetLocals()

    #  $$START OF SETUP$$
    from worktoy import EZData, overload

    class Complex(EZData):
      """Complex encapsulates complex number and supports multiple
      constructors by leveraging the overload decorator. """

      RE = 0.0  # Real part
      IM = 0.0  # Imaginary part

      @overload(float, float)  # Real and imaginary parts
      def __init__(self, x: float, y: float) -> None:
        self.RE = x
        self.IM = y

      @overload(complex)  # Complex number
      def __init__(self, z: complex) -> None:
        self.RE = z.real
        self.IM = z.imag

      @overload()  # Allowing default to be zero
      def __init__(self) -> None:
        pass

    #  $$END OF SETUP$$
    return Complex, EZData, overload

  def main(self) -> None:
    """Main example function. This part of the example code is what is
    placed in the "if __name__ == '__main__':" block. """
