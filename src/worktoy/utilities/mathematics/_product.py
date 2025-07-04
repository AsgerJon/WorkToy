"""
The 'product' function computes the product of all elements in an iterable.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union

  Number: TypeAlias = Union[int, float, complex]


def product(*args) -> Number:
  """
  Computes the product of all elements in an iterable.

  Args:
    *args: An iterable of numbers.

  Returns:
    The product of all elements in the iterable.
  """
  if not args:
    return 1.0
  if len(args) == 1 and isinstance(args[0], (list, tuple)):
    return product(*args[0])
  out = 1.0
  for arg in args:
    out *= arg
  return out
