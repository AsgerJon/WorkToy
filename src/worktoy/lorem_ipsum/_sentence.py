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
from worktoy.desc import Field
from . import BaseGenerator, Clause

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias, Optional, Iterator

  IntList: TypeAlias = list[int]
  MaybeIntList: TypeAlias = Optional[IntList]

  ClausesList: TypeAlias = list[Clause]
  MaybeClausesList: TypeAlias = Optional[ClausesList]


class Sentence(BaseGenerator):
  """
  Sentence subclasses 'BaseGenerator' and implements period separated
  sequences of words.
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
  clausesLengths: Field[IntList] = Field()
  clausesArray: Field[ClausesList] = Field()

  #  Virtual Variables
  clauseCount: Field[int] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @clauseCount.GET
  def _getClauseCount(self) -> int:
    return int(round(self.charCount / self.__clause_mean__))

  def _buildClauseLengths(self, ) -> None:
    """Sample a log-normal sequence of clause lengths summing to
    'charCount' and cache it."""
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
    """Materialize a 'Clause' for each cached length, capitalize the
    sentence's first word, and append a period to its last word."""
    clauses = []
    for length in self.clausesLengths:
      if not clauses and self.isFirst:
        clauses.append(Clause.first(length))
        continue
      clauses.append(Clause(length))
    clauses[0].capitalizeLead()
    clauses[-1].terminate('.')
    self.__clause_array__ = [*clauses, ]

  @clausesArray.GET
  def _getClausesArray(self, **kwargs) -> ClausesList:
    if self.__clause_array__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildClausesArray()
      return self._getClausesArray(_recursion=True)
    return self.__clause_array__

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
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def clear(self) -> None:
    """Drop the cached clause lengths and clause array."""
    self.__clause_lengths__ = None
    self.__clause_array__ = None

  def reset(self, ) -> None:
    """Clear and regenerate the cached clause lengths and clause array."""
    self.clear()
    self._buildClauseLengths()
    self._buildClausesArray()

  def realize(self) -> str:
    """Return the realized text for this sentence."""
    return str(self)

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
