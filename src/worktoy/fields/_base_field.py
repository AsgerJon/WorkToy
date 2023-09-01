"""WorkToy - Fields - BaseField
Field supporting types that require setting and deleting."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from worktoy.fields import AbstractField


class BaseField(AbstractField):
  """WorkToy - Fields - BaseField
  Field supporting types that require setting and deleting."""

  def __init__(self, fieldType: type, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)
    self._explicitSourceType = fieldType

  def getFieldSource(self) -> type:
    """Getter-function for field source."""
    return self._explicitSourceType

  def setFieldSource(self, *_) -> Never:
    """Disabled setter function"""
    from worktoy.waitaminute import DisabledFunctionError
    raise DisabledFunctionError(AbstractField, BaseField, )

  def getPermissionLevel(self) -> int:
    """Full Permissions"""
    return 3
