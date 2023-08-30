"""WorkToy - Wait A Minute! - ProtectedFieldError
Raised when attempting to delete a protected field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute import MetaXcept

if TYPE_CHECKING:
  Quick = lambda x: ProtectedFieldError
  from worktoy.fields import AbstractDescriptor


class ProtectedFieldError(MetaXcept):
  """WorkToy - Wait A Minute! - ProtectedFieldError
  Raised when attempting to delete a protected field."""

  def __init__(self, field: AbstractDescriptor, obj: object) -> None:
    MetaXcept.__init__(self, field, obj)
    self._protectedField = field
    self._targetObject = obj

  def __str__(self, ) -> str:
    """String Representation."""
    msg = self.monoSpace("""An attempt were made to delete the field %s 
    from object %s with insufficient permission level!""")
    return msg % (self._protectedField, self._targetObject)
