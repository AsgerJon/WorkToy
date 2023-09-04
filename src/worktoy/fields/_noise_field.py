"""WorkToy - Fields - NoiseField
A floating field with slightly random values returned."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from random import random

from worktoy.fields import FloatField


class NoiseField(FloatField):
  """WorkToy - Fields - NoiseField
  A floating field with slightly random values returned."""

  def __init__(self, defVal: float, noise: float = None,
               *args, **kwargs) -> None:
    FloatField.__init__(self, defVal, *args, **kwargs)
    self._noise = self.maybe(noise, 0.1)

  def applyNoise(self, base: float) -> float:
    """Applies noise."""
    noise = self._noise * random()
    return (1 - self._noise) * base + 2 * noise * base

  def explicitGetter(self, obj: object, cls: type) -> float:
    """Explicit getter function"""
    out = FloatField.explicitGetter(self, obj, cls)
    return self.applyNoise(out)
