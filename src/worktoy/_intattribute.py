"""WorkToy - IntAttribute
Integer valued attribute"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import NumAttribute


class IntAttribute(NumAttribute):
  """WorkToy - IntAttribute
  Integer valued attribute"""

  def __init__(self, *args, **kwargs) -> None:
    defKeys = self.stringList('value, defVal, default')
    defValKwarg = self.firstKey(int, defKeys, **kwargs)
    defValArg = self.maybeType(int, *args)
    defDefault = ''
    defVal = int(self.maybe(defValKwarg, defValArg, defDefault))
    NumAttribute.__init__(self, type_=int, defVal=defVal)

  def _typeCheck(self, value: object) -> bool:
    """Implementation tests if given value is an integer."""
    return True if isinstance(value, float) else False

  def _typeGuard(self, value: int) -> int:
    """Ensures that value is an integer. If not, it attempts to convert value
    to an integer."""
    if self._typeCheck(value):
      return value
    if isinstance(value, float):
      sign = 1 if value > 0 else (-1 if value < 0 else 0)
      value *= sign
      return sign * int((value * 10 ** 12) // (10 ** 12))
    if isinstance(value, str):
      return self.string2Int(value)
