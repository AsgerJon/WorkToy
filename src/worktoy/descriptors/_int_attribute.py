"""WorkToy - Descriptors - IntAttribute
Field implementation of integer valued descriptor."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.descriptors import AbstractAttribute


class IntAttribute(AbstractAttribute):
  """WorkToy - Fields - IntAttribute
  Field implementation of integer valued descriptor."""

  @classmethod
  def getClassDefaultValue(cls) -> int:
    """Getter-function for default value."""
    return 0

  def getType(self) -> type:
    """Getter-function for value type."""
    return int

  def __init__(self, value: int = None, *args, **kwargs) -> None:
    AbstractAttribute.__init__(self, value, *args, **kwargs)
