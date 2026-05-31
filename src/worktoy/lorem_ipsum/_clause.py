"""
Clause assembles a sequence of words.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.dispatch import overload
from worktoy.desc import Field, AttriBox
from . import StochasticWord, BaseGenerator
from worktoy.utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Self, Iterator

  IntList: TypeAlias = list[int]
  StrList: TypeAlias = list[str]

  MaybeIntList: TypeAlias = Optional[IntList]
  MaybeStrList: TypeAlias = Optional[StrList]

  Words: TypeAlias = tuple[str, ...]


class Clause(BaseGenerator):
  """
  Clause assembles a flat sequence of words summing to a target character
  count. It samples word lengths from a 'StochasticWord', realizes each
  length into a concrete word, and caches both arrays lazily.

  When built via 'Clause.first(...)', the leading positions are pinned to
  '__lead_in__' ('Lorem ipsum'), and a first clause too short to hold the
  lead-in degrades to a 'Lorem ipsum ...' placeholder of exactly the
  requested length. The surrounding 'Sentence' drives capitalization and
  terminating punctuation through 'capitalizeLead' and 'terminate'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  #  When a Clause is constructed via 'Clause.first(...)', these words
  #  are pinned to the leading positions and their character lengths
  #  override the sampled lengths at those indices.
  __lead_in__: Words = ('Lorem', 'ipsum')
  __length_var__: int = 15

  #  A first clause shorter than '__dotted_below__' characters is rendered
  #  as a 'Lorem ipsum ...' placeholder of exactly that length rather than a
  #  real word sequence: the lead-in, a partial word filling the gap, then a
  #  trailing ellipsis.
  __dotted_below__: int = 24

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

  def _placeholderWords(self, ) -> StrList:
    """
    The '_placeholderWords' method builds a 'Lorem ipsum ...' placeholder
    of exactly 'charCount' characters for a first clause shorter than
    '__dotted_below__'. The lead-in is followed by a space and a gap word
    filling the room before the trailing ellipsis: an 'etc' prefix when one
    to three characters remain, a real word once four or more fit. Below the
    lead-in's own length the lead-in itself is truncated. The text is split
    on spaces so the surrounding 'Sentence' can still capitalize the first
    word and terminate the last.

    Returns
    -------
    StrList
      The placeholder words, a 'list[str]' that joins on single spaces to
      exactly 'charCount' characters.
    """
    lead = ' '.join(self.__lead_in__)
    n = self.charCount
    if n <= len(lead) + 3:
      visible = lead[:max(0, n - 3)]
      text = visible + '.' * (n - len(visible))
    else:
      fillerLen = n - len(lead) - 4
      if fillerLen <= 0:
        filler = ''
      elif fillerLen <= 3:
        filler = 'etc'[:fillerLen]
      else:
        filler = self.stochWord.realizeLength(fillerLen)
      text = lead + ' ' + filler + '...'
    return [*text.split(' '), ]

  def _buildWordsLengths(self, ) -> None:
    """
    The '_buildWordsLengths' method partitions 'charCount' into word
    lengths drawn from 'stochWord' and caches them. When 'isFirst' is set,
    the leading slots
    are pinned to the character lengths of '__lead_in__' so 'Lorem ipsum'
    (or whatever the subclass configures) fits exactly, and only the
    remaining words are sampled. A first clause shorter than
    '__dotted_below__' falls back to a placeholder, whose lengths are read
    back from the realized words.
    """
    leadIn = self.__lead_in__ if self.isFirst else ()
    if leadIn and self.charCount < self.__dotted_below__:
      self.__words_lengths__ = [len(word) for word in self.wordsArray]
      return
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
      return self._getWordsLengths(_recursion=True)
    return self.__words_lengths__

  def _buildWordsArray(self, ) -> None:
    """
    The '_buildWordsArray' method realizes each cached length into a
    concrete word and caches the resulting word list. The leading slots are
    taken from '__lead_in__'
    when 'isFirst' is set. A first clause too short to hold the lead-in and
    one word is filled with a placeholder instead.
    """
    leadIn = self.__lead_in__ if self.isFirst else ()
    if leadIn and self.charCount < self.__dotted_below__:
      self.__words_array__ = self._placeholderWords()
      return
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
      return self._getWordsArray(_recursion=True)
    return self.__words_array__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(THIS)
  def __init__(self, other: Self, **kwargs) -> None:
    self.charCount = other.charCount
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
