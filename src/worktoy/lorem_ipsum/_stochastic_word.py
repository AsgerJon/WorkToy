"""
StochasticWord draws words from a weighted collection.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import random
from itertools import accumulate
from math import sqrt
from typing import TYPE_CHECKING

from . import COMMON_WORDS, UNCOMMON_WORDS, RARE_WORDS
from . import StochasticVariable
from ..desc import Field

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  from ..mcls import BaseSpace

  Words: TypeAlias = tuple[str, ...]
  CategoryWeight: TypeAlias = tuple[Words, float]
  CategoryWeights: TypeAlias = tuple[CategoryWeight, ...]

  CumWeights: TypeAlias = tuple[float, ...]
  LengthChoice: TypeAlias = tuple[Words, CumWeights]
  ByLengths: TypeAlias = dict[int, LengthChoice]
  WordLengths: TypeAlias = dict[int, Words]

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = BaseSpace


class StochasticWord(StochasticVariable):
  """
  StochasticWord is a 'StochasticVariable' whose distribution is the
  weighted collection of words it carries: drawing a value means drawing a
  word length, weighted by how the words are distributed.

  The 'mean', 'var', 'minVal', and 'maxVal' fields belong to the base
  class; this subclass only fills their getters, each returning a value
  cached once. Those four statistics and the per-length sampler are
  computed in '__class_init__' from '__category_weights__'. The sampler
  pairs each length with its words and the cumulative weights of those
  words, so 'realizeLength' draws with a single 'bisect' rather than
  rebuilding a weight table per call. A subclass overriding the weights
  gets its own caches when it is declared, so no analysis happens per
  instance.

  'sampleInteger' draws a length from the distribution and 'realize' turns
  that length into a word, so a realized word's length follows the cached
  statistics. This assumes the word lengths are gapless across
  '[minVal, maxVal]', which holds for the built-in collection.
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
  __by_lengths__: ByLengths = None
  __mean_value__: float = None
  __var_value__: float = None
  __min_value__: int = None
  __max_value__: int = None

  #  Public Variables
  byLengths: Field[WordLengths] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getMean(self) -> float:
    return self.__mean_value__

  def _getVar(self) -> float:
    return self.__var_value__

  def _getMinVal(self) -> int:
    return self.__min_value__

  def _getMaxVal(self) -> int:
    return self.__max_value__

  @byLengths.GET
  def _getByLengths(self) -> WordLengths:
    return {n: words for n, (words, _) in self.__by_lengths__.items()}

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_init__(
      cls,
      name: str,
      bases: Bases,
      space: Space,
      **kwargs,
  ) -> None:
    """
    The '__class_init__' method flattens '__category_weights__' into a
    weighted word table, builds the per-length sampler, and reduces the
    table to the four
    statistics, caching them on the concrete class so the getters and
    'realizeLength' read prepared values rather than rebuild them.

    Parameters
    ----------
    name : str
      The name given to the concrete class being created.
    bases : Bases
      The base classes of the concrete class, a 'tuple[type, ...]'.
    space : Space
      The prepared class body namespace, a 'BaseSpace'.
    """
    super().__class_init__(name, bases, space, **kwargs)
    pairs = []
    for words, weight in cls.__category_weights__:
      for word in words:
        pairs.append((word, weight))
    grouped: dict = dict()
    for word, weight in pairs:
      grouped.setdefault(len(word), []).append((word, weight))
    byLengths = dict()
    for length, bucket in grouped.items():
      words = (*(word for word, _ in bucket),)
      cumWeights = (*accumulate(weight for _, weight in bucket),)
      byLengths[length] = (words, cumWeights)
    total = sum(weight for _, weight in pairs)
    mean = sum(len(word) * weight for word, weight in pairs) / total
    spread = sum((len(word) - mean) ** 2 * weight for word, weight in pairs)
    cls.__by_lengths__ = byLengths
    cls.__mean_value__ = mean
    cls.__var_value__ = spread / total
    cls.__min_value__ = min(grouped)
    cls.__max_value__ = max(grouped)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __getitem__(self, length: int) -> str:
    """
    The '__getitem__' method aliases 'realizeLength', so indexing by a
    length realizes a word of that length.

    Parameters
    ----------
    length : int
      The exact character length the realized word must have.

    Returns
    -------
    str
      A word of the requested length.
    """
    return self.realizeLength(length)

  def sampleInteger(self) -> int:
    """
    The 'sampleInteger' method draws one length from the distribution, a
    Gaussian of the cached mean and variance clamped to the inclusive
    bounds.

    Returns
    -------
    int
      A length drawn from the distribution and clamped to
      '[minVal, maxVal]'.
    """
    value = round(random.gauss(self.mean, sqrt(self.var)))
    return min(self.maxVal, max(self.minVal, value))

  def realize(self) -> str:
    """
    The 'realize' method draws a length from the distribution and realizes a
    word of that length, so the realized word's length follows the cached
    statistics.

    Returns
    -------
    str
      A word whose length was drawn from the distribution.
    """
    return self.realizeLength(self.sampleInteger())

  def realizeLength(self, length: int) -> str:
    """
    The 'realizeLength' method draws one word of the requested length,
    weighted by the category each word came from.

    Parameters
    ----------
    length : int
      The exact character length the realized word must have.

    Returns
    -------
    str
      A word of the requested length.

    Raises
    ------
    IndexError
      If the distribution holds no word of the requested length.
    """
    choice = self.__by_lengths__.get(length)
    if choice is None:
      infoSpec = """Found no words of length '%d'!"""
      raise IndexError(infoSpec % length)
    words, cumWeights = choice
    return random.choices(words, cum_weights=cumWeights)[0]
