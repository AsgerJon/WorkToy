"""WorkToy - Descriptors - StrAttribute
String valued attribute descriptor implementation."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.descriptors import AbstractAttribute


class StrAttribute(AbstractAttribute):
  """WorkToy - Fields - IntAttribute
  Field implementation of integer valued descriptor."""

  @classmethod
  def getClassDefaultValue(cls) -> str:
    """Getter-function for default value."""
    return ''

  def getType(self) -> type:
    """Getter-function for value type."""
    return str

  def __init__(self, value: str = None, *args, **kwargs) -> None:
    AbstractAttribute.__init__(self, value, *args, **kwargs)
