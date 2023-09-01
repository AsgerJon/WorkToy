"""WorkToy - Fields - ReadOnlyField
Subclass of AbstractField setting permission level to 1, disables the
source setter method and requires the source type be set at instance
creation time."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from worktoy.fields import AbstractField


class ReadOnlyField(AbstractField):
  """WorkToy - Fields - ReadOnlyField
  Subclass of AbstractField setting permission level to 1, disables the
  source setter method and requires the source type be set at instance
  creation time."""

  def __init__(self, fieldType: type, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)
    self._explicitSourceType = fieldType

  def getFieldSource(self) -> type:
    """Getter-function for field source."""
    return self._explicitSourceType

  def setFieldSource(self, *_) -> Never:
    """Disabled setter function"""
    from worktoy.waitaminute import DisabledFunctionError
    raise DisabledFunctionError(AbstractField, ReadOnlyField, )

  def getPermissionLevel(self) -> int:
    """Read Only."""
    return 1
