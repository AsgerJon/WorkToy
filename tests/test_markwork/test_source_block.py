"""
TestSourceBlock subclasses 'MarkWorkTest' and provides tests for the
'SourceBlock' class in the 'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import SourceBlock, InlineText, InlineLorem
from worktoy.waitaminute import MissingVariable, TypeException
from . import MarkworkTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class TestSourceBlock(MarkworkTest):
  """
  TestSourceBlock subclasses 'MarkWorkTest' and provides tests for the
  'SourceBlock' class in the 'worktoy.markwork' package.
  """

  def test_init(self, ) -> None:
    """
    This method test the constructor added by 'SourceBlock' which takes a
    class as argument and sets it as the example class. Please note that
    readers sensitive to potential self-referential code should proceed
    with caution.
    """
    sourceBlock = SourceBlock(type(self))
    self.assertIs(sourceBlock.exampleClass, type(self))
    sourceCode = sourceBlock.markdown()
    self.assertIn('class TestSourceBlock(MarkworkTest):', sourceCode)

  def test_missing_example_class(self, ) -> None:
    """
    This method tests that if the example class is not set,
    a 'MissingVariable'
    exception is raised.
    """
    sourceBlock = SourceBlock()
    with self.assertRaises(MissingVariable) as context:
      _ = sourceBlock.exampleClass
    e = context.exception
    self.assertIs(e.instance, SourceBlock.exampleClass)
    self.assertEqual(e.varName, '__example_class__')
    self.assertIs(e.type_, type)

  def test_bad_example_class(self, ) -> None:
    """
    This method tests that if the example class is set to a non-type value,
    a 'TypeException' exception is raised.
    """

    sourceBlock = SourceBlock()
    object.__setattr__(sourceBlock, '__example_class__', print)
    with self.assertRaises(TypeException) as context:
      _ = sourceBlock.exampleClass
    e = context.exception
    self.assertEqual(e.varName, '__example_class__')
    self.assertIs(e.actualObject, print)
    self.assertIs(e.actualType, type(print))
    self.assertIn(type, e.expectedTypes)

  def test_example_class_bad_set(self, ) -> None:
    """
    This method tests that if the example class is set to a non-type value,
    a 'TypeException' exception is raised.
    """

    sourceBlock = SourceBlock()
    with self.assertRaises(TypeException) as context:
      sourceBlock.exampleClass = print
    e = context.exception
    self.assertEqual(e.varName, 'value')
    self.assertIs(e.actualObject, print)
    self.assertIs(e.actualType, type(print))
    self.assertIn(type, e.expectedTypes)

  def test_disabled_register(self, ) -> None:
    """
    This method tests that 'registerInline' is disabled for 'SourceBlock'.
    """

    with self.assertRaises(TypeError):
      class Sus(SourceBlock):
        trolololo = InlineLorem()
 