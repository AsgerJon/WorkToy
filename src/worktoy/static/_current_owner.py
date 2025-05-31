"""_CurrentOwner is a private method used by AbstractObject to expose
the current owner of the descriptor instance."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..waitaminute import MissingVariable

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


class _CurrentOwner:
  """_CurrentOwner is a private method used by AbstractObject to expose
  the current owner of the descriptor instance."""

  def __get__(self, instance: Any, owner: type) -> Any:
    """Return the current owner of the descriptor instance."""
    if instance is None:
      return self
    if TYPE_CHECKING:
      assert isinstance(instance, AbstractObject)
    if instance.__current_owner__ is None:
      if instance.__field_owner__ is None:
        return None
      return instance.__field_owner__
    return instance.__current_owner__

  def __set__(self, *_) -> Never:
    """This should never happen."""
    raise RuntimeError

  def __delete__(self, *_) -> Never:
    """This should never happen."""
    raise RuntimeError
