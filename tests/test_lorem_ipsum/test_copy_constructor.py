"""
TestCopyConstructor subclasses 'LoremIpsumTest' and pins that the copy
constructors of 'Clause', 'Sentence' and 'Paragraph' copy the first-word
flag and give the copy parts of its own. They used to drop the flag, so
'Clause(Clause.first(40)).isFirst' was 'False', and the copy of a
'Sentence' or 'Paragraph' shared its clause or sentence objects with the
original, so a change to one showed in the other.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import Clause, Sentence, Paragraph

from . import LoremIpsumTest


class TestCopyConstructor(LoremIpsumTest):
  """
  TestCopyConstructor provides tests for the copy constructors of the
  lorem generators.
  """

  def test_first_flag_copied(self) -> None:
    """The copy of a first generator is first too, and of another one
    not."""
    for cls in (Clause, Sentence):
      with self.subTest(cls=cls.__name__):
        self.assertTrue(cls(cls.first(40)).isFirst)
        self.assertFalse(cls(cls(40)).isFirst)
    self.assertTrue(Paragraph(Paragraph(200)).isFirst)

  def test_sentence_parts_own(self) -> None:
    """The copy of a 'Sentence' renders as the original and holds clauses
    of its own."""
    original = Sentence(80)
    text = str(original)
    copied = Sentence(original)
    self.assertEqual(str(copied), text)
    for mine, theirs in zip(copied, original):
      self.assertIsNot(mine, theirs)

  def test_paragraph_parts_own(self) -> None:
    """The copy of a 'Paragraph' renders as the original and holds
    sentences of its own."""
    original = Paragraph(200)
    text = str(original)
    copied = Paragraph(original)
    self.assertEqual(str(copied), text)
    for mine, theirs in zip(copied, original):
      self.assertIsNot(mine, theirs)
