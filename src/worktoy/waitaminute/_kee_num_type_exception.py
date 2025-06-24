"""
KeeNumTypeException is a custom exception class raised to indicate a
member of a KeeNum enumeration with inconsistent value type.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

from typing import TYPE_CHECKING

from ..text import monoSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class KeeNumTypeException(TypeError):
  """
  KeeNumTypeException is a custom exception class raised to indicate a
  member of a KeeNum enumeration with inconsistent value type.
  """
  memberName = _Attribute()
  memberValue = _Attribute()
  expectedType = _Attribute()

  def __init__(self, name: str, value: Any, expectedType: type) -> None:
    """Initialize the KeeNumTypeException object."""
    self.memberName = name
    self.memberValue = value
    self.expectedType = expectedType
    TypeError.__init__(self, )

  def __str__(self, ) -> str:
    """Return the string representation of the KeeNumTypeException object."""
    infoSpec = """KeeNum member '%s' has value '%s' of type '%s', but 
    expected type is '%s'!"""
    name = self.memberName
    value = str(self.memberValue)
    valueType = type(self.memberValue).__name__
    expType = self.expectedType.__name__
    info = infoSpec % (name, value, valueType, expType)
    return monoSpace(info)

  __repr__ = __str__
