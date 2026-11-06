"""
IntSampler draws random 'int' values.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...dispatch import overload
from ...desc import AttriBox
from . import BaseSampler

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Any

  KeyGroups: TypeAlias = dict[str, tuple[str, ...]]
  Settings: TypeAlias = dict[str, Any]


class IntSampler(BaseSampler):
  """
  A test that needs integers wants them from a range it names once, by
  position or by any usual spelling of the bounds, and wants a swapped
  pair corrected rather than refused. 'IntSampler' draws uniformly
  random 'int' values between 'minVal' and 'maxVal', both included,
  from the byte range '[0, 255]' unless set otherwise:

    class TestDice(BaseTest):

      def setUp(self) -> None:
        self.randomInteger = IntSampler(1, 6, seed=7)

  Implementation
  --------------

  'minVal' and 'maxVal' are 'AttriBox[int]' with the synonyms 'minimum',
  'min', 'min_value', 'minValue' and 'maximum', 'max', 'max_value',
  'maxValue' for the keyword constructor. '_orderBounds', an 'onSet'
  notifier of both boxes, swaps the pair whenever the upper bound falls
  below the lower, so a bound written by assignment, or a lone keyword
  crossing the other bound, is corrected. A pair is written by
  '_setBounds', with the notifier standing down until both are stored
  so that neither is ordered against a stale value; the positional
  constructors and '_applySettings', when both keywords are present,
  write through it. The one-argument constructor takes the upper bound
  with zero as the lower one. Each value is 'self.random.randint'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __key_groups__: KeyGroups = dict(
      minVal=('minVal', 'minimum', 'min', 'min_value', 'minValue'),
      maxVal=('maxVal', 'maximum', 'max', 'max_value', 'maxValue'),
  )

  #  Private Variables
  __bounds_pending__: bool = False

  #  Public Variables
  minVal = AttriBox[int](0)
  maxVal = AttriBox[int](255)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setBounds(self, low: Any, high: Any) -> None:
    """
    The '_setBounds' method writes the two bounds as a pair, each cast
    by its box, and orders the pair once both are stored; while it
    writes, '_orderBounds' stands down.
    """
    self.__bounds_pending__ = True
    try:
      self.minVal = low
      self.maxVal = high
    finally:
      self.__bounds_pending__ = False
    self._orderBounds()

  def _applySettings(self, settings: Settings) -> None:
    """
    The '_applySettings' method writes both bounds as a pair when the
    keywords name both, and hands the rest to the base.
    """
    if 'minVal' in settings and 'maxVal' in settings:
      self._setBounds(settings.pop('minVal'), settings.pop('maxVal'))
    BaseSampler._applySettings(self, settings)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @minVal.onSet
  @maxVal.onSet
  def _orderBounds(self, *args) -> None:
    """
    The '_orderBounds' notifier swaps the bounds when the upper one has
    fallen below the lower one.
    """
    if self.__bounds_pending__:
      #  This branch is reached by the following:
      #  - '_setBounds' is writing a pair and orders it once both are stored
      return
    if self.maxVal < self.minVal:
      self._setBounds(self.maxVal, self.minVal)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return int

  def _getItem(self, *args, **kwargs) -> int:
    return self.random.randint(self.minVal, self.maxVal)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int, int, )
  def __init__(self, minVal: int, maxVal: int, **kwargs) -> None:
    self._setBounds(minVal, maxVal)
    if kwargs:
      self.__init__(**kwargs)

  @overload(int, )
  def __init__(self, val: int, **kwargs) -> None:
    self.__init__(0, val)
    if kwargs:
      self.__init__(**kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    BaseSampler.__init__(self, **kwargs)
