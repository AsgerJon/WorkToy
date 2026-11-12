"""
TestWordWrap tests 'wordWrap' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from worktoy.utilities import wordWrap
from worktoy.waitaminute import TypeException, RedundantKeyword
from worktoy.work_test.samplers import WordSampler
from . import UtilitiesTest

HERE = sys._getframe().f_code.co_filename


class TestWordWrap(UtilitiesTest):
  """
  'wordWrap' reflows text to a width, closing a line before a word
  that would push it past the width or at a break token, and leaves a
  word longer than the width on a line of its own. The tests pin the
  docstring examples, the exact fit, the long word, the token in any
  case and under another spelling, the refusals, the warning given for
  a keyword that is no option, and that every line of a random text
  fits unless it is a single long word.
  """

  def test_docstring_examples(self) -> None:
    expected = os.linesep.join(('lorem ipsum', 'dolor sit', 'amet'))
    self.assertEqual(wordWrap(12, 'lorem ipsum dolor sit amet'), expected)
    expected = os.linesep.join(('first half', 'second half'))
    self.assertEqual(wordWrap(20, 'first half <br> second half'), expected)

  def test_exact_fit_stays(self) -> None:
    self.assertEqual(wordWrap(5, 'ab cd'), 'ab cd')
    self.assertEqual(wordWrap(4, 'ab cd'), os.linesep.join(('ab', 'cd')))

  def test_long_word_on_its_own_line(self) -> None:
    expected = os.linesep.join(('abcdef', 'gh'))
    self.assertEqual(wordWrap(3, 'abcdef gh'), expected)
    expected = os.linesep.join(('a', 'abcdef', 'b'))
    self.assertEqual(wordWrap(3, 'a abcdef b'), expected)

  def test_width_one(self) -> None:
    self.assertEqual(wordWrap(1, 'a b'), os.linesep.join(('a', 'b')))

  def test_words_sorting_before_the_token_kept(self) -> None:
    #  Only a word equal to the token breaks the line; '1' and '('
    #  sort before '<br>' and must stay.
    self.assertEqual(wordWrap(20, 'a 1 ( b'), 'a 1 ( b')

  def test_no_text(self) -> None:
    self.assertEqual(wordWrap(10), '')
    self.assertEqual(wordWrap(10, ''), '')
    self.assertEqual(wordWrap(10, '   '), '')

  def test_fragments_joined(self) -> None:
    self.assertEqual(wordWrap(100, 'a b', 'c  d', ' e'), 'a b c d e')

  def test_break_token_any_case(self) -> None:
    expected = os.linesep.join(('a', 'b'))
    self.assertEqual(wordWrap(20, 'a <BR> b'), expected)
    self.assertEqual(wordWrap(20, 'a <Br> b'), expected)

  def test_custom_break_token(self) -> None:
    expected = os.linesep.join(('a', 'b'))
    self.assertEqual(wordWrap(20, 'a // b', newLine='//'), expected)
    self.assertEqual(wordWrap(20, 'a <x> b', newLine=' <X> '), expected)
    self.assertEqual(wordWrap(20, 'a <br> b', newLine='//'), 'a <br> b')

  def test_leading_break_gives_empty_first_line(self) -> None:
    self.assertEqual(wordWrap(10, '<br> a'), os.linesep.join(('', 'a')))

  def test_width_not_int_refused(self) -> None:
    for width in ('10', 10.0, None):
      with self.subTest(width=width):
        with self.assertRaises(TypeException) as context:
          wordWrap(width, 'a')
        self.assertEqual(context.exception.varName, 'width')
        self.assertIs(context.exception.actualObject, width)
        self.assertIs(context.exception.actualType, type(width))
        self.assertEqual(context.exception.expectedTypes, (int,))
        self.assertIn("'width'", str(context.exception))

  def test_width_below_one_refused(self) -> None:
    for width in (0, -3):
      with self.subTest(width=width):
        with self.assertRaises(ValueError) as context:
          wordWrap(width, 'a')
        self.assertIn('received: %d' % width, str(context.exception))

  def test_fragment_not_str_refused(self) -> None:
    with self.assertRaises(TypeException) as context:
      wordWrap(10, 'a', 7)
    self.assertEqual(context.exception.varName, 'line')
    self.assertEqual(context.exception.actualObject, 7)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'line'", str(context.exception))
    self.assertIn("'int'", str(context.exception))

  def test_random_text_fits_width(self) -> None:
    self.randomWord = WordSampler(seed=21, size=40)
    words = self.randomWord.row
    for width in (6, 9, 12, 20):
      wrapped = wordWrap(width, ' '.join(words))
      lines = wrapped.split(os.linesep)
      with self.subTest(width=width):
        self.assertEqual(' '.join(wrapped.split()), ' '.join(words))
        for line in lines:
          self.assertTrue(len(line) <= width or ' ' not in line)

  def test_unknown_keyword_warned(self) -> None:
    expected = """'worktoy.utilities.wordWrap' received the keyword
    'newline', which it does not read, and went on without it! It reads:
    'newLine'."""
    with self.assertWarns(RedundantKeyword) as context:
      line = sys._getframe().f_lineno + 1
      text = wordWrap(20, 'first half | second half', newline='|')
    self.assertEqual(text, 'first half | second%shalf' % os.linesep)
    warning = context.warning
    self.assertIs(warning.receiver, wordWrap)
    self.assertEqual(warning.keyword, 'newline')
    self.assertEqual(warning.options, ('newLine',))
    self.assertEqual(str(warning), str.join(' ', expected.split()))
    self.assertEqual(context.filename, HERE)
    self.assertEqual(context.lineno, line)
    with self.assertWarns(RedundantKeyword):
      text = wordWrap(20, newline='|')
    self.assertEqual(text, '')
