"""
RefusedSamplers holds the refusals that belong with
'design.promises.work_test.promise_samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.work_test.samplers import BaseSampler, IntSampler


class RefusedSamplers(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A size below one raises 'ValueError'. A keyword naming no
  setting raises 'TypeError'. Source: the docstrings of the 'samplers'
  package, 'BaseSampler', 'IntSampler' and 'SamplerMeta'.
  """

  def test_shapes(self) -> None:
    sampler = IntSampler(1, 6, width=4, height=3)
    with self.assertRaises(Exception) as refused:
      IntSampler(1, 6, count=0)
    self.assertIsInstance(refused.exception, ValueError)

  def test_unknown_keyword(self) -> None:
    with self.assertRaises(Exception) as refused:
      IntSampler(1, 6, colour='red')
    self.assertIsInstance(refused.exception, TypeError)

  def test_own_sampler(self) -> None:
    class DieSampler(BaseSampler):
      sides = AttriBox[int](6)

      def _getValueType(self, **kwargs) -> type:
        return int

      def _getItem(self, *args, **kwargs) -> int:
        return self.random.randint(1, self.sides)

    class Broken(BaseSampler):
      pass

    die = DieSampler(seed=3)
    die.sides = 20
    with self.assertRaises(Exception) as refused:
      Broken()
    self.assertIsInstance(refused.exception, TypeError)
