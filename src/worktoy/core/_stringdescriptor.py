"""WorkToy - Core - StringDescriptor
Descriptor class for strings"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import AbstractDescriptor


class StringDescriptor(AbstractDescriptor):
  """WorkToy - Core - ClassDescriptor
  Descriptor class for other classes and types."""

  def __init__(self, defaultValue: str = None, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self._defaultValue = self.maybe(defaultValue, '__')
    self._valueType = str


STR = StringDescriptor
