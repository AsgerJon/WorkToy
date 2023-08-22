"""WorkToy - DictAttribute
Dictionary valued attribute"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import MutableAttribute


class DictAttribute(MutableAttribute):
  """WorkToy - DictAttribute
  Dictionary valued attribute"""

  def __init__(self, *args, **kwargs) -> None:
    MutableAttribute.__init__(self, type_=dict, defVal=dict(**kwargs))

  def _typeCheck(self, value: object) -> bool:
    """This method simply tests if value is a dict"""
    return True if isinstance(value, dict) else False

  def _typeGuard(self, value: dict) -> dict:
    """Ensures that the attribute does not somehow point at something
    other than a dict."""
    if self._typeCheck(value):
      return value
    raise self.TypeException
