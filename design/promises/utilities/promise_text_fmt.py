"""
PromiseTextFmt promises 'textFmt' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

from worktoy.utilities import textFmt


class PromiseTextFmt(TestCase):
  """
  'textFmt' turns a triple-quoted literal into one line of text: its
  arguments are joined by spaces, every run of whitespace becomes one
  space, '<br>' becomes a line break, without the spaces around it, and
  '<tab>' becomes an indent of two spaces. A line break is 'os.linesep'
  unless 'newLineSymbol' says otherwise; the tokens and the indent can
  be changed with 'newLineToken', 'tabToken' and 'indentSymbol'. Source:
  the 'textFmt' docstring and its examples.
  """

  def test_collapses_whitespace(self) -> None:
    self.assertEqual(textFmt('many    spaces   here'), 'many spaces here')
    text = """Two lines
    of a literal."""
    self.assertEqual(textFmt(text), 'Two lines of a literal.')

  def test_line_break_and_indent(self) -> None:
    expected = 'paragraph%s  indented line' % os.linesep
    self.assertEqual(textFmt('paragraph<br><tab>indented line'), expected)
    expected = 'first%ssecond' % os.linesep
    self.assertEqual(textFmt('first <br> second'), expected)

  def test_joins_arguments(self) -> None:
    self.assertEqual(textFmt('Received', 3, 'items'), 'Received 3 items')

  def test_empty(self) -> None:
    self.assertEqual(textFmt(), '')
    self.assertEqual(textFmt(''), '')

  def test_custom_tokens(self) -> None:
    text = textFmt('a|b', newLineToken='|', newLineSymbol='\n')
    self.assertEqual(text, 'a\nb')
    text = textFmt('a<br>>b', tabToken='>', indentSymbol='\t',
                   newLineSymbol='\n')
    self.assertEqual(text, 'a\n\tb')
