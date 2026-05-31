"""
TestClause tests the 'Clause' class from the
'worktoy.examples.lorem_ipsum' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

from tests.test_lorem_ipsum import LoremIpsumTest
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
    self.assertEqual(len(clause), clause.charCount)
    clause.clear()
    clause = Clause(clause)
    self.assertEqual(len(clause), clause.charCount)
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

  def test_realize(self) -> None:
    """
    This method tests that 'realize' matches '__str__'.
    """
    expectedText = str(self.clause)
    actualText = self.clause.realize()
    self.assertEqual(expectedText, actualText)

  def test_first_placeholder(self) -> None:
    """
    Testing that a first clause too short for a full word sequence degrades
    to a 'Lorem ipsum ...' placeholder of exactly the requested length,
    covering the lead-in truncation, the empty gap, and the 'etc' prefix.
    """
    cases = {
        12: 'Lorem ips...',
        14: 'Lorem ipsum...',
        15: 'Lorem ipsum ...',
        16: 'Lorem ipsum e...',
        17: 'Lorem ipsum et...',
        18: 'Lorem ipsum etc...',
    }
    for length, expected in cases.items():
      self.assertEqual(str(Clause.first(length)), expected)
    #  A gap of four or more characters draws a real word.
    for length in range(19, 24):
      clause = Clause.first(length)
      self.assertEqual(len(str(clause)), length)
      self.assertTrue(str(clause).startswith('Lorem ipsum '))
      self.assertTrue(str(clause).endswith('...'))
    #  Reading the cached lengths of a placeholder reads them back from the
    #  realized words rather than partitioning.
    clause = Clause.first(16)
    self.assertEqual(clause.wordsLengths, [len(w) for w in clause.wordsArray])
