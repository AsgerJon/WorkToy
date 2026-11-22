"""
RefusedDistributions holds the refusals that belong with
'design.promises.lorem_ipsum.promise_distributions'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.lorem_ipsum import GaussianLengths
from worktoy.waitaminute import TypeException


class RefusedDistributions(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A mean outside the bounds or a negative variance raises
  'ValueError'. A total no count of values can reach raises 'ValueError'.
  Source: the docstrings of 'StochasticVariable', 'GaussianLengths',
  'Sentence' and 'Paragraph'.
  """

  def test_statistics(self) -> None:
    lengths = GaussianLengths(40, 15, 12, 70)
    with self.assertRaises(Exception) as refused:
      lengths.mean = 'forty'
    self.assertIsInstance(refused.exception, TypeException)

  def test_refusals_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      GaussianLengths(100, 15, 12, 70)
    self.assertIsInstance(refused.exception, ValueError)

  def test_refusals_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      GaussianLengths(40, -1, 12, 70)
    self.assertIsInstance(refused.exception, ValueError)

  def test_unreachable(self) -> None:
    with self.assertRaises(Exception) as refused:
      GaussianLengths(40, 15, 12, 70).partition(5)
    self.assertIsInstance(refused.exception, ValueError)
