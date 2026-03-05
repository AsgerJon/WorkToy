"""
StochasticWord subclasses 'BaseObject' and exposes a weighted collection
of words as a stochastic variable.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import random
import os
from typing import TYPE_CHECKING

from . import BaseGenerator
from worktoy.desc import Field
from worktoy.work_io import validateExistingDirectory

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional

  strField: TypeAlias = Union[str, Field]
  intField: TypeAlias = Union[int, Field]
  floatField: TypeAlias = Union[float, Field]

  MaybeStr: TypeAlias = Optional[str]
  MaybeInt: TypeAlias = Optional[int]

  Words: TypeAlias = tuple[str, ...]
  MaybeTuples: TypeAlias = Optional[dict[int, Words]]
  MaybeWords: TypeAlias = Optional[Words]
  WeightedWord: TypeAlias = tuple[str, float]
  WeightedWords: TypeAlias = tuple[WeightedWord, ...]
  WeightedList: TypeAlias = list[WeightedWord]
  WeightedDict: TypeAlias = dict[int, WeightedWords]
  WeightedLengths: TypeAlias = dict[int, WeightedWords]
  MaybeLengths: TypeAlias = Optional[WeightedLengths]
  LengthsField: TypeAlias = Union[WeightedLengths, Field]

  MaybeWeighted: TypeAlias = Optional[WeightedWords]
  ListField: TypeAlias = Union[MaybeWeighted, Field]
  WeightedField: TypeAlias = Union[WeightedWords, Field]
  WeightedFiles: TypeAlias = Optional[tuple[str, float]]
  Range: TypeAlias = tuple[int, int]
  LenRange: TypeAlias = Union[int, Range]
  WordEntry: TypeAlias = tuple[str, int]

  Sample: TypeAlias = Union[str, Words]


class StochasticWord(BaseGenerator):
  """
  StochasticWord subclasses 'BaseObject' and exposes a weighted collection
  of words as a stochastic variable.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __data_env_var__: str = 'WORKTOY_DATA_DIR'
  __data_dir__: MaybeStr = None
  __weighted_files__: WeightedFiles = (
    ('common.txt', 0.8),
    ('uncommon.txt', 0.15),
    ('rare.txt', 0.05),
    )
  #  Fallback Variables

  #  Private Variables
  __weighted_words__: MaybeWeighted = None
  __by_lengths__: MaybeLengths = None
  __min_len__: MaybeInt = None
  __max_len__: MaybeInt = None

  #  Public Variables
  dataDir: strField = Field()
  weightedWords: WeightedField = Field()
  byLengths: LengthsField = Field()
  minLen: intField = Field()
  maxLen: intField = Field()

  #  Virtual Variables
  meanLen: floatField = Field()
  varianceLen: floatField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _resolveDataDir(self, **kwargs) -> None:
    envDir = os.getenv(self.__data_env_var__, )
    if envDir is not None:
      self.__data_dir__ = str(envDir)
    else:
      self.__data_dir__ = str(os.path.dirname(__file__))
    validateExistingDirectory(self.__data_dir__)

  @dataDir.GET
  def _getDataDir(self, **kwargs) -> str:
    if self.__data_dir__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._resolveDataDir()
      return self._getDataDir(_recursion=True, )
    return self.__data_dir__

  def _buildWeightedWords(self, ) -> None:
    weightedWords: list[WeightedWord] = []
    for file, weight in self.__weighted_files__:
      filePath = os.path.join(self.dataDir, file)
      f = None
      try:
        f = open(filePath, 'r')
      except Exception as exception:
        raise exception
      else:
        lines = f.readlines()
        for line in lines:
          line = line.strip()
          if line:
            weighted: WeightedWord = (line, weight)
            weightedWords.append(weighted)
      finally:
        try:
          f.close()
        except AttributeError:
          pass
    self.__weighted_words__ = (*weightedWords,)

  @weightedWords.GET
  def _getWeightedWords(self, **kwargs) -> WeightedWords:
    if self.__weighted_words__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildWeightedWords()
      return self._getWeightedWords(_recursion=True, )
    return self.__weighted_words__

  def _createMinLen(self, ) -> None:
    lengths = (*dict.keys(self.byLengths, ),)
    self.__min_len__ = min(lengths[1:])  # skipping punctuation entries

  @minLen.GET
  def _getMinLen(self, **kwargs) -> int:
    if self.__min_len__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createMinLen()
      return self._getMinLen(_recursion=True, )
    return self.__min_len__

  def _createMaxLen(self, ) -> None:
    lengths = dict.keys(self.byLengths, )
    self.__max_len__ = max(lengths)

  @maxLen.GET
  def _getMaxLen(self, **kwargs) -> int:
    if self.__max_len__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createMaxLen()
      return self._getMaxLen(_recursion=True, )
    return self.__max_len__

  def _createByLength(self, ) -> None:
    self.__by_lengths__ = dict()
    tmp = dict()
    for word, weight in self.weightedWords:
      n = len(word)
      if n in tmp:
        list.append(tmp[n], (word, weight))
        continue
      tmp[n] = [(word, weight), ]
    for key, existing in tmp.items():
      self.__by_lengths__[key] = (*existing,)

  @byLengths.GET
  def _getByLengths(self, **kwargs) -> WeightedLengths:
    if self.__by_lengths__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createByLength()
      return self._getByLengths(_recursion=True, )
    return self.__by_lengths__

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
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PUBLIC API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def realize(self, ) -> str:
    """
    Realizes a random word from the weighted collection of words.

    Returns:
      str: A random word from the weighted collection of words.
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
