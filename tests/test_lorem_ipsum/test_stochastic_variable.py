"""
TestStochasticVariable tests the abstract contract and the 'partition'
operation of 'StochasticVariable'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.lorem_ipsum import StochasticVariable, GaussianLengths
from . import LoremIpsumTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestStochasticVariable(LoremIpsumTest):
  """
  TestStochasticVariable checks that 'StochasticVariable' rejects an
  incomplete concrete subclass when the class is created, and that
  'partition' cuts a target into a list of in-bounds integers.
  """

  def test_missing_getter_rejected(self) -> None:
    """A subclass that leaves a statistics getter unimplemented is rejected
    when the class is created."""
    with self.assertRaises(TypeError):
      # noinspection PyUnusedLocal
      class Missing(StochasticVariable):
        _getMean = lambda *_: 0.
        #  _getVar, _getMinVal, _getMaxVal left unimplemented

  def test_non_callable_getter_rejected(self) -> None:
    """A subclass that binds a non-callable to a getter name is rejected."""
    with self.assertRaises(TypeError):
      # noinspection PyUnusedLocal
      class NotCallable(StochasticVariable):
        _getVar = lambda *_: 1.
        _getMinVal = lambda *_: 1
        _getMaxVal = lambda *_: 9
        sampleInteger = lambda *_: 5
        _getMean = 5  # not a method

  def test_concrete_subclass_accepted(self) -> None:
    """A subclass implementing all four getters is created without
    complaint and partitions correctly."""

    class Concrete(StochasticVariable):
      _getVar = lambda *_: 1.
      _getMinVal = lambda *_: 1
      _getMaxVal = lambda *_: 9
      sampleInteger = lambda *_: 5
      _getMean = lambda *_: 5

    self.assertEqual(sum(Concrete().partition(50)), 50)

  def test_partition_sums_to_target(self) -> None:
    """With the count taken from the mean, 'partition' reaches the target
    exactly."""
    dist = GaussianLengths(40, 15, 10, 70)
    for target in (100, 250, 400, 1000):
      self.assertEqual(sum(dist.partition(target)), target)

  def test_partition_in_bounds(self) -> None:
    """Every entry of a partition lies within the distribution bounds."""
    dist = GaussianLengths(40, 15, 10, 70)
    for value in dist.partition(400):
      self.assertGreaterEqual(value, 10)
      self.assertLessEqual(value, 70)
