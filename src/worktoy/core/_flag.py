"""WorkToy - Core - Flag
Provides a boolean valued descriptor class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import AbstractDescriptor


class FLAG(AbstractDescriptor):
  """Specifically for boolean flags."""

  def __init__(self, flag, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self._defVal = True if self.maybe(flag, False) else False
    self._valueType = bool

  def explicitGetter(self, obj: object, cls: type) -> object:
    """Explicit getter function. Subclasses can reimplement this and other
    accessor functions customising behaviour."""
    val = getattr(obj, self.getPrivateVariableName(), None)
    return True if val else False

  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Explicit setter function."""
    val = True if newValue else False
    setattr(obj, self.getPrivateVariableName(), val)
