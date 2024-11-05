"""The 'typeCast' function attempts to cast an object to a given type. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import numCast


def typeCast(value: object, target: type) -> object:
  """The 'typeCast' function attempts to cast an object to a given type. """
  if isinstance(value, target):
    return value
  if target in [int, float, complex]:
    return numCast(value, target)
  try:
    return target(value)
  except Exception as exception:
    e = """Unable to cast object: '%s' to type: '%s'!"""
    raise TypeError(e % (value, target)) from exception
