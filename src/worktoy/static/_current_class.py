"""
_CurrentClass exposes the current class through the descriptor protocol.
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
  from typing import Any, Never

  from . import AbstractObject


class _CurrentClass:
  """
  _CurrentClass exposes the current class through the descriptor protocol.
  """

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    Get the current class.
    """
    if instance is None:
      return self
    return owner
