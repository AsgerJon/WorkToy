"""The 'maybe' function receives any number of positional arguments and
returns the first argument that is not None. If all arguments are None,
the function returns None."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


def maybe(*args: object) -> object:
  """The 'maybe' function receives any number of positional arguments and
  returns the first argument that is not None. If all arguments are None,
  the function returns None."""
  for arg in args:
    if arg is not None:
      return arg
  return None
