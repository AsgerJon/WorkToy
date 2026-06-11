"""
TestWordSampler subclasses 'SamplerTest' and provides tests for
'WordSampler' from the 'worktoy.work_test.samplers' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test.samplers import WordSampler
from . import SamplerTest


class TestWordSampler(SamplerTest):
  """
  TestWordSample provides tests for 'WordSampler' from the
  'worktoy.work_test.samplers' package.
  """

  def test_value_type(self, ) -> None:
    """
    Testing that the value type of the sampler is 'str'.
    """
    self.assertIs(WordSampler()._getValueType(), str)

  def test_get_item(self, ) -> None:
    """
    This method tests that '_getItem' realizes a tuple of words.
    """
    words = WordSampler()._getItem()
    for word in words:
      self.assertIsInstance(word, str)
