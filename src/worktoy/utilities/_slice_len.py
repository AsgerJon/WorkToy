"""Compute the length of a slice applied to a sequence.

The ``sliceLen`` function takes a ``slice`` object and the length of
a sequence, and returns the number of elements that would result
from applying the slice to such a sequence."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


def sliceLen(sliceObj: slice, length: int) -> int:
  """Return the number of elements produced by a slice.

  Parameters
  ----------
  sliceObj : slice
      The slice to evaluate.
  length : int
      The length of the sequence the slice would apply to.

  Returns
  -------
  int
      The number of elements that would be selected.

  Raises
  ------
  ValueError
      If ``sliceObj.step`` is zero.

  Examples
  --------
  >>> sliceLen(slice(0, 10, 2), 10)
  5
  >>> sliceLen(slice(None, None, -1), 4)
  4
  >>> sliceLen(slice(5, 100), 10)
  5
  """
  return len(range(*sliceObj.indices(length), ))
