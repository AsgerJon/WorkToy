"""
FloatSampler subclasses 'IntSample' and provides 'float' samplers.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from random import random

from ...dispatch import overload
from ...desc import Field
from . import IntSampler, BaseSampler
from ...waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union

  MaybeFloat: TypeAlias = Optional[float]
  FloatField: TypeAlias = Union[float, Field]
  MaybeBool: TypeAlias = Optional[bool]
  BoolField: TypeAlias = Union[bool, Field]


class FloatSampler(IntSampler):
  """
  FloatSampler subclasses 'IntSample' and provides 'float' samplers.
  """

  #  Fallback Variables
  __fallback_min__: float = 0.0
  __fallback_max__: float = 1.0

  #  Class Variables
  __key_defaults__: dict[str, Union[int, float]] = dict(
    minVal=__fallback_min__,
    maxVal=__fallback_max__,
  )
  __key_types__ = dict(
    minVal=float,
    maxVal=float,
  )

  #  Private Variables

  #  Public Variables

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getMinVal(self, **kwargs) -> float:
    if self.__min_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__min_value__ = self.__fallback_min__
      return self._getMinVal(_recursion=True)
    if isinstance(self.__min_value__, (int, float)):
      return float(self.__min_value__)
    raise TypeException('minVal', self.__min_value__, float)

  def _getMaxVal(self, **kwargs) -> float:
    if self.__max_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__max_value__ = self.__fallback_max__
      return self._getMaxVal(_recursion=True)
    if isinstance(self.__max_value__, (int, float)):
      return float(self.__max_value__)
    raise TypeException('maxVal', self.__max_value__, float)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setMinVal(self, minValue: float, **kwargs) -> None:
    if not isinstance(minValue, (int, float)):
      raise TypeException('minValue', minValue, float)
    self.__min_value__ = float(minValue)

  def _setMaxVal(self, maxValue: float, **kwargs) -> None:
    if not isinstance(maxValue, (int, float)):
      raise TypeException('maxValue', maxValue, float)
    self.__max_value__ = float(maxValue)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return float

  def _getItem(self, *args, **kwargs) -> float:
    """
    Returns a random float between 'minVal' and 'maxVal'.
    """
    return random() * (self.maxVal - self.minVal) + self.minVal

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float, float, )
  def __init__(self, minVal: float, maxVal: float, **kwargs) -> None:
    a, b = min([minVal, maxVal]), max([minVal, maxVal])
    self.minVal, self.maxVal = a, b
    if kwargs:
      self.__init__(**kwargs)

  @overload(float, )
  def __init__(self, maxVal: float, **kwargs) -> None:
    if kwargs:
      self.__init__(**kwargs)
    values = self.__min_value__, self.__max_value__, maxVal
    values = [v for v in values if v is not None]
    if len(values) < 2:
      values.append(0.)
    values.sort()
    self.__init__(values[0], values[-1])

  @overload()
  def __init__(self, **kwargs) -> None:
    if kwargs:
      BaseSampler.__init__(self, **kwargs)
