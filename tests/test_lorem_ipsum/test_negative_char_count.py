"""
TestNegativeCharCount subclasses 'LoremIpsumTest' and pins that the lorem
generators refuse a negative 'charCount' with 'ValueError'. They accepted
one and rendered the empty string, or raised later, as the text was laid
out.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import Clause, Sentence, Paragraph
from worktoy.waitaminute import TypeException

from . import LoremIpsumTest


class TestNegativeCharCount(LoremIpsumTest):
  """
  TestNegativeCharCount provides tests for a negative 'charCount'.
  """

  def test_constructors_refuse(self) -> None:
    """Each generator refuses a negative count, by position or keyword."""
    for cls in (Clause, Sentence, Paragraph):
      with self.subTest(generator=cls.__name__):
        with self.assertRaises(ValueError):
          cls(-1)
        with self.assertRaises(ValueError):
          cls(charCount=-3)

  def test_assignment_refused(self) -> None:
    """Assigning a negative count raises and keeps the count it had."""
    paragraph = Paragraph()
    with self.assertRaises(ValueError):
      paragraph.charCount = -5
    self.assertEqual(paragraph.charCount, 40)

  def test_cast_value_refused(self) -> None:
    """A value the box casts to a negative 'int' is refused too."""
    sentence = Sentence(20)
    with self.assertRaises(ValueError):
      sentence.charCount = -2.0
    self.assertEqual(sentence.charCount, 20)

  def test_zero_allowed(self) -> None:
    """A count of zero is no text at all, which a sentence renders."""
    self.assertEqual(str(Sentence(0)), '')

  def test_cast_value_allowed(self) -> None:
    """A value the box casts to a count of zero or more is stored."""
    sentence = Sentence(20)
    sentence.charCount = 7.0
    self.assertEqual(sentence.charCount, 7)

  def test_wrong_type_left_to_box(self) -> None:
    """A value the box cannot cast raises the 'TypeException' it did."""
    sentence = Sentence(20)
    with self.assertRaises(TypeException):
      sentence.charCount = 'many'
