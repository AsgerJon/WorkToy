"""TestJoinWords tests the joinWords function"""
#  AGPL-3.0 license
#  Copyright (c) 2024-2026 Asger Jon Vistisen
from __future__ import annotations

from . import UtilitiesTest
from worktoy.utilities import joinWords


class TestJoinWords(UtilitiesTest):
  """TestJoinWords tests the joinWords function"""

  def test_empty(self) -> None:
    """Tests if joinWords correctly returns an empty string when
    receiving no arguments"""
    self.assertIsInstance(joinWords(), str)
    self.assertFalse(joinWords())

  def test_single(self) -> None:
    """Tests if joinWords correctly returns the single string as is"""
    self.assertEqual(joinWords('hello'), 'hello')

  def test_double(self) -> None:
    """Tests if joinWords correctly joins two strings"""
    self.assertEqual(joinWords('hello', 'world'), 'hello and world')

  def test_many(self, ) -> None:
    """Tests if joinWords correctly joins many strings"""
    sample = 'Tom', 'Dick', 'Harry'
    expected = 'Tom, Dick and Harry'
    self.assertEqual(joinWords(*sample), expected)

  def test_list(self) -> None:
    """Tests a list"""
    sampleTuple = 'Tom', 'Dick', 'Harry'
    sampleList = [*sampleTuple, ]
    tupleRes = joinWords(sampleTuple, )
    listRes = joinWords(sampleList, )
    self.assertEqual(tupleRes, listRes)

  def test_not_str(self, ) -> None:
    """Tests passing an object not of str and not of tuple or list"""
    intWord = 80085
    floatWord = .1337
    complexWord = 69 + 420j
    for word in [intWord, floatWord, complexWord]:
      self.assertEqual(str(word), joinWords(word))

  def test_sep_two(self) -> None:
    """The two-word path honors a custom 'sep' connector."""
    self.assertEqual(joinWords('tea', 'coffee', sep='or'),
                     'tea or coffee')

  def test_sep_many(self) -> None:
    """A custom 'sep' must apply to the final connector when more
    than two words are supplied."""
    sample = 'Tom', 'Dick', 'Harry'
    expected = 'Tom, Dick or Harry'
    self.assertEqual(joinWords(*sample, sep='or'), expected)

  def test_sep_list(self) -> None:
    """A custom 'sep' must survive the single-argument list/tuple
    unwrapping path."""
    sampleTuple = 'Tom', 'Dick', 'Harry'
    sampleList = [*sampleTuple, ]
    expected = 'Tom, Dick or Harry'
    self.assertEqual(joinWords(sampleTuple, sep='or'), expected)
    self.assertEqual(joinWords(sampleList, sep='or'), expected)

  def test_sep_pair_in_list(self) -> None:
    """A two-element list with custom 'sep' must not regress to the
    default 'and' connector."""
    self.assertEqual(joinWords(['tea', 'coffee'], sep='or'),
                     'tea or coffee')

  def test_mixed_trailing_list(self) -> None:
    """A plain arg followed by a list must flatten, not stringify
    the list as a Python repr."""
    self.assertEqual(joinWords('Tom', ['Dick', 'Harry']),
                     'Tom, Dick and Harry')

  def test_mixed_leading_list(self) -> None:
    """A list followed by plain args must flatten in source order."""
    self.assertEqual(joinWords(['Tom', 'Dick'], 'Harry'),
                     'Tom, Dick and Harry')

  def test_mixed_two_lists(self) -> None:
    """Multiple iterable args must all flatten into the result."""
    self.assertEqual(joinWords(['Tom', 'Dick'], ['Harry']),
                     'Tom, Dick and Harry')

  def test_mixed_with_tuples(self) -> None:
    """Tuples interleaved with plain args flatten like lists do."""
    self.assertEqual(joinWords(('Tom',), 'Dick', ('Harry',)),
                     'Tom, Dick and Harry')

  def test_nested_iterables(self) -> None:
    """A list nested inside another list must flatten through
    every level."""
    self.assertEqual(joinWords([['Tom', 'Dick'], 'Harry']),
                     'Tom, Dick and Harry')

  def test_mixed_with_sep(self) -> None:
    """Mixed flat / iterable args still honor a custom 'sep'."""
    self.assertEqual(joinWords('Tom', ['Dick', 'Harry'], sep='or'),
                     'Tom, Dick or Harry')

  def test_str_inside_mixed_stays_atomic(self) -> None:
    """Strings inside a mixed call must not be split character by
    character even though str is iterable."""
    self.assertEqual(joinWords(['abc', 'def'], 'ghi'),
                     'abc, def and ghi')
