"""WorkToy - Wait A Minute! - SecretFieldError
Raised when attempting to read from a secret field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute import MetaXcept

if TYPE_CHECKING:
  Quick = lambda x: SecretFieldError


class SecretFieldError(MetaXcept):
  """WorkToy - Wait A Minute! - ProtectedFieldError
  Raised when attempting to delete a protected field."""

  def __init__(self, *args) -> None:
    MetaXcept.__init__(self, *args)
    self._secretField = args[0]
    self._targetObject = args[1]
    self._ownerClass = args[2]

  def __str__(self, ) -> str:
    """String Representation."""
    header = 'SecretFieldError!'
    body = """An attempt were made to read data from field %s from object 
    %s belonging to %s with insufficient permission level."""
    msg = body % (self._secretField, self._targetObject, self._ownerClass)
    return '%s\n%s' % (header, self.monoSpace(msg))
