"""WorkToy - Wait A Minute! - SecretFieldError
Raised when attempting to read from a secret field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from worktoy.waitaminute import MetaXcept

if TYPE_CHECKING:
  from worktoy.fields import AbstractDescriptor


class SecretFieldError(MetaXcept):
  """WorkToy - Wait A Minute! - ProtectedFieldError
  Raised when attempting to delete a protected field."""

  def __init__(self, field: AbstractDescriptor, obj: any, cls: type,
               newValue: Any = None, *args, **kwargs) -> None:
    MetaXcept.__init__(self, field, obj, cls, *args, **kwargs)
    self._field = self.pretty(field)
    self._targetObject = self.pretty(obj)
    self._ownerClass = self.pretty(cls)
    self._newValue = self.pretty(newValue)

  def __str__(self, ) -> str:
    """String Representation."""
    header = MetaXcept.__str__(self)
    field = self._field
    obj = self._targetObject
    cls = self._ownerClass

    body = """Attempted to read data from secret field '%s' from object 
    '%s' on class '%s' with insufficient permission level!"""
    body = body % (field, obj, cls)
    return '%s\n%s' % (header, self.justify(body))
