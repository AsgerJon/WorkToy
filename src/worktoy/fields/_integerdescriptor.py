"""WorkToy - Core - IntDescriptor
Implements integer valued descriptor"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import AbstractDescriptor
from worktoy.core import Function


class IntegerDescriptor(AbstractDescriptor):
  """WorkToy - Core - IntDescriptor
  Implements integer valued descriptor"""

  def __init__(self, defaultValue: int, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self.setSourceClass(int)
    self.setDefaultValue(0)

  def sourceInstanceFactory(self) -> Function:
    """Factory for source instance creators."""

    def sourceInstanceCreator(cls: type, obj: object) -> object:
      """Source instance creator"""
      return 0

    return sourceInstanceCreator


INT = IntegerDescriptor
