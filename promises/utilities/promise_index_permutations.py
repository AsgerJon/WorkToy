"""
PromiseIndexPermutations promises 'indexPermutations' from
'worktoy.utilities.combinatorics'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from math import factorial
from unittest import TestCase

from worktoy.utilities.combinatorics import indexPermutations


class PromiseIndexPermutations(TestCase):
  """
  'indexPermutations(n)' gives an iterator over every permutation of
  '(0, 1, ..., n - 1)', 'n!' tuples in lexicographic order. A negative
  'n' raises 'ValueError' at the call, before anything is drawn.
  Source: the 'indexPermutations' docstring and its example.
  """

  def test_example(self) -> None:
    expected = [
      (0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0),
    ]
    self.assertEqual(list(indexPermutations(3)), expected)

  def test_count_and_order(self) -> None:
    permutations = list(indexPermutations(5))
    self.assertEqual(len(permutations), factorial(5))
    self.assertEqual(permutations, sorted(permutations))
    self.assertEqual(list(indexPermutations(0)), [()])

  def test_negative(self) -> None:
    with self.assertRaises(ValueError):
      indexPermutations(-1)
