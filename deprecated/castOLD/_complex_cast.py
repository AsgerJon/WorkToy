"""The 'complexCast' function receives a python object and attempts to static
it as a complex number. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import NumCastException

try:
  from typing import TYPE_CHECKING, SupportsComplex
except ImportError:
  TYPE_CHECKING = False
  Any = object
  SupportsComplex = object


class ComplexCastException(NumCastException):
  """The 'ComplexCastException' exception is raised when a value cannot be
  static to a complex number. """

  def __init__(self, value: object) -> None:
    NumCastException.__init__(self, value, complex)


def complexCast(value: SupportsComplex, ) -> complex:
  """The 'complexCast' function receives a python object and attempts to
  static
  it as a complex number. """
  if isinstance(value, complex):
    return value
  if isinstance(value, float):
    return value + 0j
  if isinstance(value, int):
    return float(value) + 0j
  try:
    return complex(value)
  except Exception:
    raise ComplexCastException(value)
