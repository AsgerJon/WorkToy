"""
Sentence assembles a comma-separated sequence of 'Clause' objects
terminated by a period. Each clause is itself comma-free, so the commas
mark the boundaries between clauses unambiguously.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from ..core.sentinels import THIS
from ..dispatch import overload
from ..desc import AttriBox, Field
from . import BaseGenerator, Clause, GaussianLengths

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Self, TypeAlias, Optional, Iterator

  IntList: TypeAlias = list[int]
  MaybeIntList: TypeAlias = Optional[IntList]

  ClausesList: TypeAlias = list[Clause]
  MaybeClausesList: TypeAlias = Optional[ClausesList]


class Sentence(BaseGenerator):
  """
  A sentence is clauses joined by ', ' and closed by a period, its first
  word capitalized, exactly as many characters as requested. Clause
  lengths follow a Gaussian so sentences read naturally, and a sentence
  too short for even one clause the distribution can draw must still
  come out at its count, with every view of it, rendering, length,
  'repr', iteration and the clause list, showing the same text.

  Implementation
  --------------

  'clauseDist' is a 'GaussianLengths' of mean 40, variance 15 and bounds
  12 and 70, one per instance. 'clausesLengths' partitions the count plus
  one with 'partitionSpaced' at two slots per clause, paying for the two
  characters between clauses and the period; 'clausesArray' builds a
  'Clause' per length, 'Clause.first' for the first when 'isFirst' holds,
  capitalizes the first and terminates the last. Below
  '__truncate_below__' the one clause holds the words of '_shortText'
  directly. Each clause is comma-free, so the commas mark the clause
  boundaries. The copy constructor copies each clause through the clause
  copy constructor, so the copy owns its clauses.

  Attributes
  ----------
  clauseDist : AttriBox[GaussianLengths]
    The distribution of clause lengths.
  clausesLengths : Field[IntList]
    The cached clause lengths, a 'list[int]'.
  clausesArray : Field[ClausesList]
    The cached clauses, a 'list[Clause]'.
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
    lengths drawn from 'clauseDist' and caches them. Each clause costs its
    length and two characters more, the ', ' after it or, for the last,
    the period and the one that 'charCount + 1' pays for. A short sentence
    holds the placeholder as its one clause, of 'charCount' characters.
    """
    if self.charCount < self.__truncate_below__:
      self.__clause_lengths__ = [self.charCount, ]
      return
    lengths = self.clauseDist.partitionSpaced(self.charCount + 1, 2)
    self.__clause_lengths__ = lengths

  @clausesLengths.GET
  def _getClauseLengths(self, **kwargs) -> IntList:
    if self.__clause_lengths__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._buildClauseLengths()
      return self._getClauseLengths(_recursion=True)  # pragma: no mutate
    return self.__clause_lengths__

  def _placeholderClause(self, ) -> Clause:
    """
    The '_placeholderClause' method builds the one clause of a short
    sentence, holding the words of the placeholder text, so that the
    clause renders as the sentence does. The clause is given its words
    and their lengths directly, since the distribution cannot lay out so
    few characters.
    """
    clause = Clause(self.charCount)
    words = self._shortText().split(' ')
    clause.__words_array__ = [*words, ]
    clause.__words_lengths__ = [len(word) for word in words]
    return clause

  def _buildClausesArray(self, ) -> None:
    """
    The '_buildClausesArray' method materializes a 'Clause' for each cached
    length, capitalizes the sentence's first word, and appends a period to
    its last word. A short sentence receives the placeholder clause
    instead, which is capitalized and terminated already.
    """
    if self.charCount < self.__truncate_below__:
      self.__clause_array__ = [self._placeholderClause(), ]
      return
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
      return self._getClausesArray(_recursion=True)  # pragma: no mutate
    return self.__clause_array__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    """
    The copy constructor copies the first-word flag and the layout, each
    clause copied in turn, so the copy holds clauses of its own.
    """
    self.charCount = other.charCount
    self.isFirst = other.isFirst
    if other.__clause_lengths__ is not None:
      self.__clause_lengths__ = [*other.__clause_lengths__, ]
    if other.__clause_array__ is not None:
      self.__clause_array__ = [Clause(c) for c in other.__clause_array__]

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
    return textFmt(str.join(', ', [*(str(c) for c in self.clausesArray)]))

  def __repr__(self, ) -> str:
    return str.join('\n', [*(repr(c) for c in self.clausesArray), ])

  def __len__(self, ) -> int:
    return len(str(self))

  def __iter__(self, ) -> Iterator[Clause]:
    yield from self.clausesArray
