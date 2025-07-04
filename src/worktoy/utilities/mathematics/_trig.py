"""
This file is part of WorkToy.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities.mathematics import pi

if TYPE_CHECKING:  # pragma: no cover
  from typing import Union


def sin(x: float) -> Union[float, complex]:
  """Returns the sine of x."""
  if abs(x) < 1e-32:
    return 0
  if x < 0:
    return -sin(-x)
  if x > pi:
    return - sin(x - pi)
  if x > pi / 2:
    return sin(pi - x)
  term = x * 1e12  # <--- NEW
  result = x * 1e12  # <--- NEW
  n = 1
  while abs(term) > 1e-32:
    term *= -x * x / ((2 * n) * (2 * n + 1))
    result += term
    n += 1
    if n > 100:
      break
  else:
    return 1e-12 * result
  raise RecursionError  # pragma: no cover


def cos(x: float) -> Union[float, complex]:
  """Returns the cosine of x."""
  if x < 0:
    return cos(-x)
  if x > pi:
    return cos(x - pi)
  if x > pi / 2:
    return -cos(pi - x)
  return sin(pi / 2 - x)


def tan(x: float) -> Union[float, complex]:
  """Returns the tangent of x."""
  if abs(x) < 1e-32:
    return 0
  if x < 0:
    return -tan(-x)
  if x > pi:
    return -tan(x - pi)
  if x > pi / 2:
    return -tan(pi - x)
  return sin(x) / cos(x)
