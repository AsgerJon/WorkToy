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

  def __init__(self, *args) -> None:
    """Initialize the VariableNotNone object."""
    _name, _value = None, None
    for arg in args:
      if isinstance(arg, str):
        if _name is None:
          _name = arg
          continue
      if _value is None:
        _value = arg
        break
    if _name is not None:
      self.name = _name
    if _value is not None:
      self.value = _value
    Exception.__init__(self, )

  def __str__(self, ) -> str:
    """Get the info spec."""
    if self.name is None and self.value is None:
      infoSpec = """Unexpected value at name expected to be None!%s%s"""
      name, valueStr = '', ''
    elif self.name is None:
      infoSpec = """Unexpected value: '%s' at name expected to be 
      None!%s"""
      name = ''
      valueStr = monoSpace(str(self.value), )
    elif self.value is None:
      infoSpec = """Unexpected value at name '%s' expected to be 
      None!"""
      name = self.name
      valueStr = ''
    else:
      infoSpec = """Unexpected value: '%s' at name '%s' expected to be 
      None!"""
      valueStr = monoSpace(str(self.value), )
      name = self.name
    return monoSpace(infoSpec % (valueStr, name), )

  __repr__ = __str__
