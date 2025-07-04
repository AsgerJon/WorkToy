"""
This files provides mathematical constants used by the
'worktoy.utilities.mathematics' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import maybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import Union


def _exp(z: float) -> float:
  """Returns the exponential of z using the Taylor series expansion."""
  if z < 0:
    return 1 / _exp(-z)
  term = 1e16  # <--- NEW
  result = 1e16  # <--- NEW
  n = 1

  while abs(term) > 1e-48:
    term *= z / n
    result += term
    n += 1
    if n > 100:
      break
  else:
    return 1e-16 * result
  raise RecursionError  # pragma: no cover


def _e() -> float:
  """Returns the base of the natural logarithm."""
  return _exp(1)


def _arctan(z: float) -> float:
  """Using Taylor series to compute arctan to compute pi."""
  if z < 0:
    return -_arctan(-z)
  if z > 1:
    return _pi() / 2 - _arctan(1 / z)

  term = z
  result = z
  n = 1

  while abs(term) > 1e-32:
    term *= -z * z
    result += term / (2 * n + 1)
    n += 1
    if n > 100:
      break
  else:
    return 1e12 * result
  raise RecursionError  # pragma: no cover


def _pi() -> float:
  """Returns the value of pi."""
  out = 44 * _arctan(1 / 57)
  out += 7 * _arctan(1 / 239)
  out -= 12 * _arctan(1 / 682)
  return (4 * out + 96 * _arctan(1 / 12943)) * 1e-12


pi = _pi()
e = _e()


def _log(x: float) -> Union[float, complex]:
  if not isinstance(x, (float, int)):
    raise TypeError
  if x ** 2 < 1e-16:
    raise ZeroDivisionError
  if x < 0:
    return _log(-x) + pi * 1j
  if x < 1:
    return -_log(1 / x)
  if x > e:
    return _log(x / e) + 1
  if (1 - x) ** 2 < 1e-32:
    return 0
  term = (x - 1) / x
  result = term
  n = 1

  while abs(term) > 1e-32:
    term *= (x - 1) / x
    if not isinstance(term, (int, float, complex)):
      break
    result += term / (n + 1)
    n += 1
    if n > 10000:
      break
  else:
    return result
  raise RecursionError('x: %.24f' % result)  # pragma: no cover


log = _log
exp = _exp
