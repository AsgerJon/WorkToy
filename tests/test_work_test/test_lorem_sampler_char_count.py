"""
TestLoremSamplerCharCount subclasses 'SamplerTest' from
'tests.test_work_test' and pins that a 'LoremSampler' holds a 'charCount'
of its own, forty by default, that every draw has exactly that many
characters, and that a count below one is refused and leaves the sampler
as it was. The sampler used to delegate the count to a 'Sentence' of the
'lorem_ipsum' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test.samplers import LoremSampler

from . import SamplerTest


class TestLoremSamplerCharCount(SamplerTest):
  """
  TestLoremSamplerCharCount provides tests for the 'charCount' of a
  'LoremSampler'.
  """

  def test_default(self) -> None:
    """A fresh sampler has a count of forty and draws forty characters."""
    sampler = LoremSampler()
    self.assertEqual(sampler.charCount, 40)
    self.assertEqual(len(sampler()), 40)

  def test_own_char_count(self) -> None:
    """Setting the count on one sampler leaves another at the default,
    and each draws its own length."""
    first, second = LoremSampler(), LoremSampler()
    first.charCount = 100
    self.assertEqual(first.charCount, 100)
    self.assertEqual(second.charCount, 40)
    self.assertEqual(len(first()), 100)
    self.assertEqual(len(second()), 40)

  def test_refuses_non_positive(self) -> None:
    """A count below one is refused with 'ValueError' and the sampler
    keeps its count."""
    sampler = LoremSampler()
    sampler.charCount = 12
    for charCount in (0, -1):
      with self.assertRaises(ValueError):
        sampler.charCount = charCount
    self.assertEqual(sampler.charCount, 12)

  def test_every_sample_has_the_length(self) -> None:
    """Items, rows and tables all hold strings of the count."""
    sampler = LoremSampler()
    sampler.charCount = 23
    for value in self.rollSampler(sampler):
      self.assertIsInstance(value, str)
      self.assertEqual(len(value), 23)
