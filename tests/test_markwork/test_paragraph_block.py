"""
TestParagraphBlock subclasses 'MarkworkTest' and provides tests for the
'ParagraphBlock' class in the 'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
import os

from worktoy.markwork import InlineLorem, InlineLink
from worktoy.markwork import ParagraphBlock, Index
from . import MarkworkTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class Foo(ParagraphBlock):
  """
  Foo subclasses 'ParagraphBlock' and provides an example of how one might
  use 'ParagraphBlock' in a test case.
  """

  lorem1 = InlineLorem(69)
  lorem2 = InlineLorem(420)
  link1 = InlineLink(
    """https://youtube.com/watch?v=dQw4w9WgXcQ""",
    """Educational Content, fr fr, trust me bro!""",
    """Rick Astley - Never Gonna Give You Up (Video)""",
    )
  lorem3 = InlineLorem()


class Bar(Index):
  """
  Bar subclasses 'Index' and provides an example of how one might use 'Index'
  in a test case.
  """
  __fallback_dir__ = os.path.abspath(os.path.dirname(__file__))

  foo = Foo('Foo')


class TestParagraphBlock(MarkworkTest):
  """
  TestParagraphBlock subclasses 'MarkworkTest' and provides tests for the
  'ParagraphBlock' class in the 'worktoy.markwork' package.
  """

  def test_dev_null(self) -> None:
    self.assertTrue(True)
