"""
BaseGenerator is the shared base for the 'lorem_ipsum' text generators.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import maybe
from ..dispatch import overload
from ..desc import AttriBox, Field
from ..mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Self

  MaybeBool: TypeAlias = Optional[bool]


class BaseGenerator(BaseObject):
  """
  BaseGenerator is the shared base for the 'lorem_ipsum' generators
  'Clause', 'Sentence', and 'Paragraph'. It holds the target 'charCount',
  the 'isFirst' flag with its 'first' constructor, and the short-text
  placeholder a generator falls back to when 'charCount' is too small to
  lay out real content.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  #  A 'charCount' below '__truncate_below__' is too small for the generator
  #  to lay out its content, so it degrades to a 'Lorem Ipsum...' placeholder
  #  of exactly that length.
  __truncate_below__: int = 15

  #  Private Variables
  __is_first__: MaybeBool = None

  #  Public Variables
  charCount = AttriBox[int](40)
  isFirst: Field[bool] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @isFirst.GET
  def _getIsFirst(self, ) -> bool:
    return maybe(self.__is_first__, False)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _shortText(self, ) -> str:
    """
    The '_shortText' method returns a 'Lorem Ipsum...' placeholder of
    exactly 'charCount' characters for a generator too small to lay out its
    content:
    the leading dots alone below four characters, otherwise as much of
    'Lorem Ipsum' as fits ahead of a trailing ellipsis. A subclass returns
    this for a 'charCount' below '__truncate_below__'.

    Returns
    -------
    str
      The placeholder text, exactly 'charCount' characters long.
    """
    n = self.charCount
    if n < 4:
      return '...'[:n]
    return 'Lorem Ipsum'[:n - 3] + '...'

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def __init__(self, charCount: int) -> None:
    self.charCount = charCount

  @overload()
  def __init__(self, **kwargs) -> None:
    pass

  @classmethod
  def first(cls, *args, **kwargs) -> Self:
    """
    The 'first' classmethod constructs an instance guaranteed to begin with
    the words 'Lorem ipsum'.

    Returns
    -------
    Self
      A new instance with its first-word flag set.
    """
    self = cls(*args, **kwargs)
    self.__is_first__ = True
    return self
