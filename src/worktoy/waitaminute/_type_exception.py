"""TypeException is a custom exception raised on a type mismatch.
Specifically, it should NOT be raised when the object is 'None' instead of
the expected type, since 'None' indicates absence rather than a type
mismatch. Use 'MissingVariable' for the absence case.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt, joinWords

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TypeException(TypeError):
  """
  TypeException is a custom exception raised on a type mismatch. It is the
  most widely raised exception in 'worktoy', used wherever a value reaches
  a type-checked boundary as the wrong type.

  It should NOT be raised when the object is 'None' rather than the
  expected type; that case indicates absence and belongs to
  'MissingVariable'.

  Attributes
  ----------
  varName : str
    The name of the variable or argument that received the wrong type.
  actualObject : Any
    The object that was received.
  actualType : type
    The type of the received object, equal to 'type(actualObject)'.
  expectedTypes : tuple[type, ...]
    The types that would have been accepted, in the order given to the
    constructor.
  """

  __slots__ = ('varName', 'actualObject', 'actualType', 'expectedTypes',)

  def __init__(self, name: str, obj: Any, *types) -> None:
    TypeError.__init__(self, )
    self.varName = name
    self.actualObject = obj
    self.actualType = type(obj)
    self.expectedTypes = types

  def __str__(self) -> str:
    infoSpec = """Expected object at name '%s' to be an instance of %s, 
    but received object: '%s' of type '%s'!"""
    typeNames = [t.__name__ for t in self.expectedTypes]
    typeStr = joinWords(*["""'%s'""" % name for name in typeNames], sep='or')
    objStr = repr(self.actualObject)
    if len(objStr) > 50:
      objStr = """%s...""" % objStr[:47]
    clsType = type(self.actualObject).__name__
    info = infoSpec % (self.varName, typeStr, objStr, clsType)
    return textFmt(info)

  __repr__ = __str__
