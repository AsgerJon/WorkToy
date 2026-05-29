"""
The 'joinWords' function joins words into a human-readable list phrase.
"""
#  Apache-2.0 license
#  Copyright (c) 2024-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import unpack

if TYPE_CHECKING:  # pragma: no cover
  pass


def joinWords(*words, **kwargs) -> str:
  """Join words with commas and a trailing separator.

  Iterable arguments (other than 'str' and 'bytes') are flattened
  recursively via 'unpack' before joining, so any mix of plain
  words, lists, and tuples is accepted in source order.

  Parameters
  ----------
  *words
      The words to join. Any 'list' or 'tuple' among the arguments
      is flattened into the surrounding sequence; nesting is
      collapsed all the way down. 'str' and 'bytes' are treated as
      atomic.
  **kwargs
      sep : str, optional
          Connector before the final word. Defaults to 'and'; pass
          'or' for disjunctive lists.

  Returns
  -------
  str
      The joined phrase, or '' for an empty input.

  Examples
  --------
  >>> joinWords('apples', 'pears')
  'apples and pears'
  >>> joinWords('red', 'green', 'blue')
  'red, green and blue'
  >>> joinWords('tea', 'coffee', sep='or')
  'tea or coffee'
  >>> joinWords('Tom', ['Dick', 'Harry'])
  'Tom, Dick and Harry'
  """
  sep = kwargs.get('sep', 'and')
  words = unpack(*words, strict=False)
  if not words:
    return ''
  if len(words) == 1:
    return str(words[0])
  if len(words) == 2:
    return '%s %s %s' % (words[0], sep, words[1])
  head = ', '.join(str(w) for w in words[:-1])
  return '%s %s %s' % (head, sep, words[-1])
