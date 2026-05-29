"""
KeeTypeException is raised when a 'KeeNum' member's value type does not
match the value type established by the enumeration's first member.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class KeeTypeException(TypeError):
  """
  Raised when a 'KeeNum' member's value type does not match the value
  type established by the enumeration's first member; all members must
  share one value type.

  Attributes
  ----------
  name : str
    The name of the member whose value had the wrong type.
  value : Any
    The value that was rejected.
  expectedTypes : tuple of type
    The accepted type(s) for member values.
  """

  __slots__ = ('name', 'value', 'expectedTypes')

  def __init__(self, name: str, value: Any, *types) -> None:
    self.name = name
    self.value = value
    self.expectedTypes = types
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """KeeNum member '%s' has value '%s' of type '%s', but
    expected type to be: '%s'!"""
    name = self.name
    typeNames = [t.__name__ for t in self.expectedTypes]
    from ...utilities import joinWords, textFmt
    typeStr = joinWords(*["""'%s'""" % name for name in typeNames], )
    value = str(self.value)
    valueType = type(self.value).__name__
    info = infoSpec % (name, value, valueType, typeStr)
    return textFmt(info)

  __repr__ = __str__
