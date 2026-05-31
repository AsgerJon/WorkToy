"""
GaussianLengths is a Gaussian 'StochasticVariable' clamped to a fixed
range.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from math import sqrt
from random import gauss
from typing import TYPE_CHECKING

from . import StochasticVariable
from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class GaussianLengths(StochasticVariable):
  """
  GaussianLengths is a 'StochasticVariable' whose values follow a Gaussian
  distribution of a given mean and variance, with every draw clamped to
  '[minVal, maxVal]'. The four statistics are passed to the constructor,
  so 'Clause', 'Sentence', and 'Paragraph' each hold one of these
  parametrised with their own numbers rather than each needing a subclass.

  This is the minimal concrete implementation of the abstract base: it
  fills the four statistics getters and the sampler. The fuller worktoy
  treatment, where the statistics are descriptor-backed attributes, comes
  later.

  Parameters
  ----------
  mean : float
    The mean of the Gaussian, which must lie within '[minVal, maxVal]'.
  var : float
    The variance of the Gaussian, which must not be negative.
  minVal : int
    The lowest value any draw is clamped to.
  maxVal : int
    The highest value any draw is clamped to.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __mean__ = None
  __var__ = None
  __min_val__ = None
  __max_val__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getMean(self) -> float:
    return self.__mean__

  def _getVar(self) -> float:
    return self.__var__

  def _getMinVal(self) -> int:
    return self.__min_val__

  def _getMaxVal(self) -> int:
    return self.__max_val__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mean: float, var: float, minVal: int, maxVal: int):
    if not minVal <= mean <= maxVal:
      infoSpec = """Mean '%s' must lie within the bounds '[%s, %s]'!"""
      raise ValueError(textFmt(infoSpec % (mean, minVal, maxVal)))
    if var < 0:
      infoSpec = """Variance must be non-negative, but received '%s'!"""
      raise ValueError(textFmt(infoSpec % (var,)))
    self.__mean__ = float(mean)
    self.__var__ = float(var)
    self.__min_val__ = int(minVal)
    self.__max_val__ = int(maxVal)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def sampleInteger(self) -> int:
    """
    The 'sampleInteger' method draws one Gaussian value of the stored mean
    and variance and clamps it into the inclusive bounds.

    Returns
    -------
    int
      A Gaussian draw clamped to '[minVal, maxVal]'.
    """
    value = round(gauss(self.mean, sqrt(self.var)))
    return min(self.maxVal, max(self.minVal, value))
