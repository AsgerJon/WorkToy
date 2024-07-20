"""The 'worktoy.workWrap' function receives an integer defining character
width and any number of strings. The function then returns a list of
strings containing the words from the strings received such that each
entry in the list does not exceed the character width. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


def wordWrap(width: int, *textLines) -> list[str]:
  """The wordwrap function wraps the input text to a specified width."""
  words = []
  for line in textLines:
    words.extend(line.split())
  lines = []
  line = []
  while words:
    word = words.pop(0)
    if len(' '.join([*line, word])) <= width:
      line.append(word)
    else:
      lines.append(' '.join(line))
      line = [word]
  if line:
    lines.append(' '.join(line))
  return lines
