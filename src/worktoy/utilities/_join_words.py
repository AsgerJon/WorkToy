"""Join words into a human-readable list string.

The ``joinWords`` function combines a sequence of strings into a
single phrase using commas and a final separator. By default the
final two items are joined with ``and``; pass ``sep='or'`` (or any
other connector) to change the trailing separator."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


def joinWords(*words: str, **kwargs) -> str:
  """Join words with commas and a trailing separator.

  Parameters
  ----------
  *words : str
      The words to join. Passing a single ``list`` or ``tuple``
      is treated as if its elements had been passed as varargs.
  **kwargs
      sep : str, optional
          Connector before the final word. Defaults to
          ``'and'``; pass ``'or'`` for disjunctive lists.

  Returns
  -------
  str
      The joined phrase, or ``''`` for an empty input.

  Examples
  --------
  >>> joinWords('apples', 'pears')
  'apples and pears'
  >>> joinWords('red', 'green', 'blue')
  'red, green and blue'
  >>> joinWords('tea', 'coffee', sep='or')
  'tea or coffee'
  """
  if not words:
    return ''
  sep = kwargs.get('sep', 'and')
  if len(words) == 1:
    if isinstance(words[0], (list, tuple)):
      return joinWords(*words[0])
    return str(words[0])
  if len(words) == 2:
    return '%s %s %s' % (words[0], sep, words[1])
  return joinWords(', '.join(words[:-1]), words[-1])
