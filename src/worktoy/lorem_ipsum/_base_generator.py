"""
BaseGenerator is the shared base for the 'lorem_ipsum' text generators.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import typeCast, textFmt
from ..dispatch import overload
from ..desc import AttriBox
from ..mcls import BaseObject
from ..waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Self, Any


class BaseGenerator(BaseObject):
  """
  The three text generators, a clause of words, a sentence of clauses and
  a paragraph of sentences, share one contract: a target character count
  given to the constructor or assigned later, a flag saying whether the
  text opens with 'Lorem ipsum', a layout made on first use and kept
  until the count or the flag changes, and a placeholder for a count too
  small to lay out. A project must be able to write 'Clause(30)',
  'Clause(charCount=30)' or 'Clause.first(30)' alike, be refused a
  negative count where it gives it, and get a text of exactly the count
  it asked for.

  Implementation
  --------------

  'charCount' is an 'AttriBox[int]' of 40; its 'preSet' callback refuses
  a negative value with 'ValueError' and leaves a value the box cannot
  cast to the box, and its 'onSet' callback calls 'clear'. 'isFirst' is
  an 'AttriBox[bool]' of 'False', set by the 'first' classmethod, and its
  'onSet' callback calls 'clear' as well. Three '@overload's of
  '__init__' take the count by position, as a keyword, or as 'None' by
  position, which keeps the default as 'charCount=None' does; any other
  keyword fails with Python's own 'TypeError'. 'clear' is empty here
  and replaced by
  each subclass. '_shortText' gives the 'Lorem Ipsum...' placeholder of
  exactly the count, which a subclass returns below '__truncate_below__'.

  Attributes
  ----------
  charCount : AttriBox[int]
    The target character count, 40 unless given.
  isFirst : AttriBox[bool]
    Whether the text opens with the lead-in, 'False' unless given.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  #  A 'charCount' below '__truncate_below__' is too small for the generator
  #  to lay out its content, so it degrades to a 'Lorem Ipsum...' placeholder
  #  of exactly that length.
  __truncate_below__: int = 15

  #  Public Variables
  charCount = AttriBox[int](40)
  isFirst = AttriBox[bool](False)

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

  @isFirst.onSet
  def _onSetIsFirst(self, ) -> None:
    """
    The '_onSetIsFirst' callback drops the cached layout whenever 'isFirst'
    is assigned, since that layout was made with or without the lead-in.
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
    content: as much of 'Lorem Ipsum' as fits ahead of three dots, and dots
    alone below four characters. Past the whole lead the dots make up the
    count, so a subclass may render the placeholder up to any
    '__truncate_below__' it sets.

    Returns
    -------
    str
      The placeholder text, exactly 'charCount' characters long.
    """
    n = self.charCount
    visible = 'Lorem Ipsum'[:max(0, n - 3)]
    return visible + '.' * (n - len(visible))

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

  @overload(type(None))
  def __init__(self, charCount: None) -> None:
    """A count of 'None' keeps the default, as 'charCount=None' does."""

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
    self.isFirst = True
    return self
