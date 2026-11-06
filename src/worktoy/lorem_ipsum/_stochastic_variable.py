"""
StochasticVariable is the base class for the bounded integer distributions
that drive the 'lorem_ipsum' generators.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from math import sqrt
from random import gauss, shuffle

from ..mcls import BaseObject
from ..utilities import textFmt


class StochasticVariable(BaseObject):
  """
  A lorem ipsum generator needs integers that add up: word lengths that
  fill a clause, clause lengths that fill a sentence, sentence lengths
  that fill a paragraph, each drawn from a distribution so the text looks
  natural, and together meeting the requested count exactly. The
  distributions differ, a Gaussian for the lengths of clauses and
  sentences and the histogram of a word list for the lengths of words,
  so the cutting of a total into plausible parts must be written once,
  over what any distribution can say about itself: its mean, its
  variance, its inclusive bounds, and one way to draw a value.

  Implementation
  --------------

  The base declares nothing for the four statistics: a subclass holds
  'mean', 'var', 'minVal' and 'maxVal' however it likes, 'GaussianLengths'
  in boxes written by its constructor, 'StochasticWord' in class
  attributes its class statement computes, and a subclass without them
  fails where it reads them with Python's own 'AttributeError'.
  'sampleInteger' rounds one 'random.gauss' draw of the mean and the
  standard deviation and clamps it into the bounds; a subclass may draw
  otherwise. 'partitionSpaced' chooses through '_countFor' how many
  values to draw, the count the mean suggests held between the fewest and
  the most that can add up to the target, each value costing 'spacing'
  slots beyond itself, and refuses a target no count can reach with
  'ValueError'; 'partition' is the same with no spacing. '_settle' moves
  the drawn values onto the target: '_spread' gives each its share of
  the difference in a shuffled order, clamped, and '_fill' hands what the
  clamps left to the values in the same order.

  Attributes
  ----------
  mean : float
    The mean of the distribution, held by the subclass.
  var : float
    The variance of the distribution, held by the subclass.
  minVal : int
    The lowest value a draw may give, held by the subclass.
  maxVal : int
    The highest value a draw may give, held by the subclass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def sampleInteger(self) -> int:
    """
    The 'sampleInteger' method draws one value from a Gaussian of the mean
    and the variance, rounded and clamped into the inclusive bounds.

    Returns
    -------
    int
      A Gaussian draw clamped to '[minVal, maxVal]'.
    """
    return self._clamp(round(gauss(self.mean, sqrt(self.var))))

  def _clamp(self, value: int) -> int:
    return min(self.maxVal, max(self.minVal, value))

  def _spread(self, values: list[int], order: list[int], delta: int) -> int:
    """
    The '_spread' method moves each value, in the given order, by its share
    of what is left of 'delta', each clamped to the bounds, so the values
    stay near what was drawn. It returns what the clamps left over.
    """
    for n, i in enumerate(order):
      if not delta:
        break
      share = round(delta / (len(order) - n))
      adjusted = self._clamp(values[i] + share)
      delta -= adjusted - values[i]
      values[i] = adjusted
    return delta

  def _fill(self, values: list[int], order: list[int], delta: int) -> int:
    """
    The '_fill' method gives each value, in the given order, as much of
    'delta' as its bounds allow, and returns what is left over: nothing,
    when the target lies within what the bounds allow.
    """
    for i in order:
      if not delta:
        break
      adjusted = self._clamp(values[i] + delta)
      delta -= adjusted - values[i]
      values[i] = adjusted
    return delta

  def _settle(self, values: list[int], target: int) -> list[int]:
    """
    The '_settle' method moves 'values' onto the sum 'target': the
    difference is spread over the values in random order, each taking its
    share, and what the clamps leave is filled in the same order. Two
    passes, so it cannot spin; the sum is exact whenever the target lies
    between the count times each bound.

    Parameters
    ----------
    values : list[int]
      The samples to adjust toward the target sum.
    target : int
      The sum the values should reach.

    Returns
    -------
    list[int]
      The same list, adjusted to sum to 'target'.
    """
    delta = target - sum(values)
    order = [*range(len(values))]
    shuffle(order)
    delta = self._spread(values, order, delta)
    self._fill(values, order, delta)
    return values

  def _countFor(self, target: int, spacing: int) -> int:
    """
    The '_countFor' method chooses how many values to draw for 'target',
    each costing its value plus 'spacing': the count the mean suggests,
    held between the fewest and the most values that can add up to the
    target. A target no count can reach is refused.

    Raises
    ------
    ValueError
      If no number of values within the bounds adds up to 'target'.
    """
    if target == 0:
      return 0
    low = self.minVal + spacing
    high = self.maxVal + spacing
    spacedMean = self.mean + spacing
    if spacedMean > 0:
      preferred = round(target / spacedMean)
    else:
      preferred = 0
    if target > 0 and high > 0:
      fewest = -(-target // high)
      if low > 0:
        most = target // low
      else:
        most = max(fewest, preferred)
    else:
      #  This branch is reached by the following:
      #  - The target is negative, which no values at or above zero add
      #    up to.
      #  - Every value is at most zero, so no positive target is reached.
      fewest, most = 1, 0
    if fewest > most:
      infoSpec = """A '%s' cannot cut %d into values from %d to %d%s: no
      number of such values adds up to it!"""
      if spacing:
        spacingStr = """, each with %d more for its separator""" % spacing
      else:
        spacingStr = ''
      args = (type(self).__name__, target, self.minVal, self.maxVal)
      raise ValueError(textFmt(infoSpec % (*args, spacingStr)))
    return min(most, max(fewest, preferred))

  def partition(self, target: int) -> list[int]:
    """
    The 'partition' method produces a list of integers summing to 'target'
    exactly, each one a sample from the distribution: as many samples as
    the mean suggests, held to a count that can reach the target, then
    settled onto it.

    Parameters
    ----------
    target : int
      The total the returned integers must sum to.

    Returns
    -------
    list[int]
      Integers, each within the bounds, summing to 'target'; none for a
      target of zero.

    Raises
    ------
    ValueError
      If no number of values within the bounds adds up to 'target'.
    """
    return self.partitionSpaced(target, 0)

  def partitionSpaced(self, target: int, spacing: int = 1) -> list[int]:
    """
    The 'partitionSpaced' method is 'partition' with 'spacing' extra slots
    reserved per integer, as a word followed by a separator costs its
    letters and one more, so that the sum of the integers plus 'spacing'
    times their count equals 'target' exactly.

    Parameters
    ----------
    target : int
      The total of the integers plus 'spacing' per integer.
    spacing : int, optional
      The slots each integer costs beyond its value, one unless given.

    Returns
    -------
    list[int]
      Integers, each within the bounds, with 'sum(out) + spacing *
      len(out)' equal to 'target'; none for a target of zero.

    Raises
    ------
    ValueError
      If no number of values within the bounds, each plus 'spacing', adds
      up to 'target'.
    """
    count = self._countFor(target, spacing)
    values = [self.sampleInteger() for _ in range(count)]
    return self._settle(values, target - spacing * count)
