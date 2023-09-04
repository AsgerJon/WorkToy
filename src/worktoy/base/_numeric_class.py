"""WorkToy - Core - NumericClass
Provides numeric functions."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from math import cos
from typing import Any

from icecream import ic

from worktoy.core import PI
from worktoy.base import CoreClass

ic.configureOutput(includeContext=True)


class NumericClass(CoreClass):
  """WorkToy - Core - NumericClass
  Provides numeric functions."""

  def __init__(self, *args, **kwargs) -> None:
    CoreClass.__init__(self, *args, **kwargs)

  def valueSpace(self, *args) -> Any:
    """Collects from positional arguments the start, stop and number of
    points used in intervals."""
    a, b, n = None, None, None
    if len(args) == 2:
      a, b, n = 0, args[0], args[1]
    elif len(args) == 3:
      a, b, n = args[0], args[1], args[2]
    if not (isinstance(a, float), isinstance(b, float), isinstance(n, int)):
      raise TypeError
    if n < 2:
      raise ValueError
    return dict(first=a, last=b, steps=n)

  def linSpace(self, *args) -> list[float]:
    """Linear-space for linear list of floating point."""
    valSpace = self.valueSpace(*args)
    a, b, n = [valSpace[key] for key in ['first', 'last', 'steps']]
    dx = (b - a) / (n - 1)
    return [a + dx * i for i in range(n)]

  def getChebyshev(self, *args) -> list[float]:
    """Getter-function for list of Chebyshev points."""
    valSpace = self.valueSpace(*args)
    a, b, n = [valSpace[key] for key in ['first', 'last', 'steps']]
    angleSpace = self.linSpace(0, PI, n)
    base = [cos(angle) for angle in angleSpace]
    radius = max([a - b, b - a]) / 2
    center = min([a, b]) + radius
    return [center - radius * step for step in base]
