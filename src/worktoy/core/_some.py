"""The 'some' function takes an arbitrary number of positional arguments
and returns True if at least one such argument is different from None."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


def some(*args) -> bool:
  """The 'some' function takes an arbitrary number of positional arguments
  and returns True if at least one such argument is different from None."""
  for arg in args:
    if arg is not None:
      return True
  return False
