"""
TestLoremSample subclasses 'SampleTest' and provides tests for
'LoremSample' from the 'worktoy.work_test.samplers' module.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test.samplers import LoremSampler
from . import SamplerTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestLoremSampler(SamplerTest):
  """
  TestLoremSample provides tests for 'LoremSample' from the
  'worktoy.work_test.samplers' module.
  """

  def test_value_type(self, ) -> None:
    """
    Test that the value type of the sampler is 'str'.
    """
    self.assertIs(LoremSampler()._getValueType(), str)

  def test_get_item(self, ) -> None:
    """
    Test that the get item method of the sampler returns a string.
    """
    self.assertIsInstance(LoremSampler()._getItem(), str)
