"""
Cheat is a sampler drawing values of another type than it declares.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test.samplers import BaseSampler, randomWord


class Cheat(BaseSampler):
  """
  'row' promises that every value it hands out is of the sampler's value
  type, and a sampler whose recipe breaks that promise must be caught
  there. 'Cheat' declares 'int' and draws a word, so its first row is
  the refusal the tests pin.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return int

  def _getItem(self, *args, **kwargs) -> str:
    return randomWord(self.random)
