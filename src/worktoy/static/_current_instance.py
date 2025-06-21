"""_CurrentInstance is a private method used by AbstractObject to expose
the current owning instance of the descriptor instance."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..waitaminute import attributeErrorFactory
from ..waitaminute import ProtectedError, ReadOnlyError

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


class _CurrentInstance:
  """_CurrentInstance is a private method used by AbstractObject to
  expose
  the current owning instance of the descriptor instance."""

  def __get__(self, desc: Any, owner: type) -> Any:
    """Return the current owning instance of the descriptor instance."""
    if desc is None:
      return self
    if TYPE_CHECKING:
      assert isinstance(desc, AbstractObject)
    return desc.__current_instance__

  def __set__(self, instance: Any, value: Any) -> Never:
    """
    Raises 'ReadOnlyError'
    """
    try:
      currentInstance = instance.__current_instance__
    except Exception as exception:
      currentInstance = exception
      raise ReadOnlyError(instance, self, None) from currentInstance
    else:
      raise ReadOnlyError(instance, self, currentInstance)

  def __delete__(self, instance: Any) -> Never:
    """
    Raises 'ProtectedError'
    """
    try:
      currentInstance = instance.__current_instance__
    except Exception as exception:
      cls, name = type(instance), '__current_instance__'
      attributeError = attributeErrorFactory(cls, name)
      raise attributeError from exception
    else:
      raise ProtectedError(instance, self, currentInstance)


class _InstanceAddress(_CurrentInstance):
  """_InstanceAddress is a private method used by AbstractObject to
  expose the address of the current owning instance of the descriptor
  instance."""

  def __get__(self, desc: Any, owner: type) -> Any:
    """Return the address of the current owning instance of the
    descriptor instance."""
    if desc is None:
      return self
    return id(_CurrentInstance.__get__(self, desc, owner))
