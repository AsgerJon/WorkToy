"""
GaussianLengths is a Gaussian 'StochasticVariable' clamped to a fixed
range.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import StochasticVariable
from ..desc import AttriBox
from ..utilities import textFmt


class GaussianLengths(StochasticVariable):
  """
  The clauses of a sentence and the sentences of a paragraph have no word
  list to take their lengths from, only a notion of how long they usually
  are and how much they vary. A generator must be able to state that in
  four numbers, a mean, a variance and two inclusive bounds, and get a
  'StochasticVariable' back without writing a subclass for each set of
  numbers.

  Implementation
  --------------

  The four statistics are boxes, 'AttriBox[float]' for the mean and the
  variance and 'AttriBox[int]' for the bounds, so an assignment is cast
  as a box casts, an 'int' widened to a 'float' and a text refused with
  'TypeException', and a project may retune a distribution it holds. The
  constructor writes the four and then refuses a mean outside the bounds
  and a negative variance with 'ValueError'. The draw is the base's.

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

  #  Public Variables
  mean = AttriBox[float]()
  var = AttriBox[float]()
  minVal = AttriBox[int]()
  maxVal = AttriBox[int]()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mean: float, var: float, minVal: int, maxVal: int):
    self.minVal = minVal
    self.maxVal = maxVal
    self.mean = mean
    self.var = var
    if not self.minVal <= self.mean <= self.maxVal:
      infoSpec = """Mean '%s' must lie within the bounds '[%s, %s]'!"""
      info = infoSpec % (self.mean, self.minVal, self.maxVal)
      raise ValueError(textFmt(info))
    if self.var < 0:
      infoSpec = """Variance must be non-negative, but received '%s'!"""
      raise ValueError(textFmt(infoSpec % (self.var,)))
