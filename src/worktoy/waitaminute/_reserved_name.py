"""ReservedName is raised to indicate that a used name is reserved."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


class ReservedName(Exception):
  """ReservedName is raised to indicate that a used name is reserved."""

  __reserved_name__ = None

  def __init__(self, name: str) -> None:
    """Initialize the ReservedName exception."""
    info = """Attempted to use the reserved name: '%s'!"""
    self.__reserved_name__ = name
    Exception.__init__(self, info % name)
