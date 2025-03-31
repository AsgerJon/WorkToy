"""The 'intCast' function receives a python object and attempts to static
it as an integer valued number. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import floatCast
from worktoy.waitaminute import NumCastException


class IntCastException(NumCastException):
  """The 'IntCastException' class is raised when a value cannot be static as
  an integer. """

  def __init__(self, value: object) -> None:
    NumCastException.__init__(self, value, int)


def intCast(value: object) -> int:
  """The 'intCast' function receives a python object and attempts to static
  it as an integer valued number. """

  if isinstance(value, int):
    return value
  if isinstance(value, float):
    if value.is_integer():
      return int(value)
    raise IntCastException(value)
  if isinstance(value, complex):
    if not value.imag and value.real.is_integer():
      return int(value.real)
    raise IntCastException(value)
  try:
    return type.__call__(int, value)
  except Exception as exception:
    try:
      return intCast(floatCast(value))
    except Exception as e2:
      raise IntCastException(value) from exception
