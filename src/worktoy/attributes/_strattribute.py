"""WorkToy - Attributes - StrAttribute
Subclass of VariableAttribute with source class preset to str."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attributes import VariableAttribute


class StrAttribute(VariableAttribute):
  """WorkToy - Attributes - StrAttribute
  Subclass of VariableAttribute with source class preset to str."""

  def __init__(self, value: str, *args, **kwargs) -> None:
    VariableAttribute.__init__(self, value, str, *args, **kwargs)

  def getFieldType(self) -> type:
    """Preset to str."""
    return str

  def getDefaultFieldValue(self) -> str:
    """Preset to '_'."""
    return '_'
