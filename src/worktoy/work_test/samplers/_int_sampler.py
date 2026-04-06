"""
IntSampler subclasses 'BaseSample' and provides 'int' samplers.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from random import randint

from ...dispatch import overload
from ...utilities import typeCast
from ...desc import Field
from . import BaseSampler
from ...waitaminute import TypeException
from ...waitaminute.control_flow import SkipSet
from ...waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union

  MaybeInt: TypeAlias = Optional[int]
  IntField: TypeAlias = Union[int, Field]


class IntSampler(BaseSampler):
  """
  IntSampler subclasses 'BaseSample' and provides 'int' samplers.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __min_keys__ = 'minVal', 'minimum', 'min', 'min_value', 'minValue'
  __max_keys__ = 'maxVal', 'maximum', 'max', 'max_value', 'maxValue'
  __key_groups__: dict[str, tuple[str, ...]] = dict(
    minVal=__min_keys__,
    maxVal=__max_keys__,
    )
  __key_types__: dict[str, type] = dict(
    minVal=int,
    maxVal=int,
    )
  __key_defaults__: dict[str, Union[int, float]] = dict(
    minVal=0,
    maxVal=255,
    )

  #  Fallback Variables
  __fallback_min__: int = 0
  __fallback_max__: int = 255

  #  Private Variables
  __min_value__: MaybeInt = None
  __max_value__: MaybeInt = None

  #  Public Variables
  minVal: IntField = Field()
  maxVal: IntField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createMinVal(self, ) -> None:
    self.__min_value__ = self.__fallback_min__

  def _createMaxVal(self, ) -> None:
    self.__max_value__ = self.__fallback_max__

  @minVal.GET
  def _getMinVal(self, **kwargs) -> int:
    if self.__min_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createMinVal()
      return self._getMinVal(_recursion=True)
    return self.__min_value__

  @maxVal.GET
  def _getMaxVal(self, **kwargs) -> int:
    if self.__max_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createMaxVal()
      return self._getMaxVal(_recursion=True)
    return self.__max_value__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @minVal.SET
  def _setMinVal(self, minVal: int) -> None:
    if not isinstance(minVal, int):
      try:
        casted = typeCast(int, minVal, )
      except TypeCastException as typeCastException:
        raise TypeException('minVal', minVal, int) from typeCastException
      else:
        return self._setMinVal(casted)
    return setattr(self, '__min_value__', minVal)

  @maxVal.SET
  def _setMaxVal(self, value: int) -> None:
    if not isinstance(value, int):
      try:
        casted = typeCast(int, value, )
      except TypeCastException as typeCastException:
        raise TypeException('maxVal', value, int) from typeCastException
      else:
        return self._setMaxVal(casted)
    return setattr(self, '__max_value__', value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @minVal.preSet
  def _preSetMinVal(self, value: int, *args) -> None:
    if value == self.minVal:
      raise SkipSet

  @maxVal.preSet
  def _preSetMaxVal(self, value: int, *args) -> None:
    if value == self.maxVal:
      raise SkipSet

  @minVal.onSet
  @maxVal.onSet
  def _onSetRange(self, *args) -> None:
    try:
      _ = self._getMinVal(_recursion=True)
      _ = self._getMaxVal(_recursion=True)
    except RecursionError:
      return None
    else:
      if not self.maxVal > self.minVal:
        a, b = self.minVal, self.maxVal
        self.__min_value__ = min(a, b)
        self.__max_value__ = max(a, b)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return int

  def _getItem(self, *args, **kwargs) -> int:
    return randint(self.minVal, self.maxVal)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int, int, )
  def __init__(self, minVal: int, maxVal: int, **kwargs) -> None:
    self.minVal = min(minVal, maxVal)
    self.maxVal = max(minVal, maxVal)
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
