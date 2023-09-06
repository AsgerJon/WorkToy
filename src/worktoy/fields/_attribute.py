"""WorkToy - Fields - Attribute
Basic getter, setter implementation of descriptors. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.base import DefaultClass


class Attribute(DefaultClass):
  """Getter-Only"""

  def __init__(self, defVal: Any = None, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._defaultValue = self.maybe(defVal, None)
    self._fieldName = None
    self._fieldOwner = None

  def __set_name__(self, cls: type, name: str) -> None:
    self._fieldName = name
    self._fieldOwner = cls

  def __get__(self, obj: Any, cls: type) -> Any:
    value = getattr(obj, self.getPrivateName(), None)
    if value is not None:
      return value
    setattr(obj, self.getPrivateName(), self._defaultValue)
    return self._defaultValue

  def __set__(self, obj: Any, newValue: Any) -> None:
    setattr(obj, self.getPrivateName(), newValue)

  def getPrivateName(self) -> str:
    """Getter-function for the name of the private variable."""
    return '_%s' % self._fieldName
