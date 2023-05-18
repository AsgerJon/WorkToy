"""Documentation: textBetween
Returns a list of text between start and end tags, including nested
  tag pairs.
"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import searchTerm


class Tag:
  """Tag represents a pair of start and end tags and content"""

  def __init__(self, startTag: str, endTag: str) -> None:
    self._startTag, self._endTag = startTag, endTag
    self._startInd, self._endInd = None, None
    self._level = None
    self._content = None


def textBetween(source: str, startTag: str, endTag: str) -> list:
  """Find all content between two given tags in a source text.

  Args:
  - source_text: The source text to search.
  - start_tag: The starting tag.
  - end_tag: The ending tag.

  Returns:
  A list of contents found between the start and end tags.
  """

  if not startTag or not endTag:
    raise ValueError("The startTag and endTag cannot be empty strings!")

  startInds = [[*inds, '<'] for inds in searchTerm(source, startTag)]
  endInds = [[*inds, '>'] for inds in searchTerm(source, endTag)]

  if len(startInds) - len(endInds):
    print(startInds)
    print(endInds)
    raise ValueError('Mismatch between number of start tags and end tags!')
  newTags = []
  for (openTag, closeTag) in zip(startInds, endInds):
    newTags.append(source[openTag[1]: closeTag[0]])
  return newTags
