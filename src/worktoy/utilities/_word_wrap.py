"""
The 'wordWrap' function reflows text to a fixed character width.
"""
#  Apache-2.0 license
#  Copyright (c) 2024-2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, List


def _typeException(name: str, value: Any, *types: type) -> Exception:
  """Build a 'TypeException'.

  The import is deferred so 'utilities' does not pull in
  'waitaminute' at module load time.
  """
  from ..waitaminute import TypeException
  return TypeException(name, value, *types)


def wordWrap(width: int, *textLines: str, **kwargs) -> str:
  """Wrap input strings to a maximum line width.

  Every fragment in 'textLines' is tokenized on whitespace and
  reflowed. A line is closed (and a new one started) when

  - the next word equals the line-break token (the token itself
    is discarded), or
  - appending the next word would push the current line past
    'width'.

  Words longer than 'width' are placed on their own line; no
  attempt is made to break them.

  Parameters
  ----------
  width : int
      Maximum number of characters per output line.
  *textLines : str
      Text fragments to wrap. Each must be a 'str'.
  **kwargs
      newLine : str, optional
          Token forcing a line break, matched
          case-insensitively. Defaults to '<br>'.

  Returns
  -------
  str
      The wrapped text, joined by 'os.linesep'.

  Raises
  ------
  TypeException
      If 'width' is not an 'int' or any fragment is not a
      'str'.

  Examples
  --------
  >>> wordWrap(12, 'lorem ipsum dolor sit amet')
  'lorem ipsum\\ndolor sit\\namet'
  >>> wordWrap(20, 'first half <br> second half')
  'first half\\nsecond half'
  """
  if not isinstance(width, int):
    raise _typeException('width', width, int)
  newLine = kwargs.get('newLine', '<br>').strip().lower()
  words: List[str] = []
  for fragment in textLines:
    if not isinstance(fragment, str):
      raise _typeException('line', fragment, str)
    words.extend(fragment.split())
  lines: List[str] = []
  current: List[str] = []
  for word in words:
    if word.lower() == newLine:
      lines.append(' '.join(current))
      current = []
      continue
    if current and len(' '.join([*current, word])) > width:
      lines.append(' '.join(current))
      current = [word]
      continue
    current.append(word)
  lines.append(' '.join(current))
  return os.linesep.join(lines)
