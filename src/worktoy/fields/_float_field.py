"""WorkToy - Fields - FloatField
Float-valued field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.fields import AbstractField


class FloatField(AbstractField):
  """WorkToy - Fields - FloatField
  Float-valued field."""

  def __init__(self, defVal: float = None, *args, **kwargs) -> None:
    defVal = self.maybe(defVal, 0)
    AbstractField.__init__(self, defVal, *args, **kwargs)

  def getFieldSource(self) -> type:
    """Getter-function for the field source."""
    return float

  def getPermissionLevel(self) -> int:
    """Protected, 2"""
    return 2


class FloatLabel(FloatField):
  """WorkToy - Fields - FloatField
  Float-valued field."""

  def __init__(self, defVal: float = None, *args, **kwargs) -> None:
    defVal = self.maybe(defVal, 0)
    FloatField.__init__(self, defVal, *args, **kwargs)

  def getFieldSource(self) -> type:
    """Getter-function for the field source."""
    return float

  def getPermissionLevel(self) -> int:
    """Protected, 2"""
    return 1
