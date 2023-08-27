"""WorkToy - Core - StringDescriptor
Descriptor class for strings"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.fields import AbstractDescriptor

ic.configureOutput(includeContext=True)


class StringDescriptor(AbstractDescriptor):
  """WorkToy - Core - ClassDescriptor
  Descriptor class for other classes and types."""

  __key__ = 'STR'

  def __init__(self, defaultValue: str = None, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    defaultValue = self.maybe(defaultValue, '__')
    self.setDefaultValue(defaultValue)
    self.setSourceClass(str)


STR = StringDescriptor
