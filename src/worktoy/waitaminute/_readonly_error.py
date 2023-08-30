"""WorkToy - Wait A Minute! - ReadOnlyError
Exception raised by trying to set the value of a protected field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute import MetaXcept

if TYPE_CHECKING:
  Quick = lambda x: ReadOnlyError


class ReadOnlyError(MetaXcept):
  """WorkToy - Wait A Minute! - ReadOnlyError
  Exception raised by trying to set the value of a protected field."""

  def __init__(self, *args) -> None:
    MetaXcept.__init__(self, *args)
    self._readOnlyField = args[0]
    self._targetObject = args[1]
    self._newValue = args[2]

  def __str__(self, ) -> str:
    """String Representation."""
    m = """Attempted to overwrite value of field %s on object %s with 
    new value %s without necessary permission level!"""
    msg = m % (self._readOnlyField, self._targetObject, self._newValue)
    return self.monoSpace(msg)
