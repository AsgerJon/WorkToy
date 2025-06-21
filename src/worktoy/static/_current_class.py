"""
_CurrentClass exposes the current class through the descriptor protocol.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
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
