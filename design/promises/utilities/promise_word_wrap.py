"""
PromiseWordWrap promises 'wordWrap' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

from worktoy.utilities import wordWrap


class PromiseWordWrap(TestCase):
  """
  'wordWrap' reflows text into lines of at most 'width' characters, joined by
  'os.linesep'; the line breaks already in the text are whitespace like any
  other. A '<br>' among the words, in any case, or the token given as
  'newLine', breaks the line and is dropped. A word longer than the width
  stands on a line of its own, unbroken. Source: the 'wordWrap' docstring and
  its examples.
  """

  def test_wraps(self) -> None:
    lines = wordWrap(12, 'lorem ipsum dolor sit amet').split(os.linesep)
    self.assertEqual(lines, ['lorem ipsum', 'dolor sit', 'amet'])

  def test_line_break(self) -> None:
    lines = wordWrap(20, 'first half <br> second half').split(os.linesep)
    self.assertEqual(lines, ['first half', 'second half'])
    lines = wordWrap(20, 'first <BR> second').split(os.linesep)
    self.assertEqual(lines, ['first', 'second'])
    lines = wordWrap(20, 'first // second', newLine='//')
    self.assertEqual(lines.split(os.linesep), ['first', 'second'])

  def test_existing_line_breaks_reflowed(self) -> None:
    self.assertEqual(wordWrap(20, 'first\nsecond'), 'first second')

  def test_long_word(self) -> None:
    lines = wordWrap(4, 'a extraordinary b').split(os.linesep)
    self.assertEqual(lines, ['a', 'extraordinary', 'b'])
