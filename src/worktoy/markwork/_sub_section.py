"""
SubSection subclasses 'Paragraph' and provides the lowest content
container level.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import maybe
from ..desc import AttriBox, Field
from . import HeaderNum, ParagraphBlock, Style, SubSectionStyle, InlineText
from . import Block

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Self, Iterator

  from . import Section

  StyleBox: TypeAlias = Union[AttriBox, Style]
  StrField: TypeAlias = Union[Field, str]
  MaybeStr: TypeAlias = Optional[str]

  TupleInt: TypeAlias = tuple[int, ...]
  MaybeTupleInt: TypeAlias = Optional[TupleInt]
  TupleIntField: TypeAlias = Union[TupleInt, Field]

  InlineTuple: TypeAlias = tuple[InlineText, ...]
  MaybeInlineTuple: TypeAlias = Optional[InlineTuple]

  SectionType: TypeAlias = type[Section]


class SubSection(ParagraphBlock):
  """
  SubSection subclasses 'Paragraph' and provides the lowest content
  container level.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __header_level__: HeaderNum = HeaderNum.SUBSECTION

  #  Fallback Variables
  __fallback_prefix__: TupleInt = (1, 1, 1)

  #  Private Variables
  __inline_texts__: MaybeInlineTuple = None
  __prefix_numbers__: MaybeTupleInt = None
  __anchor_cache__: MaybeStr = None

  #  Public Variables
  headerStyle: StyleBox = AttriBox[SubSectionStyle]()
  prefix: TupleIntField = Field()

  #  Virtual Variables
  header: StrField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @prefix.GET
  def _getPrefix(self, ) -> TupleInt:
    return maybe(self.__prefix_numbers__, self.__fallback_prefix__)

  @header.GET
  def _getHeader(self, ) -> str:
    infoSpec = """%s:  %s"""
    prefixStr = str.join('.', [str(pre) for pre in self.prefix])
    info = infoSpec % (prefixStr, self.title)
    return self.headerStyle.apply(info)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NESTED CLASSES   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PUBLIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def markdown(self, ) -> str:
    """
    This method expands upon the 'Paragraph.markdown' method with header
    and anchor. The header is styled with the 'headerStyle' variable.

    Returns
    -------
    str
      The Markdown representation of the subsection.

    Examples
    --------
    >>> from worktoy.markwork import SubSection, InlineText
    >>> class Roll(SubSection):
    ...   i1 = InlineText('Never gonna give you up')
    ...   i2 = InlineText('Never gonna let you down')
    ...   i3 = InlineText('Never gonna run around and desert you')
    >>> print(Roll().markdown())
    <a name="X.Y.Z  Roll"></a>
    <h3>X.Y.Z  Roll</h3>
    Never gonna give you up Never gonna let you down Never gonna run (->)
    around and desert you
    """
    anchorLine = str(self.anchor)
    inlines = super().markdown()
    blockInlines = []
    for block in self:
      blockInlines.append(block.markdown())
    lines = [anchorLine, self.header, inlines, *blockInlines]
    return str.join('\n\n', lines)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, section: Section, owner: SectionType, **kwargs) -> Self:
    if section is None:
      return self
    for i, subSection in enumerate(section.getBlocksTuple()):
      if subSection is self:
        break
    else:
      infoSpec = """'%s' object not found in '%s' object."""
      info = infoSpec % (type(self).__name__, owner.__name__)
      raise IndexError(info)
    self.__prefix_numbers__ = (*section.prefix, i + 1,)
    return self

  def __iter__(self, ) -> Iterator[Block]:
    blocks = self.getBlocksTuple()
    for block in blocks:
      yield block.__get__(self, type(self))

  def __len__(self, ) -> int:
    return len((*self.getBlocksTuple(),))
