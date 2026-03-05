"""
Paragraph subclasses 'BaseGenerator' and concatenates 'Sentence' objects
forming size specified paragraphs.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.dispatch import overload
from worktoy.desc import Field, AttriBox
from worktoy.utilities import textFmt
from . import StochasticWord, Sentence, BaseGenerator

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias, Union, Optional, Iterator

  MaybeBool: TypeAlias = Optional[bool]
  IntField: TypeAlias = Union[int, Field]
  IntList: TypeAlias = list[int]
  MaybeIntList: TypeAlias = Optional[IntList]
  IntListField: TypeAlias = Union[IntList, Field]

  SentenceList: TypeAlias = list[Sentence]
  MaybeSentenceList: TypeAlias = Optional[SentenceList]
  SentenceListField: TypeAlias = Union[SentenceList, Field]


class Paragraph(BaseGenerator):
  """
  Paragraph subclasses 'BaseObject' and concatenates 'Sentence' objects
  forming size specified paragraphs.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __sentence_mean__: int = 80
  __sentence_var__: int = 20

  #  Fallback Variables
  __fallback_count__: int = 800

  #  Private Variables
  __is_first__: MaybeBool = True  # Paragraphs defaults to being 'first'.
  __sentences_lengths__: MaybeIntList = None
  __sentences_array__: MaybeSentenceList = None

  #  Public Variables
  sentenceLengths: IntListField = Field()
  sentenceArray: SentenceListField = Field()

  #  Virtual Variables
  sentenceCount: IntField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @sentenceCount.GET
  def _getSentenceCount(self, **kwargs) -> int:
    return int(round(self.charCount / self.__sentence_mean__))

  def _buildSentencesLengths(self, **kwargs) -> None:
    mean, var = self.__sentence_mean__, self.__sentence_var__
    lengths = [self.logNormal(mean, var) for _ in range(self.sentenceCount)]
    factor = self.charCount / sum(lengths)
    lengths = [int(round(length * factor)) for length in lengths]
    target = self.charCount - self.sentenceCount + 1
    minV, maxV = mean - 2 * var, mean + 2 * var
    self.__sentences_lengths__ = self.scaleSum(
      lengths,
      target,
      minV,
      maxV,
      )

  @sentenceLengths.GET
  def _getSentenceLengths(self, **kwargs) -> IntList:
    if self.__sentences_lengths__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildSentencesLengths(_recursion=True)
      return self._getSentenceLengths(_recursion=True)
    return self.__sentences_lengths__

  def _buildSentencesArray(self, ) -> None:
    sentences: SentenceList = []
    for length in self.sentenceLengths:
      if not sentences and self.isFirst:
        sentences.append(Sentence.first(length))
        continue
      sentences.append(Sentence(length))
    self.__sentences_array__ = [*sentences, ]

  @sentenceArray.GET
  def _getSentenceArray(self, **kwargs) -> SentenceList:
    if self.__sentences_array__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildSentencesArray()
      return self._getSentenceArray(_recursion=True)
    return self.__sentences_array__

  def clear(self) -> None:
    self.__sentences_lengths__ = None
    self.__sentences_array__ = None

  def reset(self, ) -> None:
    self.clear()
    self._buildSentencesLengths()
    self._buildSentencesArray()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.charCount = other.charCount
    if other.__sentences_lengths__ is not None:
      self.__sentences_lengths__ = [*other.__sentences_lengths__, ]
    if other.__sentences_array__ is not None:
      self.__sentences_array__ = [*other.__sentences_array__, ]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self, ) -> str:
    return textFmt(str.join(' ', [*(str(s) for s in self.sentenceArray)]))

  def __repr__(self, ) -> str:
    return '\n'.join([*(repr(s) for s in self.sentenceArray), ])

  def __len__(self, ) -> int:
    sentences = self.sentenceArray
    return sum(len(s) for s in sentences) + len(sentences) - 1

  def __iter__(self, ) -> Iterator[Sentence]:
    yield from self.sentenceArray
