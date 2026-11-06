"""
StochasticWord draws words from a weighted collection.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import random
from itertools import accumulate
from typing import TYPE_CHECKING

from . import COMMON_WORDS, UNCOMMON_WORDS, RARE_WORDS
from . import StochasticVariable
from ..desc import Field
from ..utilities import textFmt, joinWords

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Optional

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
  The words of a clause must come out at the lengths the clause was cut
  into, and the cut itself must follow how long words are, so a word list
  is both a distribution over lengths and the source of a word of any
  length it holds. A project must be able to bring its own words, in
  tiers with weights of its own, by subclassing and nothing more, and
  must learn at the class statement, not at some later draw, when its
  list leaves out a length a draw may ask for.

  Implementation
  --------------

  '__category_weights__' pairs each tier of words with the weight of
  every word in it. '__class_init__', the class hook 'AbstractMetaclass'
  calls once a class exists, flattens the tiers, groups the words by
  length, refuses through '_refuseGaps' with 'ValueError' a length
  missing between the shortest and the longest, and writes onto the class
  a table of each length to its words and their cumulative weights, and
  the four statistics of the lengths, 'mean', 'var', 'minVal' and
  'maxVal', as class attributes; a subclass rebinding the weights gets
  values of its own, and no analysis runs per instance. The draw is the
  base's. 'realizeLength' draws one word of a length with
  'random.choices' over the cumulative weights and refuses a length
  without words with 'IndexError'; 'realize' draws a length and then a
  word; 'word[n]' reads as 'realizeLength(n)'.

  Attributes
  ----------
  mean : float
    The weighted mean of the word lengths, written at the class statement.
  var : float
    The weighted variance of the word lengths.
  minVal : int
    The shortest word length.
  maxVal : int
    The longest word length.
  byLengths : Field[WordLengths]
    The words of each length, a new 'dict[int, tuple[str, ...]]' at
    every read.
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

  #  Class-Level Caches, written by '__class_init__'
  __by_lengths__: ByLengths = None
  mean: Optional[float] = None
  var: Optional[float] = None
  minVal: Optional[int] = None
  maxVal: Optional[int] = None

  #  Public Variables
  byLengths: Field[WordLengths] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    table to the four statistics, writing them onto the concrete class so
    the base and 'realizeLength' read prepared values rather than rebuild
    them.

    Parameters
    ----------
    name : str
      The name given to the concrete class being created.
    bases : Bases
      The base classes of the concrete class, a 'tuple[type, ...]'.
    space : Space
      The prepared class body namespace, a 'BaseSpace'.
    """
    pairs = []
    for words, weight in cls.__category_weights__:
      for word in words:
        pairs.append((word, weight))
    grouped: dict = dict()
    for word, weight in pairs:
      grouped.setdefault(len(word), []).append((word, weight))
    cls._refuseGaps(*grouped)
    byLengths = dict()
    for length, bucket in grouped.items():
      words = (*(word for word, _ in bucket),)
      cumWeights = (*accumulate(weight for _, weight in bucket),)
      byLengths[length] = (words, cumWeights)
    total = sum(weight for _, weight in pairs)
    mean = sum(len(word) * weight for word, weight in pairs) / total
    spread = sum((len(word) - mean) ** 2 * weight for word, weight in pairs)
    cls.__by_lengths__ = byLengths
    cls.mean = mean
    cls.var = spread / total
    cls.minVal = min(grouped)
    cls.maxVal = max(grouped)

  @classmethod
  def _refuseGaps(cls, *lengths: int) -> None:
    """
    The '_refuseGaps' method raises 'ValueError' when the word 'lengths'
    leave out a length between the shortest and the longest, since
    'sampleInteger' may draw any length in that range and 'realizeLength'
    then finds no word of it.
    """
    span = range(min(lengths), max(lengths) + 1)
    missing = [length for length in span if length not in lengths]
    if missing:
      infoSpec = """StochasticWord class '%s' has words of lengths from %d
      to %d, but none of length %s. Any length in that range may be drawn,
      so each needs a word."""
      missingStr = joinWords(*missing, sep='or')
      info = infoSpec % (cls.__name__, span[0], span[-1], missingStr)
      raise ValueError(textFmt(info))

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
