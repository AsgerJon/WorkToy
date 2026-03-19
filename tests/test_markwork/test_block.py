"""
TestBlock tests the 'Block' class of the 'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import Block, MetaBlock, InlineText, InlineLorem

from . import MarkworkTest
from .examples import (LoremSubSection,
  LoremSection,
  LoremChapter,
  LoremChapterChild)

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Iterator

  Blocks: TypeAlias = Iterator[Block]


class TestBlock(MarkworkTest):
  """
  TestBlock tests the 'Block' class of the 'worktoy.markwork' package.
  """

  def test_init(self, ) -> None:
    """
    This method tests the instantiation of 'Block' instances. The 'Block'
    class provides the following overloaded constructors:

    @overload(str)
    def __init__(self, title: str, ) -> None: ...


    @overload()
    def __init__(self, ) -> None: ...
    """
    titled = Block('Never gonna give you up', )
    self.assertEqual(titled.title, 'Never gonna give you up')
    self.assertFalse(titled.inlines)
    self.assertFalse(titled.blocks)
    untitled = Block()
    self.assertEqual(untitled.title, 'Block')
    self.assertFalse(untitled.inlines)
    self.assertFalse(untitled.blocks)

  def test_inlines(self, ) -> None:
    """
    This method tests the 'inlines' property of 'Block' instances.
    """
    loremSubSection = LoremSubSection()
    self.assertTrue(loremSubSection.inlines)
    for inline in loremSubSection.inlines:
      self.assertIsInstance(inline, InlineLorem)
    loremSection = LoremSection()
    self.assertTrue(loremSection.inlines)
    for inline in loremSection.inlines:
      self.assertIsInstance(inline, InlineLorem)
    loremChapter = LoremChapter()
    self.assertTrue(loremChapter.inlines)
    for inline in loremChapter.inlines:
      self.assertIsInstance(inline, InlineLorem)
    loremChapterChild = LoremChapterChild()
    self.assertTrue(loremChapterChild.inlines)
    for inline in loremChapterChild.inlines:
      self.assertIsInstance(inline, InlineLorem)

  def test_blocks(self, ) -> None:
    """
    This method tests the 'blocks' property of 'Block' instances.
    """
    loremSection = LoremSection()
    self.assertTrue(loremSection.blocks)
    for block in loremSection.blocks:
      self.assertIsInstance(block, Block)

  def test_ref_id_unbound(self, ) -> None:
    """
    This method tests the 'ref_id' property of 'Block' instances when it is
    unbound.
    """
    loremSubSection = LoremSubSection()
    self.assertIn('LoremSubSection', loremSubSection.refId)
    loremSection = LoremSection()
    self.assertIn('LoremSection', loremSection.refId)
    loremChapter = LoremChapter()
    self.assertIn('LoremChapter', loremChapter.refId)
    loremChapterChild = LoremChapterChild()
    self.assertIn('LoremChapterChild', loremChapterChild.refId)

  def test_ref_id_bound(self, ) -> None:
    """
    This method tests the 'ref_id' property of 'Block' instances when it is
    bound.
    """
    loremSection = LoremSection()
    for block in loremSection.blocks:
      blockName = block.getFieldName()
      blockOwner = block.getFieldOwner().__name__
      expectedRefId = """%s.%s""" % (blockOwner, blockName)
      actualRefId = block.refId
      self.assertEqual(expectedRefId, actualRefId)

  def test_anchor(self, ) -> None:
    """
    This method tests the 'anchor' property of 'Block' instances.
    """
    loremSection = LoremSection()
    for block in loremSection.blocks:
      expectedAnchor = """<span id="%s"></span>""" % block.refId
      actualAnchor = block.anchor
      self.assertEqual(expectedAnchor, actualAnchor)
