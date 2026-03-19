"""
Section subclasses 'SubSection' and provides the next level content
container. Besides this semantic difference, it remains identical to
'SubSection'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..desc import AttriBox
from . import SubSection, HeaderNum, SectionStyle
from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Type, Self, Iterator

  from . import Chapter

  TupleInt: TypeAlias = tuple[int, ...]

  ChapterType: TypeAlias = Type[Chapter]
  StyleBox: TypeAlias = Union[SectionStyle, AttriBox]


class Section(SubSection):
  """
  Section subclasses 'SubSection' and provides the next level content
  container. Besides this semantic difference, it remains identical to
  'SubSection'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __header_level__: HeaderNum = HeaderNum.SECTION

  #  Fallback Variables
  __fallback_prefix__: TupleInt = (1, 1,)

  #  Public Variables
  headerStyle: StyleBox = AttriBox[SectionStyle]()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, chapter: Chapter, owner: ChapterType, **kwargs) -> Self:
    if chapter is None:
      return self
    for i, section in enumerate(chapter.getBlocksTuple()):
      if section is self:
        break
    else:
      infoSpec = """'%s' object not found in '%s' object."""
      info = infoSpec % (type(self).__name__, owner.__name__)
      raise IndexError(textFmt(info))
    self.__prefix_numbers__ = (*chapter.prefix, i + 1,)
    return self

  def __iter__(self, ) -> Iterator[SubSection]:
    subSections = self.getBlocksTuple()
    for subSection in subSections:
      yield subSection.__get__(self, type(self))

  def __len__(self, ) -> int:
    return len((*self.getBlocksTuple(),))
