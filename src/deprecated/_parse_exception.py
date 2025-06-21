"""ParseException is a custom exception raised to indicate that a keyword
argument parsing scheme has failed. Callers should handle this exception
for example by moving on to another parsing scheme."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Self, TypeAlias


class ParseException(ValueError):
  """ParseException is a custom exception raised to indicate that a keyword
  argument parsing scheme has failed. Callers should handle this exception
  for example by moving on to another parsing scheme."""

  name = _Attribute()
  type_ = _Attribute()

  def __init__(self, name: str, type_: type) -> None:
    """Initialize the ParseException object."""
    self.name = name
    self.type_ = type_
    infoSpec = """Unable to parse argument '%s' of type '%s' whilst 
    parsing keyword arguments!"""
    info = monoSpace(infoSpec % (name, type_.__name__))
    ValueError.__init__(self, info)

  def __eq__(self, other: Any) -> bool:
    """Compare the ParseException object with another object."""
    cls = type(self)
    if isinstance(other, cls):
      if self.name == other.name:
        if self.type_ == other.type_:
          return True
    return False
