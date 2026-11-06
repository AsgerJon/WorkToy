"""
TestReplaceFlex tests 'replaceFlex' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import replaceFlex
from . import UtilitiesTest


class TestReplaceFlex(UtilitiesTest):
  """
  'replaceFlex' rewrites one chosen occurrence of a substring, counted
  from one, where 'str.replace' rewrites the first so many. The tests
  pin the docstring examples, the default, an occurrence that is not
  there, the refusal of a count below one, and that overlapping
  matches are counted.
  """

  def test_docstring_examples(self) -> None:
    text = 'foo bar foo baz foo'
    self.assertEqual(replaceFlex(text, 'foo', 'X', 2), 'foo bar X baz foo')
    self.assertEqual(replaceFlex('abc', 'x', 'y'), 'abc')

  def test_default_is_first(self) -> None:
    self.assertEqual(replaceFlex('a-a-a', 'a', 'b'), 'b-a-a')
    self.assertEqual(replaceFlex('a-a-a', 'a', 'b', None), 'b-a-a')

  def test_each_occurrence(self) -> None:
    text = 'x x x x'
    for n in range(1, 5):
      expected = ' '.join('y' if i == n else 'x' for i in range(1, 5))
      with self.subTest(n=n):
        self.assertEqual(replaceFlex(text, 'x', 'y', n), expected)

  def test_beyond_last_unchanged(self) -> None:
    self.assertEqual(replaceFlex('x x x x', 'x', 'y', 5), 'x x x x')

  def test_count_below_one_refused(self) -> None:
    for n in (0, -1):
      with self.subTest(n=n):
        with self.assertRaises(ValueError) as context:
          replaceFlex('abc', 'a', 'b', n)
        self.assertIn('n=%d' % n, str(context.exception))

  def test_overlapping_matches_counted(self) -> None:
    self.assertEqual(replaceFlex('aaa', 'aa', 'b', 2), 'ab')

  def test_replacement_length_free(self) -> None:
    self.assertEqual(replaceFlex('a.b.c', '.', '::', 2), 'a.b::c')
    self.assertEqual(replaceFlex('a.b.c', '.', '', 1), 'ab.c')
