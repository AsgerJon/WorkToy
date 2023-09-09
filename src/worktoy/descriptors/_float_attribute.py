"""WorkToy - Descriptors - FloatAttribute
Float valued attribute descriptor implementation."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.descriptors import AbstractAttribute


class FloatAttribute(AbstractAttribute):
  """WorkToy - Fields - IntAttribute
  Field implementation of integer valued descriptor."""

  @classmethod
  def getClassDefaultValue(cls) -> float:
    """Getter-function for default value."""
    return .0

  def getType(self) -> type:
    """Getter-function for value type."""
    return float

  def __init__(self, value: float = None, *args, **kwargs) -> None:
    AbstractAttribute.__init__(self, value, *args, **kwargs)
