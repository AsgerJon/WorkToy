"""
Sentence assembles a comma-separated sequence of 'Clause' objects
terminated by a period. Each clause is itself comma-free, so the commas
mark the boundaries between clauses unambiguously.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import textFmt
from worktoy.core.sentinels import THIS
from worktoy.dispatch import overload
from worktoy.desc import AttriBox, Field
from . import BaseGenerator, Clause, GaussianLengths

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias, Optional, Iterator

  IntList: TypeAlias = list[int]
  MaybeIntList: TypeAlias = Optional[IntList]

  ClausesList: TypeAlias = list[Clause]
  MaybeClausesList: TypeAlias = Optional[ClausesList]


class Sentence(BaseGenerator):
  """
  Sentence assembles a comma-separated sequence of 'Clause' objects
  terminated by a period, summing to a target character count. Clause
  lengths are drawn from a Gaussian 'clauseDist'; the sentence's first word
  is capitalized and its last is given the closing period.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __clause_lengths__: MaybeIntList = None
  __clause_array__: MaybeClausesList = None

  #  Public Variables
  #  Clause lengths are drawn from this Gaussian: mean 40, variance 15,
  #  bounded to [12, 70].
  clauseDist = AttriBox[GaussianLengths](40, 15, 12, 70)
  clausesLengths: Field[IntList] = Field()
  clausesArray: Field[ClausesList] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _buildClauseLengths(self, ) -> None:
    """
    The '_buildClauseLengths' method partitions 'charCount' into clause
    lengths drawn from 'clauseDist' and caches them. The target leaves room
    for the ', ' between clauses and the closing period.
    """
    lengths = self.clauseDist.partitionSpaced(self.charCount + 1)
    target = self.charCount - 2 * (len(lengths) - 1) - 1
    self.__clause_lengths__ = self.clauseDist._settle(lengths, target)

  @clausesLengths.GET
  def _getClauseLengths(self, **kwargs) -> IntList:
    if self.__clause_lengths__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildClauseLengths()
      return self._getClauseLengths(_recursion=True)
    return self.__clause_lengths__

  def _buildClausesArray(self, ) -> None:
    """
    The '_buildClausesArray' method materializes a 'Clause' for each cached
    length, capitalizes the sentence's first word, and appends a period to
    its last word.
    """
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
    """
    The 'clear' method drops the cached clause lengths and clause array.
    """
    self.__clause_lengths__ = None
    self.__clause_array__ = None

  def reset(self, ) -> None:
    """
    The 'reset' method clears and regenerates the cached clause lengths and
    clause array.
    """
    self.clear()
    self._buildClauseLengths()
    self._buildClausesArray()

  def realize(self) -> str:
    """
    The 'realize' method returns the realized text for this sentence.

    Returns
    -------
    str
      The sentence rendered as text.
    """
    return str(self)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self, ) -> str:
    if self.charCount < self.__truncate_below__:
      return self._shortText()
    return textFmt(str.join(', ', [*(str(c) for c in self.clausesArray)]))

  def __repr__(self, ) -> str:
    return str.join('\n', [*(repr(c) for c in self.clausesArray), ])

  def __len__(self, ) -> int:
    return len(str(self))

  def __iter__(self, ) -> Iterator[Clause]:
    yield from self.clausesArray
