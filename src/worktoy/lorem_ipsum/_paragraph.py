"""
Paragraph assembles a paragraph from a sequence of 'Sentence' objects.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.sentinels import THIS
from ..dispatch import overload
from ..desc import AttriBox, Field
from ..utilities import textFmt
from . import Sentence, BaseGenerator, GaussianLengths

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Self, TypeAlias, Optional, Iterator

  IntList: TypeAlias = list[int]
  MaybeIntList: TypeAlias = Optional[IntList]

  SentenceList: TypeAlias = list[Sentence]
  MaybeSentenceList: TypeAlias = Optional[SentenceList]


class Paragraph(BaseGenerator):
  """
  A paragraph is sentences joined by single spaces, exactly as many
  characters as requested, and the usual block a mock-up asks for, so it
  opens with 'Lorem ipsum' unless told otherwise, where a clause or a
  sentence, which often sit mid-document, opens with it only through
  'first'.

  Implementation
  --------------

  'isFirst' is redeclared as an 'AttriBox[bool]' of 'True', taking the
  base's 'onSet' callback again. 'sentenceDist' is a 'GaussianLengths' of
  mean 80, variance 20 and bounds 40 and 120, one per instance.
  'sentenceLengths' partitions the count plus one with 'partitionSpaced',
  one space per sentence; a count below the shortest sentence the
  distribution can draw becomes one sentence of that count, which
  'Sentence' lays out or renders as its placeholder. 'sentenceArray'
  builds a 'Sentence' per length, 'Sentence.first' for the first when
  'isFirst' holds. 'len' is the sum of the sentence lengths and the
  spaces between them. The copy constructor copies each sentence through
  the sentence copy constructor, so the copy owns its sentences.

  Attributes
  ----------
  sentenceDist : AttriBox[GaussianLengths]
    The distribution of sentence lengths.
  sentenceLengths : Field[IntList]
    The cached sentence lengths, a 'list[int]'.
  sentenceArray : Field[SentenceList]
    The cached sentences, a 'list[Sentence]'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __sentences_lengths__: MaybeIntList = None
  __sentences_array__: MaybeSentenceList = None

  #  Public Variables
  #  Paragraphs are first by default, so the first sentence begins with
  #  'Lorem ipsum'. Clause and Sentence require an explicit '.first(...)'
  #  constructor instead because they often appear mid-document.
  isFirst = AttriBox[bool](True)
  #  Sentence lengths are drawn from this Gaussian: mean 80, variance 20,
  #  bounded to [40, 120].
  sentenceDist = AttriBox[GaussianLengths](80, 20, 40, 120)
  sentenceLengths: Field[IntList] = Field()
  sentenceArray: Field[SentenceList] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  A box records its callbacks on itself, so the box redeclared above
  #  takes the callback of 'BaseGenerator' again: an assignment of
  #  'isFirst' drops the cached layout here as it does there.
  _onSetIsFirst = isFirst.onSet(BaseGenerator._onSetIsFirst)

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
        self.charCount + 1
    )

  @sentenceLengths.GET
  def _getSentenceLengths(self, **kwargs) -> IntList:
    if self.__sentences_lengths__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildSentencesLengths()
      return self._getSentenceLengths(_recursion=True)  # pragma: no mutate
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
      return self._getSentenceArray(_recursion=True)  # pragma: no mutate
    return self.__sentences_array__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    """
    The copy constructor copies the first-word flag and the layout, each
    sentence copied in turn, so the copy holds sentences of its own.
    """
    self.charCount = other.charCount
    self.isFirst = other.isFirst
    if other.__sentences_lengths__ is not None:
      self.__sentences_lengths__ = [*other.__sentences_lengths__, ]
    if other.__sentences_array__ is not None:
      copies = [Sentence(s) for s in other.__sentences_array__]
      self.__sentences_array__ = copies

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
