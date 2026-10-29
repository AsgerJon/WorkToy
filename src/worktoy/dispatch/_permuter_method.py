"""
PermuterMethod is a 'Permuter' that forwards the calling instance ahead
of the reordered positional arguments.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import Permuter

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class PermuterMethod(Permuter):
  """
  PermuterMethod subclasses 'Permuter' from 'worktoy.dispatch' and provides
  a wrapper that extracts the calling 'instance' object and passes only
  remaining positional arguments through the arrangement.
  """

  def invoke(self, *args, **kwargs) -> Any:
    """
    The 'invoke' method accepts the calling instance ahead of the
    reordered positional arguments, so a 'PermuterMethod' can wrap a
    bound method: the instance is forwarded first, then the arguments
    restored to canonical order. The wrapped function and the instance
    are taken from 'args' by position rather than named as parameters,
    so keywords of the caller named 'func' or 'instance' go through to
    the function.

    Parameters
    ----------
    *args : Any
        The wrapped function, then the calling instance, forwarded as the
        first argument (None when the call gives none), then the
        positional arguments in arranged order.
    **kwargs : Any
        Keyword arguments forwarded unchanged.

    Returns
    -------
    Any
        Whatever the function returns.
    """
    func, args = args[0], args[1:]
    instance, args = (args[0], args[1:]) if args else (None, ())
    arrangement = self._getArrangement()
    return func(instance, *arrangement.restoreFrom(*args), **kwargs)
