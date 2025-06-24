"""WriteOnceError is a custom error class raised to indicate that a
variable was attempted to be written to more than once."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..text import monoSpace

from . import _Attribute

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class WriteOnceError(Exception):
  """WriteOnceError is a custom error class raised to indicate that a
  variable was attempted to be written to more than once."""

  varName = _Attribute()
  oldValue = _Attribute()
  newValue = _Attribute()

  def __init__(self, name: str, oldVal: Any, newVal: Any) -> None:
    """Initialize the WriteOnceError with a name, old value and new value."""
    self.varName = name
    self.oldValue = oldVal
    self.newValue = newVal
    Exception.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """Attempted to overwrite variable '%s' having value '%s' to 
    new value '%s'"""
    oldStr = str(self.oldValue)
    newStr = str(self.newValue)
    info = infoSpec % (self.varName, oldStr, newStr)
    return monoSpace(info)

  __repr__ = __str__
