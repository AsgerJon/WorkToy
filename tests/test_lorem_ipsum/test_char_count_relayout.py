"""
TestCharCountRelayout subclasses 'LoremIpsumTest' and pins that assigning
'charCount' to a lorem generator drops the layout it cached, so the next
rendering has the new length. Nothing used to clear the cached layout on
assignment, and a generator rendered once kept the old count until
'reset' was called.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import Clause, Sentence, Paragraph

from . import LoremIpsumTest


class TestCharCountRelayout(LoremIpsumTest):
  """
  TestCharCountRelayout provides tests for assigning 'charCount' to a
  lorem generator already rendered.
  """

  def test_clause(self) -> None:
    """A rendered 'Clause' renders at the new count."""
    clause = Clause(30)
    self.assertEqual(len(str(clause)), 30)
    clause.charCount = 60
    self.assertEqual(len(str(clause)), 60)

  def test_first_clause(self) -> None:
    """A rendered first 'Clause' renders at the new count and keeps its
    lead-in."""
    clause = Clause.first(30)
    str(clause)
    clause.charCount = 60
    self.assertEqual(len(str(clause)), 60)
    self.assertTrue(str(clause).startswith('Lorem ipsum'))

  def test_sentence(self) -> None:
    """A rendered 'Sentence' renders at the new count."""
    sentence = Sentence(40)
    self.assertEqual(len(str(sentence)), 40)
    sentence.charCount = 90
    self.assertEqual(len(str(sentence)), 90)

  def test_paragraph(self) -> None:
    """A rendered 'Paragraph' renders at the new count."""
    paragraph = Paragraph(100)
    self.assertEqual(len(str(paragraph)), 100)
    paragraph.charCount = 300
    self.assertEqual(len(str(paragraph)), 300)

  def test_layout_kept_between_reads(self) -> None:
    """Without an assignment, a generator keeps its layout from one read
    to the next."""
    sentence = Sentence(80)
    self.assertEqual(str(sentence), str(sentence))
