"""WorkToy - StrAttribute
String valued attribute"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import ImmutableAttribute


class StrAttribute(ImmutableAttribute):
  """WorkToy - StrAttribute
  String valued attribute"""

  def __init__(self, *args, **kwargs) -> None:
    defKeys = self.stringList('defVal, value, text')
    defValKwarg = self.firstKey(str, defKeys, **kwargs)
    defValArg = self.maybeType(str, *args)
    defDefault = ''
    defVal = str(self.maybe(defValKwarg, defValArg, defDefault))
    ImmutableAttribute.__init__(self, type_=str, defVal=defVal)

  def _typeCheck(self, value: object) -> bool:
    """Implementation tests if given value is a string"""
    return True if isinstance(value, str) else False

  def _typeGuard(self, value: str) -> str:
    """Ensures that the attribute does not somehow point at something
    other than a list."""
    if self._typeCheck(value):
      return value
    return str(value)
