"""
TestArrangements tests 'Arrangements' from 'worktoy.utilities.combinatorics'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from itertools import permutations
from math import factorial

from worktoy.utilities.combinatorics import Arrangements, Arrangement
from worktoy.work_test.samplers import WordSampler
from . import UtilitiesTest


class TestArrangements(UtilitiesTest):
  """
  'Arrangements' holds every distinct ordering of a ground tuple, with
  orderings that read the same collapsed, so repeated items do not
  multiply the set. Items that cannot be hashed are collapsed by
  equality instead. The tests pin the docstring example, the counts
  with and without repeats, the two ways of collapsing, the sequence
  and membership API, and the peek at the lazy hashability check.
  """

  def test_docstring_example(self) -> None:
    found = [a.values for a in Arrangements('A', 'A', 'B')]
    self.assertEqual(
      found,
      [('A', 'A', 'B'), ('A', 'B', 'A'), ('B', 'A', 'A')]
      )

  def test_distinct_items(self) -> None:
    arrangements = Arrangements(1, 2, 3)
    self.assertEqual(len(arrangements), 6)
    self.assertEqual(arrangements.items, (1, 2, 3))
    self.assertEqual(len(arrangements.permutations), 6)
    for arrangement in arrangements:
      with self.subTest(arrangement=arrangement):
        self.assertIsInstance(arrangement, Arrangement)
        self.assertEqual(arrangement.items, (1, 2, 3))
    found = [a.values for a in arrangements]
    self.assertEqual(found, list(permutations((1, 2, 3))))

  def test_repeated_items_collapse(self) -> None:
    self.assertEqual(len(Arrangements('A', 'A', 'B', 'B')), 6)
    self.assertEqual(len(Arrangements('A', 'A', 'A')), 1)

  def test_empty(self) -> None:
    arrangements = Arrangements()
    self.assertEqual(len(arrangements), 1)
    self.assertEqual(arrangements[0].values, ())
    self.assertTrue(arrangements.isHashable())

  def test_hashable(self) -> None:
    self.assertTrue(Arrangements(1, 'a', (2,)).isHashable())
    self.assertFalse(Arrangements([1], [2]).isHashable())
    self.assertFalse(Arrangements(1, [2]).isHashable())
    self.assertFalse(Arrangements([1], 2).isHashable())

  def test_hashable_cached(self) -> None:
    arrangements = Arrangements(1, 2)
    self.assertTrue(arrangements.isHashable())
    self.assertTrue(arrangements.isHashable())

  def test_hashable_peek(self) -> None:
    #  '_recursion=True' asks whether the answer is computed already:
    #  'RecursionError' before, the answer after, never the computing.
    blank = Arrangements.__new__(Arrangements)
    with self.assertRaises(RecursionError) as context:
      blank.isHashable(_recursion=True)
    self.assertEqual(context.exception.args, ())
    with self.assertRaises(RecursionError) as context:
      blank.isHashable(_recursion=True)
    self.assertEqual(context.exception.args, ())
    built = Arrangements(1, 2)
    self.assertTrue(built.isHashable(_recursion=True))
    self.assertFalse(
      Arrangements([1]).isHashable(_recursion=True))

  def test_unhashable_items_collapse_by_equality(self) -> None:
    arrangements = Arrangements([1], [1], [2])
    self.assertEqual(len(arrangements), 3)
    found = [a.values for a in arrangements]
    self.assertEqual(
      found,
      [([1], [1], [2]), ([1], [2], [1]), ([2], [1], [1])]
      )
    self.assertEqual(len(Arrangements([1], [2], [3])), 6)

  def test_indexing(self) -> None:
    arrangements = Arrangements('x', 'y')
    self.assertEqual(arrangements[0].values, ('x', 'y'))
    self.assertEqual(arrangements[1].values, ('y', 'x'))
    self.assertEqual(arrangements[-1].values, ('y', 'x'))
    with self.assertRaises(IndexError):
      _ = arrangements[2]

  def test_contains(self) -> None:
    arrangements = Arrangements('x', 'y', 'z')
    self.assertIn(arrangements[3], arrangements)
    self.assertIn(Arrangement(('x', 'y', 'z'), (2, 1, 0)), arrangements)
    self.assertNotIn(Arrangement(('x', 'y', 'q'), (0, 1, 2)), arrangements)
    self.assertIn(('z', 'x', 'y'), arrangements)
    self.assertNotIn(('x', 'y'), arrangements)
    self.assertNotIn(('x', 'x', 'y'), arrangements)
    self.assertNotIn(['z', 'x', 'y'], arrangements)
    self.assertNotIn('xyz', arrangements)

  def test_random_words(self) -> None:
    self.randomWord = WordSampler(seed=9)
    for n in range(1, 6):
      self.randomWord.size = n
      words = self.randomWord.row
      arrangements = Arrangements(*words)
      expected = set(permutations(words))
      with self.subTest(words=words):
        self.assertEqual(len(arrangements), len(expected))
        self.assertEqual({a.values for a in arrangements}, expected)
        self.assertTrue(len(arrangements) <= factorial(n))
