"""The overload function returns a callable that decorates a function with
the signature. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable


def overload(*args, ):
  """The overload function returns a callable that decorates a function with
  the signature. """

  types = [a for a in args if isinstance(a, type)]

  def decorate(callMeMaybe: Callable) -> Callable:
    """Decorate the function with the given signature."""
    setattr(callMeMaybe, '__overloaded_signature__', (*types,))
    return callMeMaybe

  return decorate
