"""WorkToy - Core - FloatDescriptor
Floating point valued descriptor field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import string

from worktoy.fields import AbstractDescriptor


class FloatDescriptor(AbstractDescriptor):
  """WorkToy - Core - FloatDescriptor
  Floating point valued descriptor field."""

  __key__ = 'FLOAT'

  def __init__(self, defaultValue: float, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self.setSourceClass(float)
    self.setDefaultValue(self.maybe(defaultValue, 0.))

  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Explicit setter function."""
    if isinstance(newValue, int):
      return self.explicitSetter(obj, float(newValue))
    if isinstance(newValue, complex) and newValue.imag ** 2 < 1e-12:
      return self.explicitSetter(obj, newValue.real)
    if isinstance(newValue, str):
      dig = 0
      if len(newValue) - len(newValue.replace('.', '')) == 1:
        dig = len(newValue.split('.')[-1])
      newValue = ''.join([c for c in newValue if c in string.digits])
      val = 0
      digMap = {'%d' % i: i for i in range(10)}
      for (i, d) in enumerate([c for c in newValue]):
        val += (digMap[d] * 10 ** (i - dig))
      return self.explicitSetter(obj, val)
    AbstractDescriptor.explicitSetter(self, obj, newValue)


FLOAT = FloatDescriptor
