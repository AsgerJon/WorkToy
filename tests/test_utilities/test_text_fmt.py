"""
TestTextFmt tests 'textFmt' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os

from worktoy.utilities import textFmt
from . import UtilitiesTest


class TestTextFmt(UtilitiesTest):
  """
  'textFmt' lets a message be written as an indented triple-quoted
  literal and still come out as one line, with '<br>' and '<tab>' the
  only way to ask for a line break or an indent. The tests pin the
  collapse of whitespace, the two tokens, the spaces dropped next to a
  break, the custom tokens and symbols, and what becomes of arguments
  that are empty or no strings.
  """

  def test_no_arguments(self) -> None:
    self.assertEqual(textFmt(), '')

  def test_empty_strings_only(self) -> None:
    self.assertEqual(textFmt(''), '')
    self.assertEqual(textFmt('', ''), '')

  def test_whitespace_collapsed(self) -> None:
    self.assertEqual(textFmt('many    spaces   here'), 'many spaces here')
    literal = """first line
        second line
      third"""
    self.assertEqual(textFmt(literal), 'first line second line third')

  def test_arguments_joined_by_space(self) -> None:
    self.assertEqual(textFmt('a', 'b', 'c'), 'a b c')

  def test_tokens(self) -> None:
    expected = 'paragraph%s  indented line' % os.linesep
    self.assertEqual(textFmt('paragraph<br><tab>indented line'), expected)

  def test_spaces_around_break_dropped(self) -> None:
    expected = 'a%sb' % os.linesep
    self.assertEqual(textFmt('a <br> b'), expected)
    self.assertEqual(textFmt('a', '<br>', 'b'), expected)

  def test_non_string_arguments_rendered(self) -> None:
    self.assertEqual(textFmt(1, 'x', None), '1 x None')
    self.assertEqual(textFmt(0), '0')

  def test_empty_strings_among_others_skipped(self) -> None:
    self.assertEqual(textFmt('', 'a', '', 'b'), 'a b')

  def test_custom_tokens_and_symbols(self) -> None:
    text = textFmt(
        'one | two > three',
        newLineToken='|',
        tabToken='>',
        newLineSymbol='\n\n',
        indentSymbol='\t',
    )
    self.assertEqual(text, 'one\n\ntwo \t three')

  def test_default_tokens_literal_under_custom(self) -> None:
    self.assertEqual(textFmt('a<br>b', newLineToken='|'), 'a<br>b')
