"""WorkToy - Core - FloatDescriptor
Floating point valued descriptor field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import AbstractDescriptor


class FloatDescriptor(AbstractDescriptor):
  """WorkToy - Core - FloatDescriptor
  Floating point valued descriptor field."""

  def __init__(self, defaultValue: float, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self._defVal = self.maybe(defaultValue, 0.)
    self._valueType = float


FLOAT = FloatDescriptor
