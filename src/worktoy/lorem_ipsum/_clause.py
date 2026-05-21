"""
Clause subclasses 'BaseGenerator' and implements word sequences.
"""
#  AGPL-3.0 license
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
  Clause implements word sequences.
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

  #  Fallback Variables
  __fallback_count__: int = 40

  #  Private Variables
  __words_lengths__: MaybeIntList = None
  __words_array__: MaybeStrList = None

  #  Public Variables
  stochWord: AttriBox[StochasticWord] = AttriBox[StochasticWord]()
  wordsLengths: Field[IntList] = Field()
  wordsArray: Field[StrList] = Field()

  #  Virtual Variables
  wordCount: Field[int] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @wordCount.GET
  def _getWordCount(self, ) -> int:
    return int(round(self.charCount / self.stochWord.meanLen))

  def _buildWordsLengths(self, ) -> None:
    """Sample a log-normal word-length sequence summing to 'charCount'
    and cache it. When 'isFirst' is set, the leading slots are pinned
    to the character lengths of '__lead_in__' so 'Lorem ipsum' (or
    whatever the subclass configures) fits exactly."""
    mean, var = self.stochWord.meanLen, self.stochWord.varianceLen
    minVal, maxVal = self.stochWord.minLen, self.stochWord.maxLen
    lengths = [self.logNormal(mean, var) for _ in range(self.wordCount)]
    factor = self.charCount / sum(lengths)
    lengths = [int(round(length * factor)) for length in lengths]
    lengths = [max([minVal, l]) for l in lengths]
    lengths = [min([maxVal, l]) for l in lengths]
    leadIn = self.__lead_in__ if self.isFirst else ()
    for i, word in enumerate(leadIn):
      lengths[i] = len(word)
    targetSum = self.charCount - self.wordCount + 1
    minIndex = len(leadIn)
    self.__words_lengths__ = self.scaleSum(
      lengths,
      targetSum,
      minVal,
      maxVal,
      minIndex,
    )

  @wordsLengths.GET
  def _getWordsLengths(self, **kwargs) -> IntList:
    if self.__words_lengths__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildWordsLengths()
      return self._getWordsLengths(_recursion=True)
    return self.__words_lengths__

  def _buildWordsArray(self, ) -> None:
    """Realize each cached length into a concrete word and cache the
    resulting word list. The leading slots are taken from
    '__lead_in__' when 'isFirst' is set."""
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
    """Drop the cached length and word arrays."""
    self.__words_lengths__ = None
    self.__words_array__ = None

  def reset(self, ) -> None:
    """Clear and regenerate the cached length and word arrays."""
    self.clear()
    self._buildWordsLengths()
    self._buildWordsArray()

  def capitalizeLead(self) -> None:
    """Capitalize the first word of this clause in place."""
    words = self.wordsArray
    words[0] = str.capitalize(words[0])

  def terminate(self, punctuation: str) -> None:
    """Append the given punctuation to the last word of this clause."""
    words = self.wordsArray
    words[-1] = """%s%s""" % (words[-1], punctuation)

  def realize(self) -> str:
    """Return the realized text for this clause."""
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
