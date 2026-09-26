"""
TestLoremSamplerSentence subclasses 'SamplerTest' and pins that every
'LoremSampler' draws from a 'Sentence' of its own. The 'charCount' of a
sampler is the 'charCount' of its sentence, so a shared sentence would
let one sampler resize the text of every other.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import Sentence
from worktoy.work_test.samplers import LoremSampler

from . import SamplerTest


class TestLoremSamplerSentence(SamplerTest):
  """
  TestLoremSamplerSentence provides tests for the 'Sentence' behind each
  'LoremSampler'.
  """

  def test_own_sentence(self) -> None:
    """Two samplers hold two distinct sentences."""
    first, second = LoremSampler(), LoremSampler()
    self.assertIsInstance(first.sentence, Sentence)
    self.assertIsNot(first.sentence, second.sentence)

  def test_char_count_stays_with_its_sampler(self) -> None:
    """Setting 'charCount' on one sampler leaves another at the default
    of 'Sentence'."""
    first, second = LoremSampler(), LoremSampler()
    first.charCount = 100
    self.assertEqual(first.charCount, 100)
    self.assertEqual(second.charCount, 40)

  def test_char_count_set_again(self) -> None:
    """Setting 'charCount' to the value it already has leaves the sampler
    and its sentence at that value."""
    sampler = LoremSampler()
    sampler.charCount = 100
    sampler.charCount = 100
    self.assertEqual(sampler.charCount, 100)
    self.assertEqual(sampler.sentence.charCount, 100)

  def test_char_count_reaches_the_sentence(self) -> None:
    """The 'charCount' of a sampler is that of its sentence, and each
    draw is a string."""
    sampler = LoremSampler()
    sampler.charCount = 100
    self.assertEqual(sampler.sentence.charCount, 100)
    for _ in range(8):
      self.assertIsInstance(sampler.item, str)
