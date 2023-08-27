"""WorkToy - Core - ClassDescriptor
Descriptor class for other classes and types."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import AbstractDescriptor


class ClassDescriptor(AbstractDescriptor):
  """WorkToy - Core - ClassDescriptor
  Descriptor class for other classes and types."""

  __key__ = 'CLASS'

  def __init__(self, cls: type, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self.setSourceClass(cls)


CLASS = AbstractDescriptor
