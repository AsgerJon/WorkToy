"""MissingAccessorException is a subclass of the AttributeError exception.
It is raised when an accessor is missing from a descriptor. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.mcls import CallMeMaybe


class MissingAccessorException(AttributeError):
  """MissingAccessorException is a subclass of the AttributeError exception.
  It is raised when an accessor is missing from a descriptor. """

  def __init__(self, instance: object, accessor: CallMeMaybe) -> None:
    fieldNameGet = getattr(instance, 'getFieldName', None)
    accessorName = getattr(accessor, '__name__', None)
    if fieldNameGet is None or accessorName is None:
      AttributeError.__init__(self)
    else:
      fieldName = fieldNameGet()
      e = """The accessor method '%s' is missing from the descriptor '%s'!"""
      AttributeError.__init__(self, monoSpace(e % (accessorName, fieldName)))
