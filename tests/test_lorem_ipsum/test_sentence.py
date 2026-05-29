"""
TestSentence tests the 'Sentence' class from the
'worktoy.examples.lorem_ipsum' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.lorem_ipsum import Sentence
from worktoy.work_test.samplers import IntSampler
from . import LoremIpsumTest

if TYPE_CHECKING:  # pragma: no cover
  pass

CHI2_6SIGMA_DOF4 = 55.52


class TestSentence(LoremIpsumTest):
  """
  TestSentence provides tests for the 'Sentence' class from the
  'worktoy.examples.lorem_ipsum' package.
  """

  randomInteger = IntSampler(69, 420)

  def setUp(self) -> None:
    """
    Sets the 'charCount' of the 'randomLorem'.
    """
    super().setUp()
    self.sentence = Sentence()
    self.randomLorem.charCount = 69

  def test_lengths(self, ) -> None:
    """
    Testing that the 'Clause' correctly realizes clauses.
    """
    self.randomInteger.rowCount = 10
    for length in self.randomInteger.row:
      sentence = Sentence(length)
      self.assertIsInstance(sentence, Sentence)
      self.assertEqual(len(sentence), length)

  def test_iterations(self) -> None:
    """
    Testing iteration of 'Sentence'.
    """
    sentence = Sentence()
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
    sentence.reset()
    self.assertIsNotNone(sentence.__clause_lengths__)
    self.assertIsNotNone(sentence.__clause_array__)
    sentence = Sentence(sentence)
    self.assertIsNotNone(sentence.__clause_lengths__)
    self.assertIsNotNone(sentence.__clause_array__)

  def test_recursion_guard(self, ) -> None:
    """
    Testing the 'RecursionError' guards.
    """
    sentence = Sentence(Sentence())
    sentence.clear()
    with self.assertRaises(RecursionError):
      _ = sentence._getClausesArray(_recursion=True)
    with self.assertRaises(RecursionError):
      _ = sentence._getClauseLengths(_recursion=True)

  def test_realize(self) -> None:
    """
    This method tests that 'realize' matches '__str__'.
    """
    expectedText = str(self.sentence)
    actualText = self.sentence.realize()
    self.assertEqual(expectedText, actualText)
