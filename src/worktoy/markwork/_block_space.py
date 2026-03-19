"""
BlockSpace subclasses 'BaseSpace' and provides the namespace class for the
'MetaBlock' metaclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import maybe
from ..mcls import BaseSpace
from . import InlineBase, InlineHook, BlockHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Type

  from . import Block, MetaBlock

  Meta: TypeAlias = Type[MetaBlock]

  BlockDict: TypeAlias = dict[str, Block]
  MaybeBlockDict: TypeAlias = Optional[BlockDict]
  BlockTuple: TypeAlias = tuple[Block, ...]
  MaybeBlockTuple: TypeAlias = Optional[BlockTuple]

  InlineTuple: TypeAlias = tuple[InlineBase, ...]
  MaybeInlineTuple: TypeAlias = Optional[InlineTuple]
  InlineDict: TypeAlias = dict[str, InlineBase]
  MaybeInlineDict: TypeAlias = Optional[InlineDict]

  Bases: TypeAlias = tuple[type, ...]


class BlockSpace(BaseSpace):
  """
  BlockSpace subclasses 'BaseSpace' and provides the namespace class for
  the 'MetaBlock' metaclass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __blocks_tuple__: MaybeBlockTuple = None
  __blocks_dict__: MaybeBlockDict = None
  __inlines_tuple__: MaybeInlineTuple = None
  __inlines_dict__: MaybeInlineDict = None

  #  Public Variables
  inlineHook = InlineHook()
  blockHook = BlockHook()

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getBlocksDict(self, ) -> BlockDict:
    """
    Getter-function for the block component dictionary.
    """
    return maybe(self.__blocks_dict__, dict())

  def getBlocksTuple(self, ) -> BlockTuple:
    """
    Getter-function for the block component tuple.
    """
    return maybe(self.__blocks_tuple__, ())

  def getInlinesDict(self, ) -> InlineDict:
    """
    Getter-function for the inline component dictionary.
    """
    return maybe(self.__inlines_dict__, dict())

  def getInlinesTuple(self, ) -> InlineTuple:
    """
    Getter-function for the inline component tuple.
    """
    return maybe(self.__inlines_tuple__, ())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addBlock(self, name: str, block: Block) -> None:
    """
    Adds a block component to the block component dictionary.
    """
    existingDict = self.getBlocksDict()
    existingDict[name] = block
    self.__blocks_dict__ = existingDict
    existingTuple = self.getBlocksTuple()
    self.__blocks_tuple__ = (*existingTuple, block)

  def addInline(self, name: str, inline: InlineBase) -> None:
    """
    Adds an inline component to the inline component dictionary.
    """
    existingDict = self.getInlinesDict()
    existingDict[name] = inline
    self.__inlines_dict__ = existingDict
    existingTuple = self.getInlinesTuple()
    self.__inlines_tuple__ = (*existingTuple, inline)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: Meta, name: str, bases: Bases, **kw, ) -> None:
    super().__init__(mcls, name, bases, **kw)
    self.__blocks_tuple__ = ()
    self.__blocks_dict__ = dict()
    self.__inlines_tuple__ = ()
    self.__inlines_dict__ = dict()
    for base in bases:
      if isinstance(base, mcls):
        for name_, block in base.getBlocksDict().items():
          self.addBlock(name_, block)
        for name_, inline in base.getInlinesDict().items():
          self.addInline(name_, inline)
