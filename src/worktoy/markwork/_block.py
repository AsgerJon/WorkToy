"""
Block subclasses 'BaseObject' and provides content types. Every type of
content should be a subclass of 'Block'. This is the 'smallest' object
that can be referenced.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

from ..dispatch import overload
from ..utilities import maybe, textFmt
from ..desc import Field, AttriBox
from ..mcls import BaseObject
from . import Style, InlineText, MetaBlock, InlineBase

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Type, Self, Callable

  StrField: TypeAlias = Union[Field, str]
  MaybeStr: TypeAlias = Optional[str]

  InlineDict: TypeAlias = dict[str, InlineText]
  MaybeInlineDict: TypeAlias = Optional[InlineDict]

  InlineTuple: TypeAlias = tuple[InlineText, ...]
  MaybeInlineTuple: TypeAlias = Optional[InlineTuple]
  InlineTupleField: TypeAlias = Union[InlineTuple, Field]

  BlocksTuple: TypeAlias = tuple[Self, ...]
  MaybeBlocksTuple: TypeAlias = Optional[BlocksTuple]
  BlocksTupleField: TypeAlias = Union[BlocksTuple, Field]

  BlocksDict: TypeAlias = dict[str, Self]
  MaybeBlocksDict: TypeAlias = Optional[BlocksDict]

  StyleBox: TypeAlias = Union[Style, AttriBox]

  BlockType: TypeAlias = Type[Self]
  InlinesTuple: TypeAlias = tuple[InlineText, ...]
  InlinesDict: TypeAlias = dict[str, InlineText]

  GetBlocksTuple: TypeAlias = Callable[[Self], BlocksTuple]
  GetBlocksDict: TypeAlias = Callable[[Self], BlocksDict]


class Block(BaseObject, metaclass=MetaBlock):
  """
  Block subclasses 'BaseObject' and provides content types. Every type of
  content should be a subclass of 'Block'.
  """

  getBlocksTuple: Callable[[], BlocksTuple]
  getBlocksDict: Callable[[], BlocksDict]
  getInlinesTuple: Callable[[], InlinesTuple]
  getInlinesDict: Callable[[], InlinesDict]
  getInlines: Callable[[], InlinesTuple]

  __inline_components__: MaybeInlineTuple
  __inline_dict__: MaybeInlineDict
  __block_components__: MaybeBlocksTuple
  __block_dict__: MaybeBlocksDict

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __is_block__: bool = True

  #  Fallback Variables

  #  Private Variables
  __block_title__: MaybeStr = None

  #  Public Variables
  title: StrField = Field()
  inlines: InlineTupleField = Field()
  blocks: BlocksTupleField = Field()

  #  Virtual Variables
  refId: StrField = Field()
  anchor: StrField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @inlines.GET
  def getInlines(self, ) -> InlineTuple:
    """
    Getter-function for the inline components of this block.
    """
    out = []
    for inline in self.getInlinesTuple():
      out.append(inline.__get__(self, type(self)))
    return (*out,)

  @blocks.GET
  def _getBlocks(self, ) -> BlocksTuple:
    out = []
    for block in self.getBlocksTuple():
      out.append(block.__get__(self, type(self)))
    return (*out,)

  @refId.GET
  def _getRefId(self, ) -> str:
    """
    Returns the reference ID of the block. This is used to reference the
    block in other components.
    """
    owner = self.getFieldOwner()
    if owner is None:
      infoSpec = """%s_%s"""
      clsName = type(self).__name__
      idStr = '%d' % randint(0, 2 ** 64 - 1)
      return textFmt(infoSpec % (clsName, idStr))
    else:
      infoSpec = """%s.%s"""
      fieldName = self.getFieldName()
      return textFmt(infoSpec % (owner.__name__, fieldName))

  @anchor.GET
  def _getAnchor(self, ) -> str:
    infoSpec = """<span id="%s"></span>"""
    return infoSpec % self.refId

  @title.GET
  def _getTitle(self, ) -> str:
    return maybe(self.__block_title__, type(self).__name__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def registerInline(cls, inline: InlineBase, name: str) -> None:
    """
    Subclasses that need to customize registration of inline components
    should override this method. By default, it is a no-op, leaving
    registration to the metaclass system.
    """

  @classmethod
  def registerBlock(cls, block: Block, name: str) -> None:
    """
    Subclasses that need to customize registration of block components
    should override this method. By default, it is a no-op, leaving
    registration to the metaclass system.
    """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, blockType: Type[Block], name: str, ) -> None:
    super().__set_name__(blockType, name)
    blockType.registerBlock(self, name, )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(str)
  def __init__(self, title: str, ) -> None:
    self.__block_title__ = title

  @overload()
  def __init__(self, ) -> None:
    pass

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  OPTIONAL METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  REQUIRED METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PUBLIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
