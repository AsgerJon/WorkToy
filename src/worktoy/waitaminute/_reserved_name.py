"""ReservedName is raised to indicate that a used name is reserved."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

from typing import TYPE_CHECKING

from ..text import monoSpace

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

  def __str__(self) -> str:
    """
    String representation of the ReservedName exception.
    """
    infoSpec = """Attempted to use reserved name: '%s'!"""
    info = infoSpec % self.resName
    return monoSpace(info)

  __repr__ = __str__
