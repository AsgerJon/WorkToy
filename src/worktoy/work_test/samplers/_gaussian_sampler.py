"""
GaussianSampler draws normally distributed random numbers.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from cmath import isfinite
from typing import TYPE_CHECKING
from random import gauss

from ...desc import Field
from ...dispatch import overload
from ...utilities import typeCast, textFmt
from ...waitaminute import TypeException
from ...waitaminute.dispatch import TypeCastException
from . import BaseSampler

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional

  MaybeFloat: TypeAlias = Optional[float]


class GaussianSampler(BaseSampler):
  """
  GaussianSampler draws normally distributed random floats with a given
  'mean' and 'stdDev', defaulting to the standard normal (mean 0.0,
  standard deviation 1.0). Both parameters accept synonym spellings and
  are validated as finite, with 'stdDev' additionally required to be
  non-negative.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables
  __fallback_mean__: float = 0.
  __fallback_std_dev__: float = 1.0

  #  Namespace
  __mean_keys__ = ('mean', 'average', 'avg', 'mean_value', 'meanValue')
  __std_dev_keys__ = (
    'stdDev',
    'std_dev',
    'stdDeviation',
    'std_deviation',
    'stdDevValue',
    'std_dev_value',
    'stdDeviationValue',
  )
  __key_groups__: dict[str, tuple[str, ...]] = dict(
    mean=__mean_keys__,
    stdDev=__std_dev_keys__,
  )
  __key_types__: dict[str, type] = dict(
    mean=float,
    stdDev=float,
  )
  __key_defaults__: dict[str, float] = dict(
    mean=__fallback_mean__,
    stdDev=__fallback_std_dev__,
  )

  #  Private Variables
  __mean_value__: MaybeFloat = None
  __std_dev__: MaybeFloat = None

  #  Public Variables
  mean: Field[float] = Field()
  stdDev: Field[float] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @mean.GET
  def _getMean(self, **kwargs) -> float:
    if self.__mean_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__mean_value__ = self.__fallback_mean__
      return self._getMean(_recursion=True)
    if isinstance(self.__mean_value__, (int, float)):
      return self.__mean_value__
    name, value = '__mean_value__', self.__mean_value__
    raise TypeException(name, value, float)

  @stdDev.GET
  def _getStdDev(self, **kwargs) -> float:
    if self.__std_dev__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__std_dev__ = self.__fallback_std_dev__
      return self._getStdDev(_recursion=True)
    if isinstance(self.__std_dev__, (int, float)):
      return self.__std_dev__
    name, value = '__std_dev__', self.__std_dev__
    raise TypeException(name, value, float)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @mean.SET
  def _setMean(self, mean: float) -> None:
    if not isinstance(mean, (int, float)):
      try:
        casted = typeCast(float, mean, )
      except TypeCastException as typeCastException:
        raise TypeException('mean', mean, float) from typeCastException
      else:
        return self._setMean(casted)
    if not isfinite(mean):
      infoSpec = """Mean must be a finite number, but received: '%s'!"""
      info = infoSpec % mean
      raise ValueError(textFmt(info))
    return setattr(self, '__mean_value__', mean)

  @stdDev.SET
  def _setStdDev(self, stdDev: float) -> None:
    if not isinstance(stdDev, (int, float)):
      try:
        casted = typeCast(float, stdDev, )
      except TypeCastException as typeCastException:
        raise TypeException('stdDev', stdDev, float) from typeCastException
      else:
        return self._setStdDev(casted)
    if not isfinite(stdDev):
      infoSpec = """Standard deviation must be a finite number, 
      but received: '%s'!"""
      info = infoSpec % stdDev
      raise ValueError(textFmt(info))
    if stdDev < 0:
      infoSpec = """Standard deviation must be a non-negative number, 
      but received: '%s'!"""
      info = infoSpec % stdDev
      raise ValueError(textFmt(info))
    return setattr(self, '__std_dev__', stdDev)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self) -> str:
    infoSpec = """<%s (mean: %f, stdDev: %f)>"""
    info = infoSpec % (type(self).__name__, self.mean, self.stdDev)
    return textFmt(info)

  def __repr__(self, ) -> str:
    infoSpec = """%s(%f, %f)"""
    info = infoSpec % (type(self).__name__, self.mean, self.stdDev)
    return textFmt(info)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float, float)
  def __init__(self, mean: float, stdDev: float, **kwargs) -> None:
    self.mean = mean
    self.stdDev = stdDev
    if kwargs:
      self.__init__(**kwargs)

  @overload(float, )
  def __init__(self, mean: float, **kwargs) -> None:
    self.mean = mean
    if kwargs:
      self.__init__(**kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    if kwargs:
      BaseSampler.__init__(self, **kwargs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return float

  def _getItem(self, *args, **kwargs) -> float:
    """
    The '_getItem' method draws one float from a normal distribution with
    mean 'mean' and standard deviation 'stdDev'.
    """
    return gauss(self.mean, self.stdDev)
