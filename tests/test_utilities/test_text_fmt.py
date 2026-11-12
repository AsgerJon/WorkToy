"""
TestTextFmt tests 'textFmt' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from worktoy.utilities import textFmt
from worktoy.waitaminute import RedundantKeyword
from . import UtilitiesTest

HERE = sys._getframe().f_code.co_filename


class TestTextFmt(UtilitiesTest):
  """
  'textFmt' lets a message be written as an indented triple-quoted
  literal and still come out as one line, with '<br>' and '<tab>' the
  only way to ask for a line break or an indent. The tests pin the
  collapse of whitespace, the two tokens, the spaces dropped next to a
  break, the custom tokens and symbols, what becomes of arguments that
  are empty or no strings, and the warning given for a keyword that is
  no option.
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

  def test_unknown_keyword_warned(self) -> None:
    expected = """'worktoy.utilities.textFmt' received the keyword
    'newLineTokn', which it does not read, and went on without it! It
    reads: 'newLineToken', 'tabToken', 'newLineSymbol', 'indentSymbol'."""
    options = ('newLineToken', 'tabToken', 'newLineSymbol', 'indentSymbol')
    with self.assertWarns(RedundantKeyword) as context:
      line = sys._getframe().f_lineno + 1
      text = textFmt('a<br>b', newLineTokn='|')
    self.assertEqual(text, 'a%sb' % os.linesep)
    warning = context.warning
    self.assertIs(warning.receiver, textFmt)
    self.assertEqual(warning.keyword, 'newLineTokn')
    self.assertEqual(warning.options, options)
    self.assertEqual(str(warning), str.join(' ', expected.split()))
    self.assertEqual(context.filename, HERE)
    self.assertEqual(context.lineno, line)
    with self.assertWarns(RedundantKeyword):
      text = textFmt(newLineTokn='|')
    self.assertEqual(text, '')
