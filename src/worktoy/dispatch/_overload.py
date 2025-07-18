"""
The 'overload' function provides a decorator setting type signatures for
particular function overload. This overloading implementation requires
that the owning class is derived from 'BaseMeta' or a subclass of
'BaseMeta'. Other classes must use the 'Dispatcher' descriptor from
'worktoy.dispatch' instead.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import Dispatcher, TypeSignature

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias

  Method: TypeAlias = Callable[..., Any]
  Decorator: TypeAlias = Callable[[Method], Dispatcher]


def overload(*types, ) -> Decorator:
  """
  The 'overload' function provides a decorator setting type signatures for
  particular function overload. This overloading implementation requires
  that the owning class is derived from 'BaseMeta' or a subclass of
  'BaseMeta'. Other classes must use the 'Dispatcher' descriptor from
  'worktoy.dispatch' instead.
  """

  sig = TypeSignature(*types)

  def decorator(arg: Any) -> Dispatcher:
    if isinstance(arg, Dispatcher):  # allows stacking overloads
      func = ([f for _, f in arg.__sig_funcs__] or []).pop()
      arg.__sig_funcs__.append((sig, func))
      return arg
    return Dispatcher([(sig, arg)])

  return decorator
