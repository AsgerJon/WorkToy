"""
_CurrentModule exposes the current module through the descriptor protocol.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never

  from . import AbstractObject


class _CurrentModule:
  """
  _CurrentModule exposes the current module through the descriptor protocol.
  """

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    Get the current module.
    """
    if instance is None:
      return self
    return owner.__module__
