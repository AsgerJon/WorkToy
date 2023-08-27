"""WorkToy - Core - IntDescriptor
Implements integer valued descriptor"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import AbstractDescriptor


class IntegerDescriptor(AbstractDescriptor):
  """WorkToy - Core - IntDescriptor
  Implements integer valued descriptor"""

  def __init__(self, defaultValue: int, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self._defVal = self.maybe(defaultValue, 0)
    self._valueType = int


class INT(IntegerDescriptor):
  """WorkToy - Core - IntDescriptor
  Implements integer valued descriptor"""

  def __init__(self, defaultValue: int, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self._defVal = self.maybe(defaultValue, 0)
    self._valueType = int
