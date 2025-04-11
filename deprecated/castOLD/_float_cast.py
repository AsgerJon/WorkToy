"""The 'floatCast' function receives a python object and attempts to static
it as a floating point valued number. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import NumCastException


class FloatCastException(NumCastException):
  """The 'FloatCastException' exception is raised when a value cannot be
  static to a floating point number. """

  def __init__(self, value: object) -> None:
    NumCastException.__init__(self, value, float)


def floatCast(value: object, ) -> float:
  """The 'floatCast' function receives a python object and attempts to static
  it as a floating point valued number. """
  if isinstance(value, float):
    return value
  if isinstance(value, int):
    return float(value)
  if isinstance(value, complex):
    if not value.imag:
      return float(value.real)
    raise FloatCastException(value)
  try:
    return type.__call__(float, value)
  except Exception:
    raise FloatCastException(value)
