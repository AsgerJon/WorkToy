"""
Clause assembles a sequence of words.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.sentinels import THIS
from ..dispatch import overload
from ..desc import Field, AttriBox
from ..utilities import textFmt
from . import StochasticWord, BaseGenerator

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Optional, Self, Iterator

  IntList: TypeAlias = list[int]
  StrList: TypeAlias = list[str]

  MaybeIntList: TypeAlias = Optional[IntList]
  MaybeStrList: TypeAlias = Optional[StrList]

  Words: TypeAlias = tuple[str, ...]


class Clause(BaseGenerator):
  """
  A clause is the smallest text a layout asks for: words joined by single
  spaces, exactly as many characters as requested, with no punctuation of
  its own, since the sentence around it puts the commas and the period
  and capitalizes its first word. A first clause opens with 'Lorem
  ipsum', and one too short to hold the lead-in and a word still has to
  come out at its count, as a placeholder. A project must be able to
  bring its own words by rebinding 'stochWord' to a box of its own
  'StochasticWord' subclass, and its own lead-in by rebinding
  '__lead_in__'.

  Implementation
  --------------

  'wordsLengths' and 'wordsArray' are 'Field's built on first read and
  cached until 'clear'. The lengths come from 'stochWord.partitionSpaced'
  over the count plus one, less the lead-in words and their separators,
  so the words joined by single spaces meet the count; a clause that is
  not first refuses a count below the shortest word with 'ValueError',
  and a count no run of the words adds up to is refused the same way. A
  first clause too short for the lead-in, a space and one word of its
  list takes its words from '_placeholderWords': as much of the lead-in
  as fits ahead of three dots, and dots for the rest ('Lorem ipsum....'
  at fifteen). 'capitalizeLead' and 'terminate' change the cached
  words in place for the sentence. 'reset' clears and rebuilds, 'realize'
  and 'str' render, 'len' measures the text, and iteration yields the
  words. The copy constructor, '@overload(THIS)', copies the count, the
  flag and the caches.

  Attributes
  ----------
  stochWord : AttriBox[StochasticWord]
    The word list, one per instance, built on first read.
  wordsLengths : Field[IntList]
    The cached word lengths, a 'list[int]'.
  wordsArray : Field[StrList]
    The cached words, a 'list[str]'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  #  When a Clause is constructed via 'Clause.first(...)', these words
  #  are pinned to the leading positions and their character lengths
  #  override the sampled lengths at those indices.
  __lead_in__: Words = ('Lorem', 'ipsum')

  #  Private Variables
  __words_lengths__: MaybeIntList = None
  __words_array__: MaybeStrList = None

  #  Public Variables
  stochWord = AttriBox[StochasticWord]()
  wordsLengths: Field[IntList] = Field()
  wordsArray: Field[StrList] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _isShortFirst(self, ) -> bool:
    """
    The '_isShortFirst' method says whether this is a first clause too
    short to hold its lead-in, a space and one word of its list, and so
    renders the placeholder instead of words.
    """
    if not self.isFirst:
      return False
    lead = ' '.join(self.__lead_in__)
    threshold = len(lead) + 1 + self.stochWord.minVal
    return True if self.charCount < threshold else False

  def _placeholderWords(self, ) -> StrList:
    """
    The '_placeholderWords' method builds the placeholder of a short first
    clause, exactly 'charCount' characters: as much of the lead-in as fits
    ahead of three dots, and dots for the rest. The text is split on
    spaces so the surrounding 'Sentence' can still capitalize the first
    word and terminate the last.

    Returns
    -------
    StrList
      The placeholder words, a 'list[str]' that joins on single spaces to
      exactly 'charCount' characters.
    """
    lead = ' '.join(self.__lead_in__)
    n = self.charCount
    visible = lead[:max(0, n - 3)]
    text = visible + '.' * (n - len(visible))
    return [*text.split(' '), ]

  def _buildWordsLengths(self, ) -> None:
    """
    The '_buildWordsLengths' method partitions 'charCount' into word
    lengths drawn from 'stochWord' and caches them. When 'isFirst' is set,
    the leading slots are pinned to the character lengths of '__lead_in__'
    so 'Lorem ipsum' (or whatever the subclass configures) fits exactly,
    and only the remaining words are sampled. A first clause too short for
    the lead-in and one word falls back to the placeholder, whose lengths
    are read back from the realized words.

    Raises
    ------
    ValueError
      If this clause is not a first clause and 'charCount' falls below
      the shortest word that 'stochWord' can realize, or if no run of
      words from the list adds up to 'charCount'.
    """
    if self._isShortFirst():
      self.__words_lengths__ = [len(word) for word in self.wordsArray]
      return
    leadIn = self.__lead_in__ if self.isFirst else ()
    if not leadIn:
      shortestWord = self.stochWord.minVal
      if self.charCount < shortestWord:
        infoSpec = """A 'Clause' that is not a first clause cannot
        realize fewer than %d characters, but received a character
        count of %d!"""
        info = infoSpec % (shortestWord, self.charCount)
        raise ValueError(textFmt(info))
    leadLengths = [len(word) for word in leadIn]
    target = self.charCount + 1 - sum(leadLengths) - len(leadLengths)
    rest = self.stochWord.partitionSpaced(target)
    self.__words_lengths__ = [*leadLengths, *rest]

  @wordsLengths.GET
  def _getWordsLengths(self, **kwargs) -> IntList:
    if self.__words_lengths__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildWordsLengths()
      return self._getWordsLengths(_recursion=True)  # pragma: no mutate
    return self.__words_lengths__

  def _buildWordsArray(self, ) -> None:
    """
    The '_buildWordsArray' method realizes each cached length into a
    concrete word and caches the resulting word list. The leading slots are
    taken from '__lead_in__' when 'isFirst' is set. A first clause too short
    to hold the lead-in and one word is filled with the placeholder instead.
    """
    if self._isShortFirst():
      self.__words_array__ = self._placeholderWords()
      return
    leadIn = self.__lead_in__ if self.isFirst else ()
    words = []
    for i, length in enumerate(self.wordsLengths):
      if i < len(leadIn):
        words.append(leadIn[i])
        continue
      words.append(self.stochWord.realizeLength(length))
    self.__words_array__ = [*words, ]

  @wordsArray.GET
  def _getWordsArray(self, **kwargs) -> StrList:
    if self.__words_array__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildWordsArray()
      return self._getWordsArray(_recursion=True)  # pragma: no mutate
    return self.__words_array__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.charCount = other.charCount
    self.isFirst = other.isFirst
    if other.__words_lengths__ is not None:
      self.__words_lengths__ = [*other.__words_lengths__, ]
    if other.__words_array__ is not None:
      self.__words_array__ = [*other.__words_array__, ]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def clear(self, ) -> None:
    """
    The 'clear' method drops the cached length and word arrays.
    """
    self.__words_lengths__ = None
    self.__words_array__ = None

  def reset(self, ) -> None:
    """
    The 'reset' method clears and regenerates the cached length and word
    arrays.
    """
    self.clear()
    self._buildWordsLengths()
    self._buildWordsArray()

  def capitalizeLead(self) -> None:
    """
    The 'capitalizeLead' method capitalizes the first word of this clause
    in place.
    """
    words = self.wordsArray
    words[0] = str.capitalize(words[0])

  def terminate(self, punctuation: str) -> None:
    """
    The 'terminate' method appends the given punctuation to the last word
    of this clause.

    Parameters
    ----------
    punctuation : str
      The punctuation appended to the clause's last word.
    """
    words = self.wordsArray
    words[-1] = """%s%s""" % (words[-1], punctuation)

  def realize(self) -> str:
    """
    The 'realize' method returns the realized text for this clause.

    Returns
    -------
    str
      The clause rendered as text.
    """
    return str(self)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self, ) -> str:
    return textFmt(str.join(' ', self.wordsArray))

  def __repr__(self, ) -> str:
    return str.join(' ', self.wordsArray)

  def __len__(self, ) -> int:
    return len(str(self))

  def __iter__(self, ) -> Iterator[str]:
    yield from self.wordsArray
