"""Split strings into a cleaned list of substrings.

The ``stringList`` function splits each input string by one or
more separators (default ``', '``), strips whitespace from each
piece, and discards empty results. Multiple separators may be
applied in sequence by passing a list or tuple."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


def stringList(*args: str, **kwargs) -> list[str]:
  """Split strings into a stripped, non-empty list of pieces.

  Parameters
  ----------
  *args : str
      Strings to split.
  **kwargs
      separator : str or list of str or tuple of str, optional
          Separator(s) used to split. If a single string, that
          separator is applied directly. If a list or tuple, each
          element is applied in turn, with later separators
          splitting the results of earlier ones. Defaults to
          ``', '``.

  Returns
  -------
  list of str
      Stripped, non-empty pieces in original order.

  Raises
  ------
  TypeException
      If ``separator`` is not a ``str``, ``list``, or ``tuple``.

  Examples
  --------
  >>> stringList('a, b, c')
  ['a', 'b', 'c']
  >>> stringList('a;b,c', separator=[',', ';'])
  ['a', 'b', 'c']
  """
  sep = kwargs.get('separator', ', ')
  if isinstance(sep, str):
    out = []
    for arg in args:
      out.extend(arg.split(sep))
    return [a.strip() for a in out if a.strip()]
  if isinstance(sep, (list, tuple)):
    out = [*args, ]
    for s in sep:
      out = stringList(*out, separator=s)
    return [a.strip() for a in out if a.strip()]
  from ..waitaminute import TypeException
  raise TypeException('separator', sep, str, list, tuple)
