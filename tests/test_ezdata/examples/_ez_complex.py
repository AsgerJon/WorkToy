"""
EZComplex provides an implementation of the 'EZData' dataclass, which is
used for testing the functionality of the 'EZData' dataclass and its
related components.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData, EZField
from worktoy.work_test import ComplexMixin

if TYPE_CHECKING:  # pragma: no cover
  pass


class EZComplex(EZData, ComplexMixin):
  """
  EZComplex is an 'EZData' implementation of a complex number. It mixes
  in 'ComplexMixin' for the complex arithmetic dunder methods and lets
  'EZData' generate the construction boilerplate. Complex numbers have
  no ordering, so the class is declared without the 'ordered' keyword.
  """

  REAL = EZField[float](0.0)
  IMAG = EZField[float](0.0)
