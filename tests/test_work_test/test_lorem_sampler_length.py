"""
TestLoremSamplerLength subclasses 'SamplerTest' and pins that a
'LoremSampler' serves the new length from the first draw after
'charCount' is assigned. The sentence behind it kept its cached layout
until a draw reset it, so one draw at the old length came first.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test.samplers import LoremSampler

from . import SamplerTest


class TestLoremSamplerLength(SamplerTest):
  """
  TestLoremSamplerLength provides tests for assigning 'charCount' to a
  'LoremSampler' between draws.
  """

  def test_next_draw_has_new_length(self) -> None:
    """The first draw after the assignment has the new length."""
    sampler = LoremSampler()
    sampler.charCount = 50
    self.assertEqual(len(sampler()), 50)
    sampler.charCount = 80
    self.assertEqual(len(sampler()), 80)
    self.assertEqual(len(sampler()), 80)
