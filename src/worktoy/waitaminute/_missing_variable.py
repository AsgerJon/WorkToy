"""MissingVariable exception should be raised when a variable is missing
and requires initialization. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import joinWords, monoSpace

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class MissingVariable(AttributeError):
  """MissingVariable exception should be raised when a variable is missing
  and requires initialization. """

  varName = _Attribute()
  varType = _Attribute()

  def __init__(self, name: str, *types) -> None:
    """Initialize the MissingVariable object."""
    self.varName = name
    self.varType = types
    AttributeError.__init__(self, )

  def __str__(self, ) -> str:
    """Return the string representation of the MissingVariable object."""
    infoSpec = """Missing variable '%s' of any of the following types: 
    %s"""
    typeNames = [type_.__name__ for type_ in self.varType]
    typeStr = joinWords(*typeNames, sep='or')
    info = infoSpec % (self.varName, typeStr)
    return monoSpace(info)

  __repr__ = __str__
