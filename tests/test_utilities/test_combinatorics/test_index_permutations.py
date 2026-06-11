"""
TestIndexPermutations provides tests for the 'indexPermutations'
function from 'worktoy.utilities.combinatorics'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import CombinatoricsTest
from worktoy.utilities.combinatorics import indexPermutations


class TestIndexPermutations(CombinatoricsTest):
  """Tests for indexPermutations(n): n! tuples in lex order."""

  #  ================================================================
  #  |
  #  |                       INPUT VALIDATION
  #  ================================================================

  #  ________________________________________________________________
  #  Good input - exact small cases
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_zero_yields_empty_tuple_once(self) -> None:
    """0! = 1; the single permutation of zero elements is ()."""
    self.assertEqual(list(indexPermutations(0)), [()])

  def test_one_yields_singleton(self) -> None:
    self.assertEqual(list(indexPermutations(1)), [(0,)])

  def test_two_exact(self) -> None:
    self.assertEqual(list(indexPermutations(2)), [(0, 1), (1, 0)])

  def test_three_exact_matches_docstring(self) -> None:
    """Mirrors the example from the function's docstring."""
    expected = [
      (0, 1, 2), (0, 2, 1), (1, 0, 2),
      (1, 2, 0), (2, 0, 1), (2, 1, 0)
    ]
    self.assertEqual(list(indexPermutations(3)), expected)

  #  ________________________________________________________________
  #  Bad input - negative n
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_negative_raises(self) -> None:
    with self.assertRaises(ValueError):
      list(indexPermutations(-1))

  def test_very_negative_raises(self) -> None:
    with self.assertRaises(ValueError):
      list(indexPermutations(-100))

  #  ================================================================
  #  |
  #  |                      OUTPUT PROPERTIES
  #  |             ( invariants for any non-negative n )
  #  ================================================================

  #  ________________________________________________________________
  #  Type and shape
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_returns_an_iterator(self) -> None:
    """The function is a generator; it should not eagerly materialise."""
    from collections.abc import Iterator as IteratorABC
    g = indexPermutations(3)
    self.assertIsInstance(g, IteratorABC)
    self.assertNotIsInstance(g, list)

  def test_yields_tuples(self) -> None:
    for p in indexPermutations(4):
      self.assertIsInstance(p, tuple)

  def test_each_tuple_has_length_n(self) -> None:
    n = 4
    for p in indexPermutations(n):
      self.assertEqual(len(p), n)

  #  ________________________________________________________________
  #  Combinatorial invariants
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_count_matches_factorial(self) -> None:
    """Cardinality of the output is n! for n in 0..6."""
    for n in range(7):
      with self.subTest(n=n):
        produced = sum(1 for _ in indexPermutations(n))
        self.assertEqual(produced, self.factorial(n))

  def test_each_is_a_permutation_of_zero_to_n(self) -> None:
    n = 5
    expected = set(range(n))
    for p in indexPermutations(n):
      self.assertEqual(set(p), expected)

  def test_all_yielded_tuples_are_unique(self) -> None:
    n = 5
    seen = list(indexPermutations(n))
    self.assertEqual(len(seen), len(set(seen)))

  #  ________________________________________________________________
  #  Lexicographic order
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_lex_order(self) -> None:
    """Docstring promise: tuples are yielded in lexicographic order."""
    for n in range(6):
      with self.subTest(n=n):
        produced = list(indexPermutations(n))
        self.assertEqual(produced, sorted(produced))

  def test_first_is_identity_permutation(self) -> None:
    n = 5
    first = next(iter(indexPermutations(n)))
    self.assertEqual(first, tuple(range(n)))

  def test_last_is_reversed(self) -> None:
    n = 5
    last = list(indexPermutations(n))[-1]
    self.assertEqual(last, tuple(range(n - 1, -1, -1)))
