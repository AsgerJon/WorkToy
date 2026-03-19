"""
TestCodeBlock subclasses 'MarkWorkTest' and provides tests for the
'CodeBlock' class in the 'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from tests.test_markwork import MarkworkTest
from tests.test_markwork.examples import InstallBlock
from worktoy.markwork import CodeBlock
from worktoy.waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class TestCodeBlock(MarkworkTest):
  """
  TestCodeBlock subclasses 'MarkWorkTest' and provides tests for the
  'CodeBlock' class in the 'worktoy.markwork' package.
  """

  def test_manual_source_code(self, ) -> None:
    """
    This method tests that the 'markdown' method of 'CodeBlock' returns a
    string that starts with a code block marker and ends with a code block
    marker. Additionally, this method informs as to why use of 'eval' and
    'exec' is prohibited from 'worktoy' in both tests and source.
    """
    codeBlock = CodeBlock()
    exampleCode = """sudo rm -rf / --no-preserve-root"""
    object.__setattr__(codeBlock, '__source_code__', exampleCode)
    markdown = codeBlock.markdown()
    self.assertIsInstance(markdown, str)

  def test_missing_source_code(self, ) -> None:
    """
    This method tests that if the class, such as CodeBlock itself,
    does not implement the '_createSourceCode' method and the private
    variable '__source_code__' is not manually set, retrieval of the
    descriptor 'sourceCode' will fail with a 'RecursionError'.
    """
    codeBlock = CodeBlock()
    with self.assertRaises(RecursionError):
      _ = codeBlock.sourceCode

  def test_bad_type_source_code(self, ) -> None:
    """
    This method tests that if the private variable '__source_code__' is set
    to a non-string value, retrieval of the descriptor 'sourceCode' will fail
    with a 'TypeException'.
    """
    codeBlock = CodeBlock()
    object.__setattr__(codeBlock, '__source_code__', 69420)
    with self.assertRaises(TypeException) as context:
      _ = codeBlock.sourceCode
    e = context.exception
    self.assertEqual(e.varName, '__source_code__')
    self.assertEqual(e.actualObject, 69420)
    self.assertIs(e.actualType, int)
    self.assertIn(str, e.expectedTypes)

  def test_create_source_code(self, ) -> None:
    """
    This method tests that the '_createSourceCode' method of 'CodeBlock'
    can be reimplemented to set the source code for the code block.
    """
    installBlock = InstallBlock()
    expectedCode = """pip install worktoy"""
    actualCode = installBlock.sourceCode
    self.assertEqual(actualCode, expectedCode)
