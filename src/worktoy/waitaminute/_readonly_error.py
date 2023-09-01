"""WorkToy - Wait A Minute! - ReadOnlyError
Exception raised by trying to set the value of a protected field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute import SecretFieldError
from worktoy.waitaminute import MetaXcept

if TYPE_CHECKING:
  pass


class ReadOnlyError(SecretFieldError):
  """WorkToy - Wait A Minute! - ReadOnlyError
  Exception raised by trying to set the value of a protected field."""

  def __init__(self, *args, **kwargs) -> None:
    SecretFieldError.__init__(self, *args, **kwargs)

  def __str__(self, ) -> str:
    """String Representation."""
    header = MetaXcept.__str__(self)
    field = self._field
    obj = self._targetObject
    newValue = self._newValue

    msg = """Attempted to overwrite field '%s' on object '%s' with 
    new value '%s' with insufficient permission level!"""
    body = msg % (field, obj, newValue)
    return '%s\n%s' % (header, self.justify(body))
