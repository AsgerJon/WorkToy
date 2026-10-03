"""
BaseGenerator is the shared base for the 'lorem_ipsum' text generators.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import maybe, typeCast, textFmt
from ..dispatch import overload
from ..desc import AttriBox, Field
from ..mcls import BaseObject
from ..waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Self, Any

  MaybeBool: TypeAlias = Optional[bool]


class BaseGenerator(BaseObject):
  """
  BaseGenerator is the shared base for the 'lorem_ipsum' generators
  'Clause', 'Sentence', and 'Paragraph'. It holds the target 'charCount',
  the 'isFirst' flag with its 'first' constructor, and the short-text
  placeholder a generator falls back to when 'charCount' is too small to
  lay out real content.

  The target is given by position or as the 'charCount' keyword, as in
  'Clause(30)' or 'Clause(charCount=30)', and a generator built without it
  takes the default of the 'charCount' box. Any other keyword raises the
  'TypeError' Python raises for an unexpected keyword argument, and a
  negative target raises 'ValueError', whether given to the constructor
  or assigned later.

  A generator lays out its content on first use and caches the layout.
  Assigning 'charCount' calls 'clear', which drops that cache, so the next
  rendering is laid out anew at the new count.
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
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @charCount.preSet
  def _preSetCharCount(self, value: Any) -> None:
    """
    The '_preSetCharCount' callback refuses a negative 'charCount' with
    'ValueError', since no text has fewer than no characters. The value is
    read as the 'int' the box casts it to, and a value the box cannot cast
    is left for the box to refuse.
    """
    try:
      count = typeCast(int, value)
    except TypeCastException:
      return
    if count < 0:
      infoSpec = """A '%s' needs a character count of zero or more, but
      received: %d"""
      info = infoSpec % (type(self).__name__, count)
      raise ValueError(textFmt(info))

  @charCount.onSet
  def _onSetCharCount(self, ) -> None:
    """
    The '_onSetCharCount' callback drops the cached layout whenever
    'charCount' is assigned, since that layout was made for the old count.
    """
    self.clear()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def clear(self, ) -> None:
    """
    The 'clear' method drops the layout a generator caches. The base
    caches none, and each subclass replaces this with one dropping its
    own caches.
    """

  def _shortText(self, ) -> str:
    """
    The '_shortText' method returns a 'Lorem Ipsum...' placeholder of
    exactly 'charCount' characters for a generator too small to lay out its
    content: the leading dots alone below four characters, otherwise as
    much of 'Lorem Ipsum' as fits ahead of a trailing ellipsis. A subclass
    returns this for a 'charCount' below '__truncate_below__'.

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
  def __init__(self, *, charCount: int = None) -> None:
    if charCount is not None:
      self.charCount = charCount

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
