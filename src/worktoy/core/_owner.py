"""_CurrentOwner is a private method used by AbstractObject to expose
the current owner of the descriptor instance."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import Object
from ..waitaminute import ProtectedError, ReadOnlyError

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never


class Owner(Object):
  """
  _CurrentOwner is a private method used by AbstractObject to expose
  the current owner of the descriptor instance.
  """

  def __get__(self, instance: Any, owner: type) -> Any:
    """
    Return the current owner of the descriptor instance.
    """
    if instance is None:
      return self
    return getattr(instance, '__field_owner__', None)

  def __set__(self, instance: Any, value: Any) -> Never:
    """
    This should never happen.
    """
    raise ReadOnlyError(instance, self, None)

  def __delete__(self, instance: Any) -> Never:
    """
    Illegal deleter operation
    """
    raise ProtectedError(instance, self, None)
