"""
BotchedComplex is a 'ComplexMixin' wrong in every operation.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import ComplexMixin

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class BotchedComplex(ComplexMixin):
  """
  A bank of tests proves itself by failing, and a bank test that fails
  against nothing tests nothing. 'BotchedComplex' gives a wrong answer
  to every operation the bank exercises and refuses no operand, so each
  of the twenty-five tests of 'ComplexTest' must fail against it: a
  bank test that passes here has stopped checking.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _wrong(self) -> BotchedComplex:
    """The one wrong answer every operation gives."""
    return type(self)(9, 9)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __abs__(self) -> float:
    return 0.0

  def __pos__(self) -> BotchedComplex:
    return self._wrong()

  def __neg__(self) -> BotchedComplex:
    return self._wrong()

  def __invert__(self) -> BotchedComplex:
    return self._wrong()

  def __add__(self, other: Any) -> BotchedComplex:
    return self._wrong()

  def __radd__(self, other: Any) -> BotchedComplex:
    return self._wrong()

  def __sub__(self, other: Any) -> BotchedComplex:
    return self._wrong()

  def __rsub__(self, other: Any) -> BotchedComplex:
    return self._wrong()

  def __mul__(self, other: Any) -> BotchedComplex:
    return self._wrong()

  def __rmul__(self, other: Any) -> BotchedComplex:
    return self._wrong()

  def __truediv__(self, other: Any) -> BotchedComplex:
    return self._wrong()

  def __rtruediv__(self, other: Any) -> BotchedComplex:
    return self._wrong()

  def __pow__(self, other: Any) -> BotchedComplex:
    return self._wrong()

  def __rpow__(self, other: Any) -> BotchedComplex:
    return self._wrong()
