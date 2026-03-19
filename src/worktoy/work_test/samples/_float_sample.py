"""
FloatSample subclasses 'IntSample' and provides 'float' samples.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from random import random, gauss as normal

from ...dispatch import overload
from ...utilities import maybe
from ...desc import Field
from . import IntSample

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union

  MaybeFloat: TypeAlias = Optional[float]
  FloatField: TypeAlias = Union[float, Field]
  MaybeBool: TypeAlias = Optional[bool]
  BoolField: TypeAlias = Union[bool, Field]


class FloatSample(IntSample):
  """
  FloatSample subclasses 'IntSample' and provides 'float' samples.
  """
  #  Class Variables
  __mean_keys__ = 'mean', 'average', 'avg', 'mean_value', 'meanValue'
  __var_keys__ = 'variance', 'var', 'variance_value', 'varianceValue'
  __gauss_keys__ = 'gauss', 'gaussian', 'normal', 'gauss_flag', 'gaussFlag'
  __key_groups__: dict[str, tuple[str, ...]] = dict(
    **IntSample.__key_groups__,
    mean=__mean_keys__,
    variance=__var_keys__,
    gauss=__gauss_keys__,
    )
  __key_types__: dict[str, type] = dict(
    **IntSample.__key_types__,
    mean=float,
    variance=float,
    gauss=bool,
    )
  __key_defaults__: dict[str, Union[int, float]] = dict(
    **IntSample.__key_defaults__,
    mean=0.,
    variance=1.,
    gauss=False,
    )

  #  Fallback Variables
  __fallback_min__: float = 0.0
  __fallback_max__: float = 1.0
  __fallback_mean__: float = 0.
  __fallback_variance__: float = 1.0
  __fallback_gauss__: bool = False

  #  Private Variables
  __mean_val__: MaybeFloat = None
  __variance_val__: MaybeFloat = None
  __gauss_flag__: MaybeBool = None

  #  Public Variables
  mean: FloatField = Field()
  variance: FloatField = Field()
  gauss: BoolField = Field()

  #  Virtual Variables
  minVal = Field(IntSample.minVal)
  maxVal = Field(IntSample.maxVal)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @mean.GET
  def _getMean(self, **kwargs) -> float:
    if self.__mean_val__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createMean()
      return self._getMean(_recursion=True)
    return self.__mean_val__

  @variance.GET
  def _getVariance(self, **kwargs) -> float:
    if self.__variance_val__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createMean()
      return self._getVariance(_recursion=True)
    return self.__variance_val__

  def _createGauss(self, ) -> None:
    self.__gauss_flag__ = self.__fallback_gauss__

  @gauss.GET
  def _getGauss(self, **kwargs) -> bool:
    if self.__gauss_flag__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createGauss()
      return self._getGauss(_recursion=True)
    return self.__gauss_flag__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @gauss.SET
  def _setGauss(self, value: bool) -> None:
    self.__gauss_flag__ = value

  @mean.SET
  def _setMean(self, value: float) -> None:
    self.__mean_val__ = value

  @variance.SET
  def _setVariance(self, value: float) -> None:
    if value <= 0:
      infoSpec = """Received non-positive variance: '%f'!"""
      info = infoSpec % value
      raise ValueError(info)
    self.__variance_val__ = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createMean(self, ) -> None:
    """
    Sets mean to the fallback value.
    """
    self.__mean_val__ = self.__fallback_mean__

  def _createVariance(self, ) -> None:
    """
    Sets variance to the fallback value.
    """
    self.__variance_val__ = self.__fallback_variance__

  @minVal.onSet
  @maxVal.onSet
  def _update(self, value: int) -> None:
    """
    Sets the mean and variance based on the 'minVal' and 'maxVal' values.
    """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return float

  def _getItem(self, *args, **kwargs) -> float:
    """
    Returns a random float between 'minVal' and 'maxVal'.
    """
    if self.gauss:
      return normal(self.mean, self.variance ** 0.5)
    return random() * (self.maxVal - self.minVal) + self.minVal

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float, float, strict=True)
  def __init__(self, mean: float, variance: float, **kwargs) -> None:
    self.mean = mean
    self.variance = variance
    if kwargs:
      self.__init__(**kwargs)

  @overload(float, strict=True)
  def __init__(self, variance: float, **kwargs) -> None:
    if variance <= 0:
      infoSpec = """Received non-positive variance: '%f'!"""
      info = infoSpec % variance
      raise ValueError(info)
    self.variance = variance
    if kwargs:
      self.__init__(**kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    if kwargs:
      IntSample.__init__(self, **kwargs)
