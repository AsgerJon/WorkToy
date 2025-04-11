"""The 'typeCast' function attempts to static an object to a given type. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.castOLD import numCast
from worktoy.text import typeMsg
from worktoy.waitaminute import TypeCastException

try:
  from typing import Any
except ImportError:
  Any = object


def typeCast(value: object, target: type, **kwargs) -> Any:
  """The 'typeCast' function attempts to static an object to a given type.
  """
  if not isinstance(target, type):
    e = typeMsg('target', target, type)
    raise TypeError(e)
  if isinstance(value, target):
    return value
  if target in [int, float, complex]:
    try:
      return numCast(value, target)
    except Exception as exception:
      if kwargs.get('strict', True):
        raise TypeCastException(value, target) from exception
  try:
    return target(value)
  except Exception as exception:
    if kwargs.get('strict', True):
      raise TypeCastException(value, target) from exception
