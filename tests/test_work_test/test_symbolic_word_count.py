"""
TestSymbolicWordCount subclasses 'SamplerTest' and pins that
'SymbolicSampler' refuses a word count below one with 'ValueError', as the
column and row counts of every sampler do. A count of zero drew names of
no words, and a negative count did too.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test.samplers import SymbolicSampler

from . import SamplerTest


class TestSymbolicWordCount(SamplerTest):
  """
  TestSymbolicWordCount provides tests for the word count of
  'SymbolicSampler'.
  """

  def test_constructor_refuses(self) -> None:
    """Zero and negative counts raise, by position and by keyword."""
    for count in (0, -2):
      with self.subTest(count=count):
        with self.assertRaises(ValueError):
          SymbolicSampler(count)
        with self.assertRaises(ValueError):
          SymbolicSampler(wordCount=count)

  def test_assignment_refused(self) -> None:
    """Assigning zero raises and keeps the count the sampler had."""
    sampler = SymbolicSampler()
    with self.assertRaises(ValueError):
      sampler.wordCount = 0
    self.assertEqual(sampler.wordCount, 3)

  def test_one_allowed(self) -> None:
    """A single word is a name."""
    sampler = SymbolicSampler(1)
    self.assertEqual(sampler.wordCount, 1)
    self.assertEqual(len(sampler()), 1)
