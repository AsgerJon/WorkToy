"""
SymbolicSampler subclasses 'BaseSample' and provides samplers of symbolic
data.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...desc import Field, SymbolicName
from ...dispatch import overload
from ...lorem_ipsum import StochasticWord
from . import BaseSampler

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union

  MaybeInt: TypeAlias = Optional[int]
  IntField: TypeAlias = Union[int, Field]
  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]
  MaybeSymbolic: TypeAlias = Optional[SymbolicName]
  SymbolicField: TypeAlias = Union[Field, SymbolicName]


class SymbolicSampler(BaseSampler):
  """
  SymbolicSampler subclasses 'BaseSample' and provides samplers of symbolic
  data.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables
  __fallback_count__: int = 3

  #  Class Variables
  __count_keys__: tuple[str, ...] = (
    'wordCount',
    'count',
    'numWords',
    'num_words',
    'word_count',
    )
  __key_groups__: dict[str, tuple[str, ...]] = dict(
    wordCount=__count_keys__,
    )
  __key_types__: dict[str, type] = dict(
    wordCount=int,
    )
  __key_defaults__: dict[str, Union[int, float]] = dict(
    wordCount=__fallback_count__,
    )

  #  Private Variables
  __word_count__: MaybeInt = None

  #  Public Variables
  wordCount: IntField = Field()
  stochWord = StochasticWord()

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createWordCount(self, ) -> None:
    self.__word_count__ = self.__fallback_count__

  @wordCount.GET
  def _getWordCount(self, **kwargs) -> int:
    if self.__word_count__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createWordCount()
      return self._getWordCount(_recursion=True)
    return self.__word_count__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @wordCount.SET
  def _setWordCount(self, value: int) -> None:
    self.__word_count__ = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return SymbolicName

  def _getItem(self, *args, **kwargs) -> SymbolicName:
    words = (*(self.stochWord.realize() for _ in range(self.wordCount)),)
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

    """Megan campbell"""
