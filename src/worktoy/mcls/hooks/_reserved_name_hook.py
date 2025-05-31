"""ReservedNameHook protects reserved names. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ...waitaminute import ReservedName

from . import AbstractHook, ReservedNames

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class ReservedNameHook(AbstractHook):
  """ReservedNameHook protects reserved names."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public variables
  reservedNames = ReservedNames()

  def setItemHook(self, key: str, value: Any, oldValue: Any) -> bool:
    """The setItemHook method is called when an item is set in the
    namespace."""
    if key in self.reservedNames:
      if key in self.space:
        raise ReservedName(key)
    return False
