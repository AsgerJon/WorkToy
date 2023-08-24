"""WorkToy - ParsingClass
Utility class inherited by DefaultClass focused on parsing."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import PrimitiveClass, Function


class ParsingClass(PrimitiveClass):
  """WorkToy - ParsingClass
  Utility class inherited by DefaultClass focused on parsing."""

  def __init__(self, *args, **kwargs) -> None:
    PrimitiveClass.__init__(self, *args, **kwargs)

  def parseFactory(self, type_: type, *keys) -> Function:
    """Creates a parsing function"""

    def parseKeyType(instance: ParsingClass, *args, **kwargs) -> list:
      """Parses for keys and types given in positional arguments. Roughly
      speaking, then types are used to find positional arguments and
      strings are used to find keyword arguments:"""
      typeValues = self.maybeTypes(type, *args)
      keyValues = self.maybeTypes(str, *args)
      types = (*typeValues,) or (object,)
      out = []
      for arg in args:
        if isinstance(arg, types):
          out.append(arg)
      for key in keyValues:
        val = kwargs.get(key, None)
        if val is not None and isinstance(val, types):
          out.append(val)
      return out

    return parseKeyType

  def parseKey(self, *args, **kwargs) -> object:
    """Finds keys and a type in the positional arguments and returns the
    first value from the keyword arguments whose key is one of the keys
    found, and whose type is of the type found. Setting a type test is
    optional. """
    type_ = self.maybeType(type, *args)
    if not isinstance(type_, type):
      type_ = object
    keys = self.maybeTypes(str, *args)
    for key in keys:
      val = kwargs.get(key, None)
      if val is not None and isinstance(val, type_):
        return val

  def parseKeys(self, *args, **kwargs) -> list:
    """Same as parseKey, but finds every value matching a key and
    belonging to the type if present. """
    type_ = self.maybeType(type, *args)
    if not isinstance(type_, type):
      type_ = object
    keys = self.maybeTypes(str, *args)
    out = []
    for key in keys:
      val = kwargs.get(key, None)
      if val is not None and isinstance(val, type_):
        out.append(out)
    return out
