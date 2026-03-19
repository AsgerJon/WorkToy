"""
TestSection subclasses 'MarkworkTest' and provides tests for the 'Section'
class in the 'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import Section, InlineLorem, SubSection, Chapter, Index
from . import MarkworkTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class SubSectionExample(SubSection):
  """
  SubSectionExample subclasses 'SubSection' and provides an example of how
  one might use 'SubSection' in a test case.
  """

  i1 = InlineLorem()
  i2 = InlineLorem()
  i3 = InlineLorem()
  i4 = InlineLorem()
  i5 = InlineLorem()
  i6 = InlineLorem()


class SectionExample(Section):
  """
  SectionExample subclasses 'Section' and provides an example of how one
  might use 'Section' in a test case.
  """

  sub1 = SubSectionExample('Never')
  sub2 = SubSectionExample('gonna')
  sub3 = SubSectionExample('give')
  sub4 = SubSectionExample('you')
  sub5 = SubSectionExample('up')


class ChapterExample(Chapter):
  """
  ChapterExample subclasses 'Chapter' and provides an example of how one
  might use 'Chapter' in a test case.
  """

  sec1 = SectionExample("For so long...")
  i1 = InlineLorem()


class IndexExample(Index):
  """
  IndexExample subclasses 'Index' and provides an example of how one might
  use 'Index' in a test case.
  """

  chap1 = ChapterExample('Chapter One')


class TestSection(MarkworkTest):
  """
  TestSection subclasses 'MarkworkTest' and provides tests for the 'Section'
  class in the 'worktoy.markwork' package.
  """

  def test_init(self, ) -> None:
    """Tests that a 'Section' instance can be initialized without errors."""
    sec = SectionExample('Section Example')
    self.assertIsInstance(sec, SubSection)

  def test_index(self, ) -> None:
    """Tests that a 'Section' instance can be indexed without error."""
    indexExample = IndexExample()
    self.assertIsInstance(indexExample, Index)
    indexStr = indexExample.markdown()
    self.assertIsInstance(indexStr, str)

  def test_instance_is_none(self, ) -> None:
    """
    Tests the branch where the 'Section' is accessed through the owning
    class rather than through an instance.
    """
    sec = ChapterExample.sec1
    self.assertIsInstance(sec, Section)

  def test_incompatible_components(self) -> None:
    """
    Tests that the branch where a 'Section' instance is not registered on the
    supposedly owning class raises an error.
    """

    class Foo(IndexExample):
      sec = SectionExample('Sus Section')

    blocks = (*((k, v) for k, v in Foo.__blocks_dict__.items()),)
    newBlocks = dict()
    for k, v in blocks:
      if k != 'sec':
        newBlocks[k] = v
    setattr(Foo, '__blocks_dict__', newBlocks)
    setattr(Foo, '__blocks_tuple__', (*(v for _, v in newBlocks.items()),))

    with self.assertRaises(IndexError):
      _ = Foo().sec
    with self.assertRaises(IndexError):
      _ = SectionExample.__get__(Foo.sec, Foo(), Foo)

  def test_length(self, ) -> None:
    """Tests that the length of a 'Section' instance is the number of
    'SubSection' components it contains."""
    sec = SectionExample('Section Example')
    self.assertEqual(len(sec), 5)
