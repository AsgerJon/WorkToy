"""Count the positional parameters of a callable.

The 'argsCount' function inspects a callable and returns how
many of its parameters can be passed positionally. '*args',
'**kw', and keyword-only parameters are not counted."""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from inspect import signature, Parameter

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable


def argsCount(func: Callable) -> int:
  """Return the count of positional parameters of 'func'.

  Bound methods are unwrapped via '__func__' so that 'self'
  is included in the count. Parameters of kind
  'POSITIONAL_ONLY' and 'POSITIONAL_OR_KEYWORD' are counted;
  '*args', '**kw', and 'KEYWORD_ONLY' parameters are
  ignored.

  Parameters
  ----------
  func : Callable
      The callable to inspect.

  Returns
  -------
  int
      The number of positional parameters.

  Examples
  --------
  >>> argsCount(lambda a, b, *args, c=0: None)
  2
  """
  func = getattr(func, '__func__', func)
  sig = signature(func)
  params = sig.parameters.values()
  posKind = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
  posParams = [p for p in params if p.kind in posKind]
  return len(posParams)
