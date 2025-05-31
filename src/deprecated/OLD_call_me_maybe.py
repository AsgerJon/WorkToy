"""
CallMeMaybe is like typing.Callable except usable at runtime.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class CallMeMaybe:
  """CallMeMaybe is like typing.Callable except usable at runtime.

  It is used to represent a callable object that can be called with
  any number of arguments and keyword arguments.
  """

  def __instancecheck__(self, instance: Any) -> bool:
    """Check if the instance is callable."""
    return True if callable(instance) else False
