"""
Chapter subclasses 'Section' and provides the next level content
container. Besides this semantic difference, it remains identical to
'Section'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import maybe, textFmt
from ..desc import AttriBox, Field
from . import HeaderNum, ChapterStyle, Section

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Type, Any, Self, Iterator

  from . import Index

  TupleInt: TypeAlias = tuple[int, ...]
  MaybeTupleInt: TypeAlias = Optional[TupleInt]
  TupleIntField: TypeAlias = Union[TupleInt, Field]

  IndexType: TypeAlias = Type[Index]

  StyleBox: TypeAlias = Union[ChapterStyle, AttriBox]


class Chapter(Section):
  """
  Chapter subclasses 'Section' and provides the next level content
  container. Besides this semantic difference, it remains identical to
  'Section'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __header_level__: HeaderNum = HeaderNum.CHAPTER

  #  Fallback Variables
  __fallback_prefix__: TupleInt = (1,)

  #  Private Variables

  #  Public Variables
  headerStyle: StyleBox = AttriBox[ChapterStyle]()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, index: Index, indexType: IndexType, **kwargs) -> Self:
    if index is None:
      return self
    i = 0
    for i, chapter in enumerate(indexType.getBlocksTuple()):
      if chapter is self:
        break
    else:
      infoSpec = """'%s' object not found in '%s' object."""
      info = infoSpec % (type(self).__name__, indexType.__name__)
      raise IndexError(textFmt(info))
    self.__prefix_numbers__ = i + 1,
    return self

  def __iter__(self, ) -> Iterator[Section]:
    sections = self.getBlocksTuple()
    for section in sections:
      yield section.__get__(self, type(self))

  def __len__(self, ) -> int:
    return len((*self.getBlocksTuple(),))
