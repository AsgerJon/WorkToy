"""WorkToy - Fields - Field
Property like class"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from icecream import ic

from worktoy.base import DefaultClass
from worktoy.core import Function

ic.configureOutput(includeContext=True)


class AbstractField(DefaultClass):
  """WorkToy - Fields - Field
  Property like class"""

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._defaultValue = self.maybe(*args, None)
    self._fieldName = None
    self._fieldOwner = None

  def __set_name__(self, cls: type, name: str) -> None:
    self._fieldName = name
    self._fieldOwner = cls

  def getDefaultValue(self) -> Any:
    """Getter-function for default value."""
    return self._defaultValue

  def getPrivateName(self, ) -> str:
    """Getter-function for private name. """
    return '_%s' % self._fieldName

  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Wraps the inner getter function. """
    out = getattr(obj, self.getPrivateName(), None)
    if out is None:
      if obj is not None:
        setattr(obj, self.getPrivateName(), self.getDefaultValue())
      return self.getDefaultValue()
    return out

  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Wraps the inner setter function. """
    setattr(obj, self.getPrivateName(), newValue)

  def explicitDeleter(self, obj: object, ) -> None:
    """Wraps the inner setter function. """
    delattr(obj, self.getPrivateName(), )

  def __get__(self, obj: object, cls: type) -> Any:
    """Getter-function. """
    return self.explicitGetter(obj, cls)

  def __set__(self, obj: object, newValue: object) -> None:
    """Getter-function."""
    return self.explicitSetter(obj, newValue)

  def __delete__(self, obj: object) -> None:
    """Deleter-function."""
    return self.explicitDeleter(obj)
