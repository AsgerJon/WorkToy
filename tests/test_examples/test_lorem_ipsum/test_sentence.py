"""
TestSentence tests the 'Sentence' class from the
'worktoy.examples.lorem_ipsum' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from random import randint

from worktoy.lorem_ipsum import Sentence

from . import LoremIpsumTest

if TYPE_CHECKING:  # pragma: no cover
  pass

CHI2_6SIGMA_DOF4 = 55.52


class TestSentence(LoremIpsumTest):
  """
  TestSentence provides tests for the 'Sentence' class from the
  'worktoy.examples.lorem_ipsum' package.
  """

  def setUp(self) -> None:
    super().setUp()
    self.sentence = Sentence()
    self.sentence.reset()
    self.minLen = 60
    self.maxLen = 150

  def test_lengths(self, ) -> None:
    """
    Testing that the 'Clause' correctly realizes clauses.
    """
    lengths = sorted([randint(self.minLen, self.maxLen) for _ in range(16)])
    self.assertEqual(len(self.sentence), Sentence.__fallback_count__)
    for length in lengths:
      sentence = Sentence(length)
      self.assertIsInstance(sentence, Sentence)
      self.assertEqual(len(sentence), length)

  def test_iterations(self) -> None:
    """
    Testing iteration of 'Sentence'.
    """
    sentence = Sentence(self.sentence)
    sentence.reset()
    sentenceRepr = repr(sentence)
    for clause in sentence:
      for word in clause:
        self.assertIn(word, sentenceRepr)

  def test_init(self) -> None:
    """
    Testing initialization of 'Sentence'.
    """
    sentence = Sentence()
    sentence.clear()
    self.assertIsInstance(sentence, Sentence)
    clauses = (*sentence.clausesArray,)
    for left, right in zip(sentence, clauses):
      self.assertIs(left, right)
    sentence.clear()
    sentence = Sentence(sentence)
    self.assertIsNone(sentence.__clause_lengths__)
    self.assertIsNone(sentence.__clause_array__)

  def test_recursion_guard(self, ) -> None:
    """
    Testing the 'RecursionError' guards.
    """
    sentence = Sentence(self.sentence)
    sentence.clear()
    with self.assertRaises(RecursionError):
      _ = sentence._getClausesArray(_recursion=True)
    with self.assertRaises(RecursionError):
      _ = sentence._getClauseLengths(_recursion=True)
