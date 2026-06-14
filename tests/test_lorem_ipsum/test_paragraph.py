"""
TestParagraph tests the 'Paragraph' class from the
'worktoy.lorem_ipsum' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint

from worktoy.lorem_ipsum import Paragraph
from . import LoremIpsumTest


class TestParagraph(LoremIpsumTest):
  """
  TestParagraph provides tests for the 'Paragraph' class from the
  'worktoy.lorem_ipsum' package.
  """

  def setUp(self) -> None:
    super().setUp()
    self.paragraph: Paragraph = Paragraph()
    self.paragraph.reset()
    self.minLen: int = 300
    self.maxLen: int = 1500

  def test_lengths(self, ) -> None:
    """
    Testing that 'Paragraph' realizes to exactly the requested character
    count.
    """
    lengths = [randint(self.minLen, self.maxLen) for _ in range(16)]
    paragraph = Paragraph()
    self.assertEqual(len(paragraph), paragraph.charCount)
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

  def test_realize(self) -> None:
    """
    This method tests that 'realize' matches '__str__'.
    """
    expectedText = str(self.paragraph)
    actualText = self.paragraph.realize()
    self.assertEqual(expectedText, actualText)

  def test_short_charcount(self) -> None:
    """
    A 'charCount' below the sentence distribution's minimum collapses to a
    single sentence length equal to 'charCount', since 'Sentence' realizes
    short counts exactly through its own placeholder fallback.
    """
    short = Paragraph(20)
    self.assertLess(short.charCount, short.sentenceDist.minVal)
    self.assertEqual(short.sentenceLengths, [20])
