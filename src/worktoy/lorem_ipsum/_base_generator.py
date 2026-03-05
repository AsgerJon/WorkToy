"""
BaseGenerator subclasses 'BaseObject' and provides functionality shared by
'Sentence' and 'Paragraph' for generating stochastic text.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from math import exp, log, sqrt
from random import gauss, randint

from worktoy.utilities import maybe
from worktoy.dispatch import overload
from worktoy.desc import AttriBox, Field
from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Self

  MaybeBool: TypeAlias = Optional[bool]

  BoolField: TypeAlias = Union[bool, Field]
  IntBox: TypeAlias = Union[int, AttriBox]


class BaseGenerator(BaseObject):
  """
  BaseGenerator provides functionality shared by 'Sentence' and
  'Paragraph' for generating stochastic text.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def logNormal(mean: float, var: float) -> float:
    innerVar = log(1 + var / mean ** 2)
    innerMean = log(mean) - innerVar / 2
    return exp(gauss(innerMean, sqrt(innerVar)))

  @staticmethod
  def scaleSum(
      lengths: list[int],
      targetSum: int,
      minVal: int,
      maxVal: int,
      minIndex: int = None,
      maxIndex: int = None,
      ) -> list[int]:
    """
    Adjusts the sum of the integers in the given list randomly
    incrementing or decrementing the integers until the sum of the
    integers is reduced by the given amount.

    Parameters
    ----------
    lengths : list[int]
      The list of integers to adjust.
    targetSum: int
      The target sum of the integers in the list after adjustments.
    minVal: int
      Entries in the list with this value or lower will not be decremented.
    maxVal: int
      Entries in the list with this value or higher will not be incremented.
    minIndex: int (Optional)
      If given, only entries greater than or equal to this index will be
      adjusted.
    maxIndex: int (Optional)
      If given, only entries less than this index will be adjusted.

    Returns
    -------
    list[int]
      Returns the original list after adjustments.
    """
    minIndex = maybe(minIndex, 0)
    maxIndex = maybe(maxIndex, len(lengths) - 1)
    miss = sum(lengths) - targetSum
    while abs(miss) > 0:
      index = randint(minIndex, maxIndex)
      currentValue = lengths[index]
      if miss > 0 and currentValue > minVal:
        lengths[index] -= 1
        miss -= 1
      elif miss < 0 and currentValue < maxVal:
        lengths[index] += 1
        miss += 1
    return lengths

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __is_first__: MaybeBool = None

  #  Public Variables
  charCount: IntBox = AttriBox[int](40)
  isFirst: BoolField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @isFirst.GET
  def _getIsFirst(self, ) -> bool:
    return maybe(self.__is_first__, False)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def __init__(self, charCount: int) -> None:
    self.charCount = charCount

  @overload()
  def __init__(self, **kwargs) -> None:
    try:
      count = getattr(type(self), '__fallback_count__')
    except AttributeError:
      pass
    else:
      self.__init__(count)

  @classmethod
  def first(cls, *args, **kwargs) -> Self:
    self = cls(*args, **kwargs)
    self.__is_first__ = True
    return self

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
