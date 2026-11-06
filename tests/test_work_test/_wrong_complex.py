"""
WrongComplex is a 'ComplexMixin' whose addition is wrong on purpose.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import ComplexMixin

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class WrongComplex(ComplexMixin):
  """
  A bank of tests proves itself by failing: an implementation with one
  wrong operation must fail the tests of that operation and no other.
  'WrongComplex' adds as if every addend were zero, so the four addition
  tests of 'ComplexTest' fail against it and the other twenty-one pass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __add__(self, other: Any) -> Any:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return type(self)(self.REAL, self.IMAG)
