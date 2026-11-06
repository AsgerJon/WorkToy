"""
GaussianSampler draws normally distributed random numbers.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from math import isfinite
from typing import TYPE_CHECKING

from ...desc import AttriBox
from ...dispatch import overload
from ...utilities import textFmt
from . import BaseSampler

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Any

  KeyGroups: TypeAlias = dict[str, tuple[str, ...]]


class GaussianSampler(BaseSampler):
  """
  A test that needs numbers clustered around a value wants to name the
  centre and the spread and nothing else. 'GaussianSampler' draws
  normally distributed random floats with a given 'mean' and 'stdDev',
  the standard normal unless set otherwise.

  Implementation
  --------------

  'mean' and 'stdDev' are 'AttriBox[float]' with '0.0' and '1.0', each
  with synonyms for the keyword constructor ('average', 'avg',
  'mean_value', 'meanValue'; 'std_dev', 'stdDeviation',
  'std_deviation', 'stdDevValue', 'std_dev_value', 'stdDeviationValue').
  A 'preSet' notifier refuses a mean or a deviation that is not finite,
  and a negative deviation, with 'ValueError' before the box stores it;
  a value that is no number is left to the box, which casts or refuses
  it. The positional constructors take the mean and the deviation, or
  the mean alone. Each value is 'self.random.gauss'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __key_groups__: KeyGroups = dict(
      mean=('mean', 'average', 'avg', 'mean_value', 'meanValue'),
      stdDev=(
        'stdDev',
        'std_dev',
        'stdDeviation',
        'std_deviation',
        'stdDevValue',
        'std_dev_value',
        'stdDeviationValue',
      ),
  )

  #  Public Variables
  mean = AttriBox[float](0.0)
  stdDev = AttriBox[float](1.0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @mean.preSet
  def _refuseMean(self, value: Any) -> None:
    if isinstance(value, (int, float)) and not isfinite(value):
      infoSpec = """Mean must be a finite number, but received: '%s'!"""
      raise ValueError(textFmt(infoSpec % value))

  @stdDev.preSet
  def _refuseStdDev(self, value: Any) -> None:
    if not isinstance(value, (int, float)):
      #  This branch is reached by the following:
      #  - The value is no number; the box casts or refuses it
      return
    if not isfinite(value):
      infoSpec = """Standard deviation must be a finite number, 
      but received: '%s'!"""
      raise ValueError(textFmt(infoSpec % value))
    if value < 0:
      infoSpec = """Standard deviation must be a non-negative number, 
      but received: '%s'!"""
      raise ValueError(textFmt(infoSpec % value))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self) -> str:
    infoSpec = """<%s (mean: %f, stdDev: %f)>"""
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
    BaseSampler.__init__(self, **kwargs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return float

  def _getItem(self, *args, **kwargs) -> float:
    return self.random.gauss(self.mean, self.stdDev)
