"""
Paragraph assembles a paragraph from a sequence of 'Sentence' objects.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.dispatch import overload
from worktoy.desc import AttriBox, Field
from worktoy.utilities import textFmt
from . import Sentence, BaseGenerator, GaussianLengths

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias, Optional, Iterator

  MaybeBool: TypeAlias = Optional[bool]
  IntList: TypeAlias = list[int]
  MaybeIntList: TypeAlias = Optional[IntList]

  SentenceList: TypeAlias = list[Sentence]
  MaybeSentenceList: TypeAlias = Optional[SentenceList]


class Paragraph(BaseGenerator):
  """
  Paragraph assembles a space-separated sequence of 'Sentence' objects
  summing to a target character count, with sentence lengths drawn from a
  Gaussian 'sentenceDist'. Paragraphs default to 'isFirst=True', so the
  first sentence begins with 'Lorem ipsum'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  #  Paragraphs default to 'isFirst=True' so the first sentence begins
  #  with 'Lorem ipsum'. Clause and Sentence require an explicit
  #  '.first(...)' constructor instead because they often appear
  #  mid-document.
  __is_first__: MaybeBool = True
  __sentences_lengths__: MaybeIntList = None
  __sentences_array__: MaybeSentenceList = None

  #  Public Variables
  #  Sentence lengths are drawn from this Gaussian: mean 80, variance 20,
  #  bounded to [40, 120].
  sentenceDist = AttriBox[GaussianLengths](80, 20, 40, 120)
  sentenceLengths: Field[IntList] = Field()
  sentenceArray: Field[SentenceList] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _buildSentencesLengths(self, ) -> None:
    """
    The '_buildSentencesLengths' method partitions 'charCount' into
    sentence lengths drawn from 'sentenceDist' and caches them. The target
    leaves room for the single space between sentences. A 'charCount'
    below the shortest length 'sentenceDist' can draw becomes a single
    sentence length of exactly 'charCount', since 'Sentence' realizes
    short counts exactly through its own placeholder fallback.
    """
    if self.charCount < self.sentenceDist.minVal:
      self.__sentences_lengths__ = [self.charCount, ]
      return
    self.__sentences_lengths__ = self.sentenceDist.partitionSpaced(
        self.charCount + 1)

  @sentenceLengths.GET
  def _getSentenceLengths(self, **kwargs) -> IntList:
    if self.__sentences_lengths__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildSentencesLengths()
      return self._getSentenceLengths(_recursion=True)
    return self.__sentences_lengths__

  def _buildSentencesArray(self, ) -> None:
    """
    The '_buildSentencesArray' method materializes a 'Sentence' for each
    cached length and caches the resulting sentence list.
    """
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
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def clear(self) -> None:
    """
    The 'clear' method drops the cached sentence lengths and sentence
    array.
    """
    self.__sentences_lengths__ = None
    self.__sentences_array__ = None

  def reset(self, ) -> None:
    """
    The 'reset' method clears and regenerates the cached sentence lengths
    and array.
    """
    self.clear()
    self._buildSentencesLengths()
    self._buildSentencesArray()

  def realize(self) -> str:
    """
    The 'realize' method returns the realized text for this paragraph.

    Returns
    -------
    str
      The paragraph rendered as text.
    """
    return str(self)

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
