"""ReservedName is raised to indicate that a used name is reserved."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class ReservedName(Exception):
  """ReservedName is raised to indicate that a used name is reserved."""

  resName = _Attribute()

  def __init__(self, name: str) -> None:
    """Initialize the ReservedName object."""
    self.resName = name
    info = """Attempted to use reserved name: '%s'!"""
    Exception.__init__(self, info % name)

  def _resolveOther(self, other: Any) -> ReservedName:
    """Resolve the other object."""
    cls = type(self)
    if isinstance(other, cls):
      return other
    if isinstance(other, (tuple, list)):
      try:
        return cls(*other)
      except TypeError:
        return NotImplemented
    return NotImplemented

  def __eq__(self, other: object) -> bool:
    """Compare the ReservedName object with another object."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return False
    cls = type(self)
    if isinstance(other, cls):
      if self.resName != other.resName:
        return False
      return True
    return False
