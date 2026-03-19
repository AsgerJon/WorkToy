"""
TestChapter subclasses 'MarkworkTest' and provides tests for the 'Chapter'
class in the 'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import Chapter, Section, SubSection, InlineLorem, Index
from . import MarkworkTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class ChapterExample(Chapter):
  """
  ChapterExample subclasses 'Chapter' and provides an example of how one
  might use 'Chapter' in a test case.
  """

  i1 = InlineLorem()
  sec1 = Section('For so long...')
  i2 = InlineLorem()


class IndexExample(Index):
  """
  IndexExample subclasses 'Index' and provides an example of how one might
  use 'Index' in a test case.
  """

  chap1 = ChapterExample('Chapter Example')


class TestChapter(MarkworkTest):
  """
  TestChapter subclasses 'MarkworkTest' and provides tests for the 'Chapter'
  class in the 'worktoy.markwork' package.
  """

  def test_init(self, ) -> None:
    """Tests that a 'Chapter' instance can be initialized without error."""
    chapter = ChapterExample('Chapter Example')
    self.assertIsInstance(chapter, Chapter)

  def test_instance_is_none(self, ) -> None:
    """Tests that a 'Chapter' instance can be accessed when the instance is
    None."""
    chapter = ChapterExample('Chapter Example')
    self.assertIs(chapter.__get__(None, IndexExample), chapter)

  def test_incompatible_components(self) -> None:
    """Tests that an IndexError is raised when a 'Chapter' instance is not
    found in the 'Index' instance."""

    class Foo(IndexExample):
      sus = ChapterExample('Chapter Example')

    blocks = (*((k, v) for k, v in Foo.__blocks_dict__.items()),)
    newBlocks = dict()
    for k, v in blocks:
      if k != 'sus':
        newBlocks[k] = v
    setattr(Foo, '__blocks_dict__', newBlocks)
    setattr(Foo, '__blocks_tuple__', (*(v for _, v in newBlocks.items()),))

    with self.assertRaises(IndexError):
      _ = Foo().sus
    with self.assertRaises(IndexError):
      _ = ChapterExample.__get__(Foo.sus, Foo(), Foo)

  def test_length(self) -> None:
    """Tests that a 'Chapter' instance has the correct length."""
    chapter = ChapterExample('Chapter Example')
    self.assertEqual(len(chapter), 1)
