"""PermissionLevel provides an Enum class representation of the
implemented permission levels."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import Never

from worktoy.core import maybe
from worktoy.stringtools import monoSpace

from worktoy.waitaminute import ProtectedPropertyError, ReadOnlyError


class PermissionLevel(Enum):
  """This enum defines a permission level for an instance of Field"""

  SECRET = 0
  READ_ONLY = 1
  PROTECTED = 2
  UNRESTRICTED = 3

  @classmethod
  def getFromValue(cls, value: int) -> PermissionLevel:
    """Getter-function for the instance having given value"""
    if -1 < value < 4:
      if not value:
        return cls.SECRET
      if value == 1:
        return cls.READ_ONLY
      if value == 2:
        return cls.PROTECTED
      if value == 3:
        return cls.UNRESTRICTED
    e = """%s provides only instances of values from 0 to 3 inclusive, 
    but received %d!""" % value
    raise ValueError(monoSpace(e))

  @classmethod
  def getFromAccess(cls, access: str) -> PermissionLevel:
    """Getter-function for the lowest permission level permitted the given
    access"""
    p = dict(none=0, getter=1, setter=2, delete=3)
    return cls.getFromValue(p[maybe(access, 'none')])

  @classmethod
  def _getDescriptions(cls, ) -> list[str]:
    """Getter-function for enum descriptions"""
    out = [
      r"""No access to read the content of the property. Please note 
      that the property still appears in as a property, but where no 
      accessor functions are available. Also, the type of the variable is 
      also available. """,
      r"""Access to read the variable, but not to set or delete the 
      variable""",
      r"""Access to read and edit the the variable, but not to delete it.""",
      r"""Unrestricted access. This grants access to the delete function, 
      which in this implementation replaces the contents with None."""
    ]
    return [monoSpace(desc) for desc in out]

  def _getAllowRead(self) -> bool:
    """Getter-function for read access"""
    return True if self.value > 0 else False

  def _setAllowRead(self, *_) -> Never:
    """LOL, you don't have access to edit the access of Permissions. It's
    too crazy!"""
    raise ReadOnlyError('allowRead')

  def _delAllowRead(self) -> Never:
    """LOL, you don't have access to delete the access of Permissions. It's
    too crazy!"""
    raise ProtectedPropertyError('allowRead')

  def _getAllowEdit(self) -> bool:
    """Getter-function for edit access"""
    return True if self.value > 1 else False

  def _setAllowEdit(self, *_) -> Never:
    """LOL, you don't have access to edit the access of Permissions. It's
    too crazy!"""
    raise ReadOnlyError('allowEdit')

  def _delAllowEdit(self) -> Never:
    """LOL, you don't have access to delete the access of Permissions. It's
    too crazy!"""
    raise ProtectedPropertyError('allowEdit')

  def _getAllowDelete(self) -> bool:
    """Getter-function for delete access"""
    return True if self.value > 2 else False

  def _setAllowDelete(self, *_) -> Never:
    """LOL, you don't have access to Delete the access of Permissions. It's
    too crazy!"""
    raise ReadOnlyError('allowDelete')

  def _delAllowDelete(self) -> Never:
    """LOL, you don't have access to delete the access of Permissions. It's
    too crazy!"""
    raise ProtectedPropertyError('allowDelete')

  canGet = property(_getAllowRead, _setAllowRead, _delAllowRead)
  canSet = property(_getAllowEdit, _setAllowEdit, _delAllowEdit)
  canDel = property(_getAllowDelete, _setAllowDelete, _delAllowDelete)

  def __repr__(self) -> str:
    """Code Representation"""
    return '%s.%s' % (self.__class__.__qualname__, self.name)

  def __str__(self) -> str:
    """String Representation"""
    return '%s: %s' % (self.name, self._getDescriptions()[self.value])
