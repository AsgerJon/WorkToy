"""The 'numCast' function receives a numeric value and a numeric type and
returns the value cast as the given type if possible. If unable to cast,
an instance of NumCastException is raised. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import NumCastException

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False


def intCast(value: object) -> int:
  """The 'intCast' function receives a numeric value and returns the value
  cast as an integer if possible. If unable to cast, an instance of
  NumCastException is raised. """
  if isinstance(value, int):
    return value
  if isinstance(value, float):
    if value.is_integer():
      return int(value)
    raise NumCastException(value, int)
  if isinstance(value, complex):
    if not value.imag and value.real.is_integer():
      return int(value.real)
    raise NumCastException(value, int)
  try:
    if TYPE_CHECKING:
      assert isinstance(value, str)  # For the linters out there
    return int(value)
  except Exception as exception:
    raise NumCastException(value, int) from exception


def floatCast(value: object) -> float:
  """The 'floatCast' function receives a numeric value and returns the value
  cast as a float if possible. If unable to cast, an instance of
  NumCastException is raised. """
  if isinstance(value, float):
    return value
  if isinstance(value, int):
    return float(value)
  if isinstance(value, complex):
    if not value.imag:
      return float(value.real)
    raise NumCastException(value, float)
  try:
    if TYPE_CHECKING:
      assert isinstance(value, str)  # For the linters out there
    return float(value)
  except Exception as exception:
    raise NumCastException(value, float) from exception


def complexCast(value: object) -> complex:
  """The 'complexCast' function receives a numeric value and returns the
  value
  cast as a complex number if possible. If unable to cast, an instance of
  NumCastException is raised. """
  if isinstance(value, complex):
    return value
  if isinstance(value, int):
    return floatCast(value) + 0j
  if isinstance(value, float):
    return value + 0j
  try:
    if TYPE_CHECKING:
      assert isinstance(value, str)  # For the linters out there
    return complex(value)
  except Exception as exception:
    raise NumCastException(value, complex) from exception


def numCast(value: object, numType: type) -> object:
  """The 'numCast' function receives a numeric value and a numeric type and
  returns the value cast as the given type if possible. If unable to cast,
  an instance of NumCastException is raised. """

  if numType not in [int, float, complex]:
    try:
      return numType(value)
    except Exception as exception:
      e = """Tried casting object: '%s' to non-standard numeric type: 
      '%s', which raised an exception!"""
      raise TypeError(e % (value, numType,)) from exception
  if numType is int:
    return intCast(value)
  if numType is float:
    return floatCast(value)
  if numType is complex:
    return complexCast(value)
