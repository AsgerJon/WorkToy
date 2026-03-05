"""
TestClause tests the 'Clause' class from the
'worktoy.examples.lorem_ipsum' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

from tests.test_examples.test_lorem_ipsum import LoremIpsumTest
from worktoy.lorem_ipsum import Clause

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestClause(LoremIpsumTest):
  """
  TestClause provides tests for the 'Clause' class from the
  'worktoy.examples.lorem_ipsum' package.
  """

  def setUp(self) -> None:
    super().setUp()
    self.clause = Clause()
    self.clause.reset()
    self.minLen = 30
    self.maxLen = 80

  def test_lengths(self, ) -> None:
    """
    Testing that the 'Clause' correctly realizes clauses.
    """
    lengths = sorted([randint(30, 80) for _ in range(16)])
    clause = Clause(self.clause)
    self.assertEqual(len(clause), Clause.__fallback_count__)
    clause.clear()
    clause = Clause(clause)
    self.assertEqual(len(clause), Clause.__fallback_count__)
    for length in lengths:
      clause = Clause(length)
      self.assertIsInstance(clause, Clause)
      self.assertEqual(len(clause), length)

  def test_iteration(self) -> None:
    """
    Testing that the 'Clause' correctly realizes clauses.
    """
    clause = Clause(self.clause)
    self.assertIsInstance(clause, Clause)
    for word in clause:
      self.assertIsInstance(word, str)

  def test_recursion_guard(self, ) -> None:
    """
    Testing the 'RecursionError' guards.
    """
    clause = Clause(self.clause)
    clause.clear()
    with self.assertRaises(RecursionError):
      _ = clause._getWordsArray(_recursion=True)
    with self.assertRaises(RecursionError):
      _ = clause._getWordsLengths(_recursion=True)
