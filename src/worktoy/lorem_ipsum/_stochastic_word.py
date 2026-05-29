"""
StochasticWord draws words from a weighted collection.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import random
from typing import TYPE_CHECKING

from . import COMMON_WORDS, UNCOMMON_WORDS, RARE_WORDS
from worktoy.desc import Field
from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional

  MaybeInt: TypeAlias = Optional[int]

  Words: TypeAlias = tuple[str, ...]
  WeightedWord: TypeAlias = tuple[str, float]
  WeightedWords: TypeAlias = tuple[WeightedWord, ...]
  WeightedLengths: TypeAlias = dict[int, WeightedWords]
  MaybeLengths: TypeAlias = Optional[WeightedLengths]

  MaybeWeighted: TypeAlias = Optional[WeightedWords]
  CategoryWeight: TypeAlias = tuple[Words, float]
  CategoryWeights: TypeAlias = tuple[CategoryWeight, ...]


class StochasticWord(BaseObject):
  """
  StochasticWord subclasses 'BaseObject' and exposes a weighted
  collection of words as a stochastic variable.

  Unlike 'Clause', 'Sentence', and 'Paragraph', a 'StochasticWord' has
  no 'charCount', no 'isFirst' notion, and no '.first(...)' constructor:
  it is a distribution over words, not a size-driven text generator.

  Derived caches ('weightedWords', 'byLengths', 'minLen', 'maxLen') are
  fully determined by '__category_weights__' and are therefore stored
  on the concrete class rather than per instance. Each subclass that
  overrides '__category_weights__' computes its own caches on first
  access via 'cls.__dict__' lookups.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __category_weights__: CategoryWeights = (
    (COMMON_WORDS, 0.8),
    (UNCOMMON_WORDS, 0.15),
    (RARE_WORDS, 0.05),
  )

  #  Class-Level Caches
  #  Populated lazily per concrete class via 'cls.__dict__' lookups so
  #  subclasses overriding '__category_weights__' get their own.
  __weighted_words__: MaybeWeighted = None
  __by_lengths__: MaybeLengths = None
  __min_len__: MaybeInt = None
  __max_len__: MaybeInt = None

  #  Public Variables
  weightedWords: Field[WeightedWords] = Field()
  byLengths: Field[WeightedLengths] = Field()
  minLen: Field[int] = Field()
  maxLen: Field[int] = Field()

  #  Virtual Variables
  meanLen: Field[float] = Field()
  varianceLen: Field[float] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _buildWeightedWords(self, ) -> None:
    """Flatten the category-weighted word tuples into a single weighted
    tuple and store it on the concrete class."""
    cls = type(self)
    weightedWords: list[WeightedWord] = []
    for category, weight in cls.__category_weights__:
      for word in category:
        weightedWords.append((word, weight))
    setattr(cls, '__weighted_words__', (*weightedWords,))

  @weightedWords.GET
  def _getWeightedWords(self, **kwargs) -> WeightedWords:
    cls = type(self)
    cached = cls.__dict__.get('__weighted_words__')
    if cached is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildWeightedWords()
      return self._getWeightedWords(_recursion=True, )
    return cached

  def _createMinLen(self, ) -> None:
    """Cache the shortest word length present in 'byLengths' on the
    concrete class."""
    cls = type(self)
    lengths = (*dict.keys(self.byLengths, ),)
    setattr(cls, '__min_len__', min(lengths))

  @minLen.GET
  def _getMinLen(self, **kwargs) -> int:
    cls = type(self)
    cached = cls.__dict__.get('__min_len__')
    if cached is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createMinLen()
      return self._getMinLen(_recursion=True, )
    return cached

  def _createMaxLen(self, ) -> None:
    """Cache the longest word length present in 'byLengths' on the
    concrete class."""
    cls = type(self)
    lengths = dict.keys(self.byLengths, )
    setattr(cls, '__max_len__', max(lengths))

  @maxLen.GET
  def _getMaxLen(self, **kwargs) -> int:
    cls = type(self)
    cached = cls.__dict__.get('__max_len__')
    if cached is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createMaxLen()
      return self._getMaxLen(_recursion=True, )
    return cached

  def _createByLength(self, ) -> None:
    """Group all weighted words by their character length and store the
    resulting 'length -> WeightedWords' mapping on the concrete class."""
    cls = type(self)
    byLengths: dict = dict()
    tmp = dict()
    for word, weight in self.weightedWords:
      n = len(word)
      if n in tmp:
        list.append(tmp[n], (word, weight))
        continue
      tmp[n] = [(word, weight), ]
    for key, existing in tmp.items():
      byLengths[key] = (*existing,)
    setattr(cls, '__by_lengths__', byLengths)

  @byLengths.GET
  def _getByLengths(self, **kwargs) -> WeightedLengths:
    cls = type(self)
    cached = cls.__dict__.get('__by_lengths__')
    if cached is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createByLength()
      return self._getByLengths(_recursion=True, )
    return cached

  @meanLen.GET
  def _getMeanLen(self, **kwargs) -> float:
    totalLen = 0
    totalWords = 0
    for word, weight in self.weightedWords:
      totalLen += len(word) * weight
      totalWords += weight
    return totalLen / totalWords

  @varianceLen.GET
  def _getVarianceLen(self, **kwargs) -> float:
    mean = self.meanLen
    totalLen = 0
    totalWords = 0
    for word, weight in self.weightedWords:
      totalLen += ((len(word) - mean) ** 2) * weight
      totalWords += weight
    return totalLen / totalWords

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __getitem__(self, index: int) -> WeightedWords:
    try:
      words = self.byLengths[index]
    except KeyError as keyError:
      infoSpec = """Found no words of length '%d'!"""
      info = infoSpec % index
      raise IndexError(info) from keyError
    else:
      return (*words,)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PUBLIC API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def realize(self, ) -> str:
    """
    Realizes a random word from the weighted collection of words.

    Returns
    -------
    str
      A random word from the weighted collection of words.
    """
    words = tuple(map(lambda x: x[0], self.weightedWords))
    weights = tuple(map(lambda x: x[1], self.weightedWords))
    return random.choices(words, weights=weights, k=1)[0]

  def realizeLength(self, charLen: int, ) -> str:
    """
    Realizes a random word from the weighted collection of words having
    the given length.
    """
    words = tuple(map(lambda x: x[0], self[charLen]))
    weights = tuple(map(lambda x: x[1], self[charLen]))
    return random.choices(words, weights=weights, k=1)[0]
