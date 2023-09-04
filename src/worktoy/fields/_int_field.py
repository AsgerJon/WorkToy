"""WorkToy - Fields - IntField
Integer valued mutable field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.fields import AbstractField

from icecream import ic

ic.configureOutput(includeContext=True)


class IntField(AbstractField):
  """WorkToy - Fields - IntField
  Integer valued mutable field."""

  def __init__(self, defVal: Any, *args, **kwargs) -> None:
    if not isinstance(defVal, int):
      try:
        defVal = int(defVal)
      except Exception:
        from worktoy.waitaminute import TypeSupportError
        raise TypeSupportError(int, defVal, 'defVal') from Exception
    AbstractField.__init__(self, defVal, *args, **kwargs)

  def getFieldSource(self) -> type:
    """Integer"""
    return int

  def getPermissionLevel(self) -> int:
    """Protected. """
    return 2

  def explicitSetter(self, obj: object, newValue: int) -> None:
    """Explicit setter function. Tries to find the _set[NAME] method on
    the object."""
    return setattr(obj, self.getPrivateName(), newValue)

  def explicitGetter(self, obj: object, cls: type) -> int:
    return AbstractField.explicitGetter(self, obj, cls)


class IntLabel(IntField):
  """Integer-valued immutable field."""

  def __init__(self, defVal: Any, *args, **kwargs) -> None:
    IntField.__init__(self, defVal, *args, **kwargs)

  def getPermissionLevel(self) -> int:
    """ReadOnly, 1"""
    return 1
