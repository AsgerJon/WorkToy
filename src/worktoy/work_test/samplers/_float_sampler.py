"""
FloatSampler draws random 'float' values.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...dispatch import overload
from ...desc import AttriBox
from . import IntSampler, BaseSampler


class FloatSampler(IntSampler):
  """
  A test that needs real numbers wants them from an interval it names
  as it names an integer range. 'FloatSampler' draws uniformly random
  'float' values between 'minVal' and 'maxVal', from the unit interval
  '[0.0, 1.0]' unless set otherwise, and takes 'int' bounds as floats.

  Implementation
  --------------

  'FloatSampler' is an 'IntSampler' whose two bounds are declared again
  as 'AttriBox[float]' with '0.0' and '1.0', so the synonyms, the
  ordering of a pair and of a lone bound, and the keyword constructor
  are those of 'IntSampler'; '_orderBounds' is registered again on the
  new boxes and hands on to the base. The positional constructors take
  two floats, or one float as the upper bound with zero as the lower
  one; the inherited integer signatures reach the same boxes, which
  cast. Each value is 'self.random.random()' scaled into the interval.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  minVal = AttriBox[float](0.0)
  maxVal = AttriBox[float](1.0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @minVal.onSet
  @maxVal.onSet
  def _orderBounds(self, *args) -> None:
    IntSampler._orderBounds(self, *args)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return float

  def _getItem(self, *args, **kwargs) -> float:
    return self.random.random() * (self.maxVal - self.minVal) + self.minVal

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float, float, )
  def __init__(self, minVal: float, maxVal: float, **kwargs) -> None:
    self._setBounds(minVal, maxVal)
    if kwargs:
      self.__init__(**kwargs)

  @overload(float, )
  def __init__(self, val: float, **kwargs) -> None:
    self.__init__(0.0, val)
    if kwargs:
      self.__init__(**kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    BaseSampler.__init__(self, **kwargs)
