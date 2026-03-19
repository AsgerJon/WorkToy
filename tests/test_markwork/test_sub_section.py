"""
TestSubSection subclasses 'MarkworkTest' and provides tests for the
'SubSection' class in the 'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import SubSection, InlineLorem, InlineLink
from worktoy.markwork import Badge, Index, Block
from worktoy.utilities import ExceptionInfo
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
  i3 = InlineLink(
    """https:/youtube.com/watch?v=dQw4w9WgXcQ""",
    """Educational Content, fr fr, trust me bro!""",
    """Rick Astley - Never Gonna Give You Up (Video)""",
    )
  i4 = Badge(
    """https://i.imgflip.com/2/10998c.jpg""",
    """Risitas Meme""",
    )
  i5 = InlineLorem()
  i6 = InlineLorem()


class IndexExample(Index):
  """
  IndexExample subclasses 'Index' and provides an example of how one might
  use 'Index' in a test case.
  """

  sub1 = SubSectionExample('SubSection Example')


class TestSubSection(MarkworkTest):
  """
  TestSubSection subclasses 'MarkworkTest' and provides tests for the
  'SubSection' class in the 'worktoy.markwork' package.
  """

  def test_init(self, ) -> None:
    """Tests that a 'SubSection' instance can be initialized without
    error."""
    subSectionExample = SubSectionExample('Test SubSection')
    self.assertIsInstance(subSectionExample, SubSection)

  def test_index(self, ) -> None:
    """Tests that a 'SubSection' instance can be indexed without error."""
    indexExample = IndexExample()
    self.assertIsInstance(indexExample, Index)
    indexStr = indexExample.markdown()
    self.assertIsInstance(indexStr, str)

  def test_instance_is_none(self, ) -> None:
    """
    Tests the branch where the 'SubSection' is accessed through the owning
    class rather than through an instance.
    """
    subSectionExample = IndexExample.sub1
    self.assertIsInstance(subSectionExample, SubSection)

  def test_incompatible_components(self) -> None:
    """Tests that the branch where a 'SubSection' instance is not
    registered on the supposedly owning class.  """

    class Foo(IndexExample):
      sus = SubSectionExample('Sus SubSection')

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
      _ = SubSectionExample.__get__(Foo.sus, Foo(), Foo)

  def test_iterability(self, ) -> None:
    """Tests that a 'SubSection' instance is iterable."""

    class Bar(Block):
      i1 = InlineLorem(40)
      i2 = InlineLorem(40)
      i3 = InlineLorem(40)

    class Foo(SubSection):
      bar1 = Bar()
      bar2 = Bar()
      bar3 = Bar()

    for bar in Foo():
      self.assertIsInstance(bar, Bar)

  def test_length(self) -> None:
    """Tests that a 'SubSection' instance has a length equal to the number of
    blocks it contains."""

    class Bar(Block):
      i1 = InlineLorem(40)
      i2 = InlineLorem(40)
      i3 = InlineLorem(40)

    class Foo(SubSection):
      bar1 = Bar()
      bar2 = Bar()
      bar3 = Bar()

    foo = Foo()
    self.assertEqual(len(foo), 3)
