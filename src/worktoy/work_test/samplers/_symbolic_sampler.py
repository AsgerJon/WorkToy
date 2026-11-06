"""
SymbolicSampler draws samples of symbolic data.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...desc import AttriBox, SymbolicName
from ...dispatch import overload
from . import BaseSampler, randomWord

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Any

  KeyGroups: TypeAlias = dict[str, tuple[str, ...]]


class SymbolicSampler(BaseSampler):
  """
  A test of anything that renders names in several conventions wants
  random names made of real words, so that every spelling can be
  checked against the words. 'SymbolicSampler' draws 'SymbolicName'
  values, each built from 'wordCount' random words of 'LOREM_WORDS',
  three unless set otherwise and never fewer than one.

  Implementation
  --------------

  'wordCount' is an 'AttriBox[int]' with the synonyms 'numWords',
  'num_words' and 'word_count' for the keyword constructor ('count' is
  the row count, as on every sampler);
  a 'preSet' notifier refuses a count below one with 'ValueError'. The
  one-argument constructor takes the count. Each value is a
  'SymbolicName' of 'wordCount' words from 'randomWord' drawing from
  'self.random'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __key_groups__: KeyGroups = dict(
      wordCount=('wordCount', 'numWords', 'num_words', 'word_count'),
  )

  #  Public Variables
  wordCount = AttriBox[int](3)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @wordCount.preSet
  def _refuseWordCount(self, value: Any) -> None:
    if isinstance(value, (int, float)) and value < 1:
      raise ValueError("""Word count must be a positive integer.""")

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return SymbolicName

  def _getItem(self, *args, **kwargs) -> SymbolicName:
    words = (*(randomWord(self.random) for _ in range(self.wordCount)),)
    return SymbolicName(*words)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def __init__(self, wordCount: int, **kwargs) -> None:
    self.wordCount = wordCount
    if kwargs:
      self.__init__(**kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    BaseSampler.__init__(self, **kwargs)
