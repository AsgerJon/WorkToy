"""
The 'argsInspect' function receives another function as argument,
and returns a tuple of types corresponding to the type hints.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from inspect import signature, Parameter

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable


def argsCount(func: Callable) -> int:
  """
  The 'argsCount' function receives another function as argument,
  and returns the number of arguments that function takes.
  """
  func = getattr(func, '__func__', func)
  sig = signature(func)
  params = sig.parameters.values()
  posKind = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
  posParams = [p for p in params if p.kind in posKind]
  return len(posParams)
