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

  def invoke(self, func, instance=None, *args, **kwargs) -> Any:
    """
    The 'invoke' method accepts the calling instance ahead of the
    reordered positional arguments, so a 'PermuterMethod' can wrap a
    bound method: 'instance' is forwarded first, then the arguments
    restored to canonical order.

    Parameters
    ----------
    func : Callable
        The wrapped function.
    instance : Any, optional
        The calling instance, forwarded as the first argument.
    *args : Any
        Positional arguments in arranged order.
    **kwargs : Any
        Keyword arguments forwarded unchanged.

    Returns
    -------
    Any
        Whatever 'func' returns.
    """
    return func(instance, *self.arrangement.restoreFrom(*args), **kwargs)
