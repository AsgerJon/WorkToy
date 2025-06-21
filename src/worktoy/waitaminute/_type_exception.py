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


def _resolveTypeNames(*types) -> str:
  """Creates the first part of the error message listing the expected type
  or types. """
  if len(types) == 1:
    if isinstance(types[0], (tuple, list)):
      return _resolveTypeNames(*types[0])
    if isinstance(types[0], type):
      expName = types[0].__name__
    elif isinstance(types[0], str):
      expName = types[0]
    else:
      raise TypeError("""Received bad arguments: %s""" % (str(types),))
    return """Expected object of type '%s'""" % (expName,)
  typeNames = []
  for type_ in types:
    if isinstance(type_, type):
      typeNames.append("""'%s'""" % type_.__name__)
    elif isinstance(type_, str):
      typeNames.append("""'%s'""" % type_)
    else:
      raise TypeError("""Received bad arguments: %s""" % (str(types),))
  infoSpec = """Expected object of any of the following types: %s"""
  typeStr = joinWords(*typeNames, sep='or')
  return monoSpace(infoSpec % (typeStr,))


class _Meta(type):
  """Metaclass simplifying __str__ and __repr__"""

  def __str__(cls) -> str:
    """String representation of the class."""
    return cls.__name__

  def __repr__(cls) -> str:
    """Representation of the class."""
    return cls.__name__


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
    prelude = _resolveTypeNames(*self.expectedType)
    actName = type(self.actualObject).__name__
    actRepr = repr(self.actualObject)
    infoSpec = """%s at name: '%s', but received object of type '%s' with 
    repr: '%s'"""
    info = infoSpec % (prelude, self.varName, actName, actRepr)
    return monoSpace(info)

  __repr__ = __str__
