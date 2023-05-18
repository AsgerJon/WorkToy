"""The findAll function returns the indicis of a term in a text. """
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


def searchTerm(text: str, term: str) -> list[list[int, int]]:
  """Searches a text for all instances of a term and returns their
  indices."""
  if not term:
    raise ValueError('The term cannot be the empty string!')
  out = []
  if not text:
    return out
  n = len(term)
  c = 0
  text += '          '
  while c + n < len(text):
    testTag = text[c:c + n]
    if testTag == term:
      out.append([c, c + n])
      c += n
    else:
      c += 1
  return sorted(out)
