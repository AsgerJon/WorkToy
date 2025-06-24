"""TypeException is a custom exception class for handling type related
errors. Specifically, this exception should NOT be raised if the object is
None instead of the expected type. This is because None indicates absense
rather than type mismatch. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import monoSpace, joinWords

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class TypeException(TypeError):
  """
  TypeException is a custom exception class for handling type related
  errors. Specifically, this exception should NOT be raised if the object is
  None instead of the expected type.
  """

  varName = _Attribute()
  actualObject = _Attribute()  # This is the object that was received
  actualType = _Attribute()
  expectedType = _Attribute()

  def __init__(self, name: str, obj: object, *types) -> None:
    """Initialize the TypeException with the name of the variable, the
    received object, and the expected types."""
    TypeError.__init__(self, )
    self.varName = name
    self.actualObject = obj
    self.actualType = type(obj)
    self.expectedType = types

  def __str__(self) -> str:
    """String representation of the TypeException."""
    spec = """%s! Expected type of variable '%s' to be one of: (%s), 
    but received '%s' of type '%s'!"""
    cls = type(self).__name__
    exp = ', '.join([t.__name__ for t in self.expectedType])
    valStr = ('%50s' % repr(self.actualObject))[:50].replace(' ', '')
    valType = type(self.actualObject).__name__
    info = spec % (cls, self.varName, exp, valStr, valType)
    return monoSpace(info)

  __repr__ = __str__
