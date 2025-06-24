"""_CurrentOwner is a private method used by AbstractObject to expose
the current owner of the descriptor instance."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..waitaminute import attributeErrorFactory
from ..waitaminute import ProtectedError, ReadOnlyError

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never
  from . import AbstractObject


class _CurrentOwner:
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
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(instance, AbstractObject)
    if instance.__current_owner__ is None:
      if instance.__field_owner__ is None:
        return None
      return instance.__field_owner__
    return instance.__current_owner__

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


class _OwnerAddress(_CurrentOwner):
  """_OwnerAddress is a private method used by AbstractObject to expose
  the address of the current owner of the descriptor instance."""

  def __get__(self, instance: Any, owner: type) -> Any:
    """
    Returns 'self' if 'instance' is 'None', otherwise returns the 'id' of
    the object at the super call.
    """
    if instance is None:
      return self
    return id(_CurrentOwner.__get__(self, instance, owner))
