"""
TestInlineText tests the Inline classes from the 'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import maybe, ExceptionInfo
from worktoy.lorem_ipsum import Paragraph, Sentence
from worktoy.markwork import InlineBase, InlineText, InlineLink

from . import MarkworkTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Self, Any, Never

  InlineTexts: TypeAlias = tuple[InlineText, ...]


class TestInlineText(MarkworkTest):
  """
  TestInlineText tests the InlineText classes from the 'worktoy.markwork'
  package.
  """

  def test_init(self):
    """
    This method tests each overloaded constructor of the 'InlineText'
    class, which provides the following constructor overloads:

    Overloaded Constructors
    -----------------------
    @overload(str)
    def __init__(self, text: str) -> None: ...

    @overload(THIS)
    def __init__(self, other: Self) -> None: ...

    @overload()
    def __init__(self, ) -> None: ...
    """
    inlineText = InlineText('Hello, World!')
    self.assertEqual(inlineText.text, 'Hello, World!')
    inlineEmpty = InlineText()
    self.assertFalse(inlineEmpty.text)
    self.assertFalse(inlineEmpty)
    inlineClone = InlineText(inlineText)
    self.assertEqual(inlineClone.text, 'Hello, World!')
    self.assertEqual(inlineClone, inlineText)

  def test_str_repr(self) -> None:
    """
    Test the string representation of the 'Inline' class.
    """
    for inlineText in self.randomInlineTexts():
      self.assertIn(inlineText.text, str(inlineText))
      self.assertIn(inlineText.text, repr(inlineText))

  def test_add(self, ) -> None:
    """
    Test the addition of 'Inline' instances.
    """
    other = """Never gonna give you up"""
    for inlineText in self.randomInlineTexts():
      added = inlineText + other
      iAdded = InlineText()
      iAdded += inlineText
      iAdded += other
      rAdded = other + inlineText
      additions = (added, iAdded, rAdded)
      for addition in additions:
        self.assertIsInstance(addition, InlineText)
        self.assertIn(inlineText.text, addition.text)
        self.assertIn(other, addition.text)

  def test_contains(self, ) -> None:
    """
    Tests the 'in' operator for 'InlineText' instances.
    """
    for _ in range(10):
      sentence = Sentence(100)
      sentenceText = str(sentence)
      inlineText = InlineText(sentenceText)
      for word in sentenceText.split():
        for item in (word, InlineText(word)):
          self.assertIn(item, inlineText)
    self.assertFalse(self in InlineText())

  def test_eq(self, ) -> None:
    """
    Tests the equality operator for 'InlineText' instances.
    """
    for inlineText in self.randomInlineTexts():
      clone = InlineText(inlineText)
      self.assertEqual(inlineText, clone)
      self.assertIsNot(inlineText, clone)

  def test_len(self, ) -> None:
    """
    Tests the length of 'InlineText' instances.
    """
    for inlineText in self.randomInlineTexts():
      self.assertEqual(len(inlineText), len(str.split(inlineText.text, )))

  def test_iter(self, ) -> None:
    """
    Tests the iteration of 'InlineText' instances.
    """
    for inlineText in self.randomInlineTexts():
      for word in inlineText:
        self.assertIn(word, inlineText.text)

  def test_bool(self, ) -> None:
    """
    Tests the boolean value of 'InlineText' instances.
    """
    inlineEmpty = InlineText()
    for inlineText in self.randomInlineTexts():
      self.assertTrue(inlineText)
      self.assertFalse(inlineEmpty)
      inlineEmpty = InlineText(inlineEmpty)

  def test_bad_operand(self, ) -> None:
    """
    Tests the behavior of 'InlineText' instances when given an operand of an
    unsupported type.
    """
    badOperands = (69, (420,), lambda: 1337, object())
    inlineText = InlineText()

    for operand in badOperands:
      with self.assertRaises(TypeError):
        _ = inlineText + operand
      with self.assertRaises(TypeError):
        inlineText += operand
      with self.assertRaises(TypeError):
        _ = operand + inlineText
      self.assertFalse(operand in inlineText)
      self.assertNotEqual(inlineText, operand)
