"""WorkToy - FloatAttribute
  Floating point valued attribute"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import NumAttribute


class FloatAttribute(NumAttribute):
  """WorkToy - FloatAttribute
    Floating point valued attribute"""

  def __init__(self, *args, **kwargs) -> None:
    defKeys = self.stringList('value, defVal, default')
    defValKwarg = self.firstKey(float, defKeys, **kwargs)
    defValArg = self.maybeType(float, *args)
    defDefault = ''
    defVal = float(self.maybe(defValKwarg, defValArg, defDefault))
    NumAttribute.__init__(self, type_=float, defVal=defVal or 0)

  def _typeCheck(self, value: object) -> bool:
    """Implementation tests if given value is a float"""
    return True if isinstance(value, float) else False

  def _typeGuard(self, value: float) -> float:
    """Ensures that value is a float. If not, it attempts to convert value
    to a float."""
    if self._typeCheck(value):
      return value
    if isinstance(value, int):
      return float(value)
    if isinstance(value, str):
      return self.string2Float(value)
    converter = getattr(value, '__float__', None)
    if not callable(converter):
      raise self.TypeException
