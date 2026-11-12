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
    Two bounds given together must be ordered against each other, never
    one of them against the bound the other is about to replace. Writing
    300 and 400 over the range from 0 to 255 one bound at a time would
    find the new lower bound above the old upper one, swap the two, and
    end at 255 and 400.

    Implementation
    --------------

    Both bounds are written, each cast by its box, while
    '__bounds_pending__' makes '_orderBounds' stand down, and
    '_orderBounds' orders the pair once both are stored.

    Parameters
    ----------

    low : Any
      The one bound.

    high : Any
      The other bound.
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
    Two bounds given by keyword belong together as two given by position
    do, and must be written as a pair.

    Implementation
    --------------

    When the settings hold both bounds, the two are taken out and
    written through '_setBounds'. The rest, a lone bound included, goes
    to 'BaseSampler._applySettings'.

    Parameters
    ----------

    settings : Settings
      A 'dict[str, Any]' from the name of each setting found to its
      value.
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
    A test names a range by its two ends and should not have to care
    which it wrote first, and a bound assigned later must not leave the
    range empty.

    Implementation
    --------------

    The method is the 'onSet' notifier of both boxes. Unless
    '_setBounds' is writing a pair, an upper bound found below the lower
    one makes it write the two swapped, through '_setBounds'.
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
