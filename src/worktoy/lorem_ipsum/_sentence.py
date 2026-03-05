"""
Sentence subclasses 'BaseGenerator' and implements period separated
sequences of words.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import textFmt
from worktoy.core.sentinels import THIS
from worktoy.dispatch import overload
from worktoy.desc import Field, AttriBox

from . import StochasticWord, BaseGenerator, Clause

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias, Union, Optional, Iterator

  IntField: TypeAlias = Union[int, Field]

  IntList: TypeAlias = list[int]
  MaybeIntList: TypeAlias = Optional[IntList]
  IntListField: TypeAlias = Union[IntList, Field]

  ClausesList: TypeAlias = list[Clause]
  MaybeClausesList: TypeAlias = Optional[ClausesList]
  ClausesField: TypeAlias = Union[ClausesList, Field]

  StochWordBox: TypeAlias = Union[StochasticWord, AttriBox]


class Sentence(BaseGenerator):
  """
  Sentence subclasses 'BaseObject' and implements period separated sequences
  of words.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __clause_mean__: int = 40
  __clause_var__: int = 15

  #  Fallback Variables
  __fallback_count__: int = 120

  #  Private Variables
  __clause_lengths__: MaybeIntList = None
  __clause_array__: MaybeClausesList = None

  #  Public Variables
  clausesLengths: IntListField = Field()
  clausesArray: ClausesField = Field()

  #  Virtual Variables
  clauseCount: IntField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @clauseCount.GET
  def _getClauseCount(self) -> int:
    return int(round(self.charCount / self.__clause_mean__))

  def _buildClauseLengths(self, ) -> None:
    mean, var = self.__clause_mean__, self.__clause_var__
    lengths = [self.logNormal(mean, var) for _ in range(self.clauseCount)]
    factor = self.charCount / sum(lengths)
    lengths = [int(round(l * factor)) for l in lengths]
    target = self.charCount - self.clauseCount * 2 + 1
    minV, maxV = mean - 2 * var, mean + 2 * var
    self.__clause_lengths__ = self.scaleSum(lengths, target, minV, maxV, )

  @clausesLengths.GET
  def _getClauseLengths(self, **kwargs) -> IntList:
    if self.__clause_lengths__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildClauseLengths()
      return self._getClauseLengths(_recursion=True)
    return self.__clause_lengths__

  def _buildClausesArray(self, ) -> None:
    clauses = []
    for length in self.clausesLengths:
      if not clauses and self.isFirst:
        clauses.append(Clause.first(length))
        continue
      clauses.append(Clause(length))
    clauses[0].wordsArray[0] = str.capitalize(clauses[0].wordsArray[0])
    clauses[-1].wordsArray[-1] = """%s.""" % clauses[-1].wordsArray[-1]
    self.__clause_array__ = [*clauses, ]

  @clausesArray.GET
  def _getClausesArray(self, **kwargs) -> ClausesList:
    if self.__clause_array__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildClausesArray()
      return self._getClausesArray(_recursion=True)
    return self.__clause_array__

  def clear(self) -> None:
    self.__clause_lengths__ = None
    self.__clause_array__ = None

  def reset(self, ) -> None:
    self.clear()
    self._buildClauseLengths()
    self._buildClausesArray()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.charCount = other.charCount
    if other.__clause_lengths__ is not None:
      self.__clause_lengths__ = [*other.__clause_lengths__, ]
    if other.__clause_array__ is not None:
      self.__clause_array__ = [*other.__clause_array__, ]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self, ) -> str:
    return textFmt(str.join(', ', [*(str(c) for c in self.clausesArray)]))

  def __repr__(self, ) -> str:
    return str.join('\n', [*(repr(c) for c in self.clausesArray), ])

  def __len__(self, ) -> int:
    return len(str(self))

  def __iter__(self, ) -> Iterator[Clause]:
    yield from self.clausesArray
