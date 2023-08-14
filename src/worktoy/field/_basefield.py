"""Field provides a convenient way to set data fields on classes"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from worktoy.field import AbstractField, PermissionLevel
from worktoy.waitaminute import ReadOnlyError, ProtectedPropertyError


class BaseField(AbstractField):
  """Field subclasses AbstractField. It is particularly well suited for
  use with classes of metaclass WorkType."""

  @classmethod
  def _getPermissionLevel(cls) -> PermissionLevel:
    """Implementation allowing setting and reading, but not deleting"""
    return PermissionLevel.PROTECTED

  def __init__(self, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)
    self._owner = None
    self._ownerName = None

  def _getOwnerName(self, ) -> str:
    """Getter-function for the name of the class on which this field is
    defined."""
    return self._ownerName

  def _setOwnerName(self, name: str) -> None:
    """Setter-function for the name of the class on which this field is
    defined."""
    if self._ownerName is not None:
      raise ReadOnlyError('ownerName')
    self._ownerName = name

  def _delOwnerName(self, ) -> Never:
    """Illegal deleter function"""
    raise ProtectedPropertyError('ownerName')

  def _getOwner(self, ) -> type:
    """Getter-function for owner class"""
    if isinstance(self._owner, str):
      owner = globals().get(self._owner, None)
      if owner is not None:
        self.owner = owner
    return self._owner

  def _setOwner(self, owner: type) -> None:
    """Setter-function for the owner class"""
    if self._owner is not None:
      raise ReadOnlyError('owner')
    self._owner = owner

  def _delOwner(self) -> Never:
    """Illegal deleter function"""
    raise ProtectedPropertyError('owner')

  ownerName = property(_getOwnerName, _setOwnerName, _delOwnerName)
  owner = property(_getOwner, _setOwner, _delOwner)
