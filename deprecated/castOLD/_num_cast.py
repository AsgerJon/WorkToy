"""The 'numCast' function receives a numeric value and a numeric type and
returns the value static as the given type if possible. If unable to static,
an instance of NumCastException is raised. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace
from worktoy.castOLD import intCast, floatCast, complexCast

try:
  from typing import TYPE_CHECKING, Any
except ImportError:
  TYPE_CHECKING = False
  Any = object


def numCast(value: object, numType: type) -> Any:
  """The 'numCast' function receives a numeric value and a numeric type and
  returns the value static as the given type if possible. If unable to
  static,
  an instance of NumCastException is raised. """

  if numType not in [int, float, complex]:
    e = """The 'numCast' function supports only target types: 'int', 'float',
    and 'complex', but received: '%s'!"""
    numTypeName = numType.__name__
    raise ValueError(e % monoSpace(numTypeName))
  if numType is int:
    return intCast(value)
  if numType is float:
    return floatCast(value)
  if numType is complex:
    return complexCast(value)
