"""
The 'maybe' function returns the first of its arguments that is not 'None'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def maybe(*args) -> Any:
  """Return the first non-'None' argument.

  Parameters
  ----------
  *args
      Candidate values, tried left to right.

  Returns
  -------
  The first argument that is not 'None', or 'None' if every
  argument is 'None' (or no arguments were given).

  Examples
  --------
  >>> maybe(None, None, 'fallback')
  'fallback'
  >>> maybe(0, 'ignored')
  0
  >>> maybe(None, None) is None
  True
  """
  for arg in args:
    if arg is not None:
      return arg
  return None
