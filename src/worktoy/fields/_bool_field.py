"""WorkToy - Fields - BoolField
Boolean valued mutable field """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.fields import AbstractField


class BoolField(AbstractField):
  """WorkToy - Fields - BoolField
  Boolean valued mutable field """

  def __init__(self, defVal: Any, *args, **kwargs) -> None:
    defVal = True if defVal else False
    AbstractField.__init__(self, defVal, *args, **kwargs)

  def getFieldSource(self) -> type:
    """Integer"""
    return bool

  def explicitGetter(self, obj: object, cls: type) -> bool:
    return True if AbstractField.explicitGetter(self, obj, cls) else False

  def explicitSetter(self, obj: object, val: Any) -> None:
    return AbstractField.explicitSetter(self, obj, True if val else False)

  def getPermissionLevel(self) -> int:
    """Protected, 2"""
    return 2


class BoolLabel(BoolField):
  """WorkToy - Fields - BoolField
  Boolean valued immutable field """

  def __init__(self, *args, **kwargs) -> None:
    BoolField.__init__(self, *args, **kwargs)

  def getPermissionLevel(self) -> int:
    """ReadOnly, 1"""
    return 1
