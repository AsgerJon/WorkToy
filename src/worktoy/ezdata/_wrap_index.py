"""Internal helper: wrap a possibly-negative index to ``[0, n)``
or raise ``IndexError`` if it cannot be wrapped."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations


def wrapIndex(key: int, n: int) -> int:
  """Wrap ``key`` to ``[0, n)`` or raise ``IndexError``.

  Negative indices wrap modulo ``n``; non-negative indices must
  already be in range. ``n == 0`` is rejected.
  """
  if n == 0:
    raise IndexError('index out of range; class has no fields')
  if key < 0:
    key = key % n
  if 0 <= key < n:
    return key
  raise IndexError(
      'index %d out of range for sequence of length %d' % (key, n))
