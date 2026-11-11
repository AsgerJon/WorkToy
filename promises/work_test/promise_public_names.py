"""
PromisePublicNames promises the names 'worktoy.work_test' exports.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

import worktoy.work_test
import worktoy.work_test.samplers


class PromisePublicNames(TestCase):
  """
  'BaseTest', 'SubTest', 'ComplexMixin', 'ComplexTest' and 'samplers'
  import from 'worktoy.work_test', and the samplers, 'BaseSampler',
  'SamplerMeta', 'LOREM_WORDS', 'randomWord' and 'loremSentence' from
  'worktoy.work_test.samplers'. Source: '__all__' of both packages.
  """

  def test_work_test(self) -> None:
    for name in ('samplers', 'SubTest', 'BaseTest', 'ComplexMixin',
                 'ComplexTest'):
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.work_test, name))

  def test_samplers(self) -> None:
    names = ('LOREM_WORDS', 'randomWord', 'loremSentence', 'SamplerMeta',
             'BaseSampler', 'IntSampler', 'FloatSampler', 'GaussianSampler',
             'SymbolicSampler', 'WordSampler', 'LoremSampler')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.work_test.samplers, name))
