"""VariableNotNone should be raised when a variable is unexpectedly not
None."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..text import monoSpace

from . import _Attribute

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional, Self


class VariableNotNone(Exception):
  """VariableNotNone should be raised when a variable is unexpectedly not
  None."""

  name = _Attribute()
  value = _Attribute()

  def __init__(self, _name: str, _value: Any) -> None:
    """Initialize the VariableNotNone object."""
    self.name, self.value = _name, _value
    Exception.__init__(self, )

  def __str__(self, ) -> str:
    """Get the info spec."""
    infoSpec = """Unexpected value: '%s' at name '%s' expected to be 
    None!"""
    valueStr = monoSpace(str(self.value), )
    name = self.name
    return monoSpace(infoSpec % (valueStr, name), )

  __repr__ = __str__
