"""WorkToy - Fields - Flag
Boolean valued field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never

from worktoy.fields import AbstractDescriptor


class Flag(AbstractDescriptor):
  """WorkToy - Fields - Flag
  Boolean valued field."""

  def __init__(self, defVal: Any, *args, **kwargs) -> None:
    defVal = True if defVal else False
    AbstractDescriptor.__init__(self, *args, **kwargs)

  def explicitGetter(self, obj: object, cls: type) -> bool:
    val = AbstractDescriptor.explicitGetter(self, obj, cls)
    return True if val else False

  def explicitSetter(self, obj: object, newValue: Any) -> None:
    val = True if newValue else False
    return AbstractDescriptor.explicitSetter(self, obj, val)

  def explicitDeleter(self, *_, ) -> Never:
    return AbstractDescriptor.explicitDeleter(self, *_)

  def getPermissionLevel(self) -> int:
    """Protected, 2"""
    return 2
