"""WorkToy - Wait A Minute! - ProtectedFieldError
Raised when attempting to delete a protected field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute import MetaXcept

if TYPE_CHECKING:
  from worktoy.fields import AbstractDescriptor


class ProtectedFieldError(MetaXcept):
  """WorkToy - Wait A Minute! - ProtectedFieldError
  Raised when attempting to delete a protected field."""

  def __init__(self, field: AbstractDescriptor, obj: object,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, field, obj, *args, **kwargs)
    self._protectedField = self.pretty(field)
    self._targetObject = self.pretty(obj)

  def __str__(self, ) -> str:
    """String Representation."""

    header = MetaXcept.__str__(self)

    field = self._protectedField
    obj = self._targetObject

    msg = """Attempted to delete field '%s' from object '%s' with 
    insufficient permission level!""" % (field, obj)

    return '%s\n%s' % (header, self.justify(msg))
