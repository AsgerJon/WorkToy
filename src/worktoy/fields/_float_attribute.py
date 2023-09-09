"""WorkToy - Fields - FloatAttribute
Float valued attribute descriptor implementation."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.fields import Attribute


class FloatAttribute(Attribute):
  """WorkToy - Fields - IntAttribute
  Field implementation of integer valued descriptor."""

  def __init__(self, value: int = None, *args, **kwargs) -> None:
    Attribute.__init__(self, *args, **kwargs)

  def getDefaultValue(self) -> float:
    return .0

  def getType(self) -> type:
    """Getter-function for value type."""
    return float

  def explicitGetter(self, obj: Any, cls: type = None) -> float:
    """Explicit getter function. """
    return self.__attribute_value__

  def explicitSetter(self, obj: Any, newValue: float) -> None:
    """Explicit setter function."""
    self.__attribute_value__ = newValue

  def explicitDeleter(self, obj: Any, ) -> None:
    """Explicit deleter function."""
    delattr(obj, self.getPrivateName())
