"""Replace a single specific occurrence of a substring.

Unlike ``str.replace``, which always rewrites the first ``count``
occurrences from the left, ``replaceFlex`` rewrites *only* the
``n``-th occurrence and leaves the rest in place."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import maybe

if TYPE_CHECKING:  # pragma: no cover
  pass


def replaceFlex(text: str, old: str, new: str, n: int = None) -> str:
  """Replace the ``n``-th occurrence of ``old`` with ``new``.

  Parameters
  ----------
  text : str
      Source string.
  old : str
      Substring to locate.
  new : str
      Replacement substring.
  n : int, optional
      1-based index of the occurrence to replace. Defaults to ``1``
      (first occurrence). Searches advance past the prior match by
      one character, so overlapping matches are scanned.

  Returns
  -------
  str
      The text with one occurrence rewritten, or the unchanged
      input if fewer than ``n`` occurrences exist.

  Examples
  --------
  >>> replaceFlex('foo bar foo baz foo', 'foo', 'X', 2)
  'foo bar X baz foo'
  >>> replaceFlex('abc', 'x', 'y')
  'abc'
  """
  n = maybe(n, 1)
  i = -1
  for _ in range(n):
    i = text.find(old, i + 1)
    if i == -1:
      return text
  return text[:i] + new + text[i + len(old):]
