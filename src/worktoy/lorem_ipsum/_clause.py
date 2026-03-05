"""
Clause subclasses 'BaseGenerator' and implements word sequences.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import gauss, randint
from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.dispatch import overload
from worktoy.desc import Field, AttriBox
from . import StochasticWord, BaseGenerator
from worktoy.utilities import textFmt, maybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Self, Iterator

  MaybeBool: TypeAlias = Optional[bool]

  BoolField: TypeAlias = Union[bool, Field]
  IntField: TypeAlias = Union[int, Field]
  StrField: TypeAlias = Union[str, Field]

  IntList: TypeAlias = list[int]
  StrList: TypeAlias = list[str]

  MaybeIntList: TypeAlias = Optional[IntList]
  MaybeStrList: TypeAlias = Optional[StrList]

  IntListField: TypeAlias = Union[IntList, Field]
  StrListField: TypeAlias = Union[StrList, Field]

  StochWordBox: TypeAlias = Union[StochasticWord, AttriBox]


class Clause(BaseGenerator):
  """
  Clause implements word sequences.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __length_var__: int = 15

  #  Fallback Variables
  __fallback_count__: int = 40

  #  Private Variables
  __words_lengths__: MaybeIntList = None
  __words_array__: MaybeStrList = None

  #  Public Variables
  stochWord: StochWordBox = AttriBox[StochasticWord]()
  wordsLengths: IntListField = Field()
  wordsArray: StrListField = Field()

  #  Virtual Variables
  wordCount: IntField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @wordCount.GET
  def _getWordCount(self, ) -> int:
    return int(round(self.charCount / self.stochWord.meanLen))

  def _buildWordsLengths(self, ) -> None:
    mean, var = self.stochWord.meanLen, self.stochWord.varianceLen
    minVal, maxVal = self.stochWord.minLen, self.stochWord.maxLen
    lengths = [gauss(mean, var ** 0.5) for _ in range(self.wordCount)]
    factor = self.charCount / sum(lengths)
    lengths = [int(round(length * factor)) for length in lengths]
    lengths = [max([minVal, l]) for l in lengths]
    lengths = [min([maxVal, l]) for l in lengths]
    if self.isFirst:
      lengths[0] = 5
      lengths[1] = 5
    targetSum = self.charCount - self.wordCount + 1
    minIndex = 2 if self.isFirst else 0
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
    words = []
    for i, length in enumerate(self.wordsLengths):
      if i < 2 and self.isFirst:
        words.append(('Lorem', 'ipsum')[i])
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

  def clear(self, ) -> None:
    self.__words_lengths__ = None
    self.__words_array__ = None

  def reset(self, ) -> None:
    self.clear()
    self._buildWordsLengths()
    self._buildWordsArray()

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
