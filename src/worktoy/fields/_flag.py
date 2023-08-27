"""WorkToy - Core - Flag
Provides a boolean valued descriptor class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import AbstractDescriptor


class FLAG(AbstractDescriptor):
  """Specifically for boolean flags."""

  __key__ = 'FLAG'

  def __init__(self, flag, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self.setSourceClass(bool)
    self.setDefaultValue(True if self.maybe(flag, False) else False)

  def explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit getter function. Subclasses can reimplement this and other
    accessor functions customising behaviour."""
    getter = getattr(cls, self.getGetterFunctionName(), None)
    if getter is None:
      raise TypeError
    return True if getter(obj) else False

  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Explicit setter function."""
    setter = getattr(self.getOwner(), self.getSetterFunctionName(), None)
    if setter is None:
      raise TypeError
    setter(obj, True if newValue else False)
