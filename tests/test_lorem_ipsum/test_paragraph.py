"""
TestParagraph tests the 'Paragraph' class from the
'worktoy.examples.lorem_ipsum' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from random import randint

from worktoy.lorem_ipsum import Paragraph

from . import LoremIpsumTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestParagraph(LoremIpsumTest):
  """
  TestParagraph provides tests for the 'Paragraph' class from the
  'worktoy.examples.lorem_ipsum' package.
  """

  def setUp(self) -> None:
    super().setUp()
    self.paragraph = Paragraph()
    self.paragraph.reset()
    self.minLen = 300
    self.maxLen = 1500

  def test_lengths(self, ) -> None:
    """
    Testing that the 'Clause' correctly realizes clauses.
    """
    lengths = sorted([randint(self.minLen, self.maxLen) for _ in range(16)])
    paragraph = Paragraph()
    self.assertEqual(len(paragraph), Paragraph.__fallback_count__)
    for length in lengths:
      paragraph = Paragraph(length)
      self.assertIsInstance(paragraph, Paragraph)
      self.assertEqual(len(paragraph), length)

  def test_recursion_guard(self, ) -> None:
    """
    Testing the 'RecursionError' guards.
    """
    paragraph = Paragraph(self.paragraph)
    paragraph.clear()
    with self.assertRaises(RecursionError):
      _ = paragraph._getSentenceArray(_recursion=True)
    with self.assertRaises(RecursionError):
      _ = paragraph._getSentenceLengths(_recursion=True)

  def test_iteration(self) -> None:
    """
    Testing iteration of 'Paragraph'.
    """
    paragraph = Paragraph(self.paragraph)
    paragraph.reset()
    paragraphRepr = repr(paragraph)
    for sentence in paragraph:
      for clause in sentence:
        for word in clause:
          self.assertIn(word, paragraphRepr)

  def test_init(self, ) -> None:
    """
    Testing initialization of 'Paragraph'.
    """
    paragraph = Paragraph()
    paragraph.clear()
    self.assertIsInstance(paragraph, Paragraph)
    sentences = (*paragraph.sentenceArray,)
    for left, right in zip(paragraph, sentences):
      self.assertIs(left, right)
    paragraph.clear()
    paragraph = Paragraph(paragraph)
    self.assertIsNone(paragraph.__sentences_lengths__)
    self.assertIsNone(paragraph.__sentences_array__)

  def test_str(self) -> None:
    """
    Testing the string representation of 'Paragraph'.
    """
    paragraph = Paragraph(self.paragraph)
    paragraph.reset()
    paragraphStr = str(paragraph)
    for sentence in paragraph:
      self.assertIn(str(sentence), paragraphStr)
