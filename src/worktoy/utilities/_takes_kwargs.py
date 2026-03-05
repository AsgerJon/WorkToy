"""
The 'takesKwargs' function receives another function as argument,
and returns 'True' or 'False' indicating whether the function signature
includes a '**' parameter.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from inspect import signature, Parameter

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable


def takesKwargs(func: Callable) -> bool:
  """
  The 'takesKwargs' function receives another function as argument,
  and returns 'True' or 'False' indicating whether the function signature
  includes a '**' parameter.
  """
  func = getattr(func, '__func__', func)
  sig = signature(func)
  params = sig.parameters.values()
  for p in params:
    if p.kind == Parameter.VAR_KEYWORD:
      return True
  return False
