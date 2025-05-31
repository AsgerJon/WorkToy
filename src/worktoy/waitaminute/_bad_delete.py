"""BadDelete is a temporary custom exception meant to be caught in
__delattr__. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class BadDelete(TypeError):
  """
  BadSet is a temporary custom class meant to be caught in __setattr__
  which raises a more precise error based on it.
  """

  instance = _Attribute()

  def __init__(self, instance: Any, ) -> None:
    """
    Initialize the BadSet instance.
    """
    self.instance = instance
