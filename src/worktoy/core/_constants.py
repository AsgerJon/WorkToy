"""WorkToy - Core - Constants
This module provides mathematical constants."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os

PI = 3.14159265358979323


def factorial(n: int) -> int:
  """Factorial function."""
  if n in [0, 1]:
    return 1
  return n * factorial(n - 1) if n > 1 else 1


def quad(order: int) -> int:
  """0, 1,  0, -1, 0, ..."""
  return (((order + 2) % 4) // 2) - (((2 - order) % 4) // 2)


def sineTerm(x: float, a: float, order: int) -> float:
  """Term in sine function."""
  return ((x - a) ** order / factorial(order)) * quad(order)


def cosineTerm(x: float, a: float, order: int) -> float:
  """Term in sine function."""
  return ((x - a) ** order / factorial(order)) * quad(order + 1)


def principalSine(val: float, ) -> float:
  """Sine"""
  if val < 0:
    return -principalSine(-val, )
  a = 0 if (PI / 4 - abs(val)) ** 2 < PI / 8 else PI / 4
  a = a if val > 0 else -a
  out = 0
  c = 0
  term = sineTerm(val, a, 0)
  while (quad(c + 1) ** 2) + term ** 2 > 1e-16:
    out += term
    c += 1
    term = sineTerm(val, a, c)
  return out


def principalCosine(val: float, ) -> float:
  """Cosine"""
  return (1 - principalSine(val) ** 2) ** 0.5


here = os.path.dirname(__file__)
fileName = 'lorem.txt'
filePath = os.path.join(here, fileName)
with open(filePath) as f:
  loremSample = f.read()
