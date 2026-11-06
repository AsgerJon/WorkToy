"""
PermuterMethod is a 'Permuter' that forwards the calling instance ahead
of the reordered positional arguments.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import Permuter

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class PermuterMethod(Permuter):
  """
  A flexible overload declared in a class body is a method: the first
  argument is the instance, which must stay first, and only the arguments
  after it may come in any order.

  Implementation
  --------------

  'invoke' takes the instance off the front and restores the remaining
  arguments through the arrangement, which therefore covers the
  parameters after 'self'.
  """

  def invoke(self, *args, **kwargs) -> Any:
    """
    The method must receive the instance first and its other positional
    arguments in the order it declares them.

    Implementation
    --------------

    The function and the instance are taken by position, so caller
    keywords named 'func' or 'instance' reach the function. With no
    positional argument at all, the instance is 'None'.

    Parameters
    ----------

    *args
      The function, the instance, then the remaining positional arguments
      in the order of 'arrangement.values'.

    **kwargs
      Keyword arguments.

    Returns
    -------

    Any
      What the function returns.
    """
    func, args = args[0], args[1:]
    instance, args = (args[0], args[1:]) if args else (None, ())
    arrangement = self._getArrangement()
    return func(instance, *arrangement.restoreFrom(*args), **kwargs)
