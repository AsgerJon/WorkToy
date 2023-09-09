"""WorkToy - Descriptors - StrAttribute
String valued attribute descriptor implementation."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.descriptors import AbstractAttribute


class StrAttribute(AbstractAttribute):
  """WorkToy - Fields - IntAttribute
  Field implementation of integer valued descriptor."""

  def __init__(self, value: int = None, *args, **kwargs) -> None:
    AbstractAttribute.__init__(self, *args, **kwargs)

  def getDefaultValue(self) -> str:
    return ''

  def getType(self) -> type:
    """Getter-function for value type."""
    return str

  def explicitGetter(self, obj: Any, cls: type = None) -> str:
    """Explicit getter function. """
    return self.__attribute_value__

  def explicitSetter(self, obj: Any, newValue: str) -> None:
    """Explicit setter function."""
    self.__attribute_value__ = newValue

  def explicitDeleter(self, obj: Any, ) -> None:
    """Explicit deleter function."""
    delattr(obj, self.getPrivateName())
