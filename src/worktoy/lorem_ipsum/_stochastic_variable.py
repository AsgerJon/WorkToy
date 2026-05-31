"""
StochasticVariable is the base class for the bounded integer distributions
that drive the 'lorem_ipsum' generators.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Callable
from random import shuffle
from typing import TYPE_CHECKING

from ..desc import Field
from ..mcls import BaseObject
from ..utilities import textFmt
from ..waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Optional


class StochasticVariable(BaseObject):
  """
  StochasticVariable is the base class for a bounded distribution over the
  integers. A subclass states its statistics, the mean, the variance, and
  the inclusive bounds, and says how to draw one value; this base class
  turns that into the shared operation the generators need: cutting a
  target total into a list of plausible integers.

  A subclass supplies four read accessors and one sampler:

  - 'mean', 'var', 'minVal', 'maxVal' are 'Field' getters left empty here
    and required of every concrete subclass. 'StochasticWord' computes
    them from the histogram of its word list; 'GaussianLengths' takes them
    as construction arguments.
  - 'sampleInteger' draws a single value, which must land within the
    bounds.

  On top of those, 'partition' produces a list of integers summing to a
  given target, each one a sample, by choosing a count from the mean (so
  the target always falls inside the reachable band), then nudging the
  integers to land exactly on the target.
  """
  
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  
  #  Class Variables
  __required_fields__ = ('mean', 'var', 'minVal', 'maxVal')
  
  #  Public Variables
  mean: Field[float] = Field()
  var: Field[float] = Field()
  minVal: Field[int] = Field()
  maxVal: Field[int] = Field()
  
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  
  @mean.GET
  def _getMean(self) -> float:
    """
    The 'mean' getter, which each concrete subclass implements, returns the
    mean of the distribution.

    Returns
    -------
    float
      The mean of the distribution.
    """

  @var.GET
  def _getVar(self) -> float:
    """
    The 'var' getter, which each concrete subclass implements, returns the
    variance of the distribution.

    Returns
    -------
    float
      The variance of the distribution.
    """

  @minVal.GET
  def _getMinVal(self) -> int:
    """
    The 'minVal' getter, which each concrete subclass implements, returns
    the lowest value the distribution may produce.

    Returns
    -------
    int
      The lowest value the distribution may produce.
    """

  @maxVal.GET
  def _getMaxVal(self) -> int:
    """
    The 'maxVal' getter, which each concrete subclass implements, returns
    the highest value the distribution may produce.

    Returns
    -------
    int
      The highest value the distribution may produce.
    """
  
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  
  @classmethod
  def __class_init__(cls, name: str, bases, space, **kwargs) -> None:
    """
    The '__class_init__' method rejects a concrete subclass that left a
    statistics getter on the abstract base, or that bound something not
    callable to one. The
    base class subclasses 'BaseObject' directly and declares those empty
    getters, so it is exempt, while its subclasses are reached up the MRO.

    Parameters
    ----------
    name : str
      The name given to the subclass being created.
    bases : tuple[type, ...]
      The base classes of the subclass being created.
    space : BaseSpace
      The prepared namespace of the class body.

    Raises
    ------
    TypeError
      If a required statistics getter still resolves to the empty one
      declared on the abstract base.
    TypeException
      If a getter name is bound to something that is not callable.
    """
    if BaseObject in bases:
      return
    baseClass = cls
    for klass in cls.__mro__:
      if BaseObject in klass.__bases__:
        baseClass = klass
        break
    for fieldName in cls.__required_fields__:
      getterKey = getattr(baseClass, fieldName).__get_key__
      found = getattr(cls, getterKey)
      original = getattr(baseClass, getterKey)
      if found is original:
        infoSpec = """Class '%s' must implement the getter for the '%s'
        field; it still resolves to the empty one on '%s'."""
        info = infoSpec % (name, fieldName, baseClass.__name__)
        raise TypeError(textFmt(info))
      if not callable(found):
        raise TypeException(getterKey, found, Callable)
  
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  
  def sampleInteger(self) -> int:
    """
    The 'sampleInteger' method is left abstract on the base and implemented
    by each concrete subclass to draw a single value from the distribution.

    Returns
    -------
    int
      A single value drawn from the distribution, landing within the
      bounds.

    Raises
    ------
    NotImplementedError
      Always, on the abstract base, since a concrete subclass must supply
      the draw.
    """
    raise NotImplementedError
  
  def _settle(self, values: list[int], target: int) -> list[int]:
    """
    The '_settle' method distributes the difference between 'target' and the
    sum of 'values' across the values in random order, clamping each to the
    bounds.
    It runs one pass, so it cannot spin, and an unreachable target lands as
    near as the bounds allow.

    Parameters
    ----------
    values : list[int]
      The samples to adjust toward the target sum.
    target : int
      The sum the values should reach.

    Returns
    -------
    list[int]
      The same list, adjusted toward summing to 'target'.
    """
    delta = target - sum(values)
    order = [*range(len(values))]
    shuffle(order)
    for i in order:
      if not delta:
        break
      adjusted = min(self.maxVal, max(self.minVal, values[i] + delta))
      delta -= adjusted - values[i]
      values[i] = adjusted
    return values

  def partition(self, target: int) -> list[int]:
    """
    The 'partition' method produces a list of integers summing to 'target',
    each one a sample from the distribution. It draws a count of samples
    taken from the
    mean, finds the single difference between their sum and 'target', then
    distributes that difference across the values in random order, clamping
    each to the bounds. One pass settles the sum, so an unreachable target
    lands as near as the bounds allow rather than spinning in a loop.

    Parameters
    ----------
    target : int
      The total the returned integers must sum to.

    Returns
    -------
    list[int]
      Integers, each within the bounds, summing to 'target' when the bounds
      allow and as near as possible otherwise.
    """
    count = round(target / self.mean) or 1
    values = [self.sampleInteger() for _ in range(count)]
    return self._settle(values, target)

  def partitionSpaced(self, target: int) -> list[int]:
    """
    The 'partitionSpaced' method mirrors 'partition' but reserves one extra
    slot per integer, as a word followed by a single separator does, so that
    the sum of the
    integers plus their count equals 'target'. A list joined by one
    character separators therefore reaches 'target' characters exactly. Each
    integer costs its value plus that one slot, so the count is taken from
    'mean + 1' and the values are settled to sum to 'target' minus the
    count.

    Parameters
    ----------
    target : int
      The total of the integers plus their count.

    Returns
    -------
    list[int]
      Integers, each within the bounds, with 'sum(out) + len(out)' equal to
      'target' when the bounds allow and as near as possible otherwise.
    """
    count = round(target / (self.mean + 1)) or 1
    values = [self.sampleInteger() for _ in range(count)]
    return self._settle(values, target - count)
