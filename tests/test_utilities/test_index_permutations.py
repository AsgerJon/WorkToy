"""
TestIndexPermutations tests 'indexPermutations' from
'worktoy.utilities.combinatorics'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from itertools import permutations
from math import factorial

from worktoy.utilities.combinatorics import indexPermutations
from . import UtilitiesTest


class TestIndexPermutations(UtilitiesTest):
  """
  'indexPermutations' yields every ordering of the positions of a tuple
  of a given length, in lexicographic order, and refuses a negative
  length when called rather than when first drawn from. The tests pin
  the docstring example, the two smallest lengths, the count and the
  order up to length five, and the moment of the refusal.
  """

  def test_docstring_example(self) -> None:
    expected = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1),
                (2, 1, 0)]
    self.assertEqual(list(indexPermutations(3)), expected)

  def test_smallest_lengths(self) -> None:
    self.assertEqual(list(indexPermutations(0)), [()])
    self.assertEqual(list(indexPermutations(1)), [(0,)])
    self.assertEqual(list(indexPermutations(2)), [(0, 1), (1, 0)])

  def test_count_and_order(self) -> None:
    for n in range(6):
      found = list(indexPermutations(n))
      with self.subTest(n=n):
        self.assertEqual(len(found), factorial(n))
        self.assertEqual(found, sorted(found))
        self.assertEqual(len(set(found)), len(found))
        self.assertEqual(found, list(permutations(range(n))))

  def test_negative_refused_at_call(self) -> None:
    with self.assertRaises(ValueError) as context:
      indexPermutations(-1)
    self.assertIn('non-negative', str(context.exception))

  def test_returns_iterator(self) -> None:
    found = indexPermutations(2)
    self.assertEqual(next(found), (0, 1))
    self.assertEqual(next(found), (1, 0))
    with self.assertRaises(StopIteration) as context:
      next(found)
    self.assertEqual(context.exception.args, ())
