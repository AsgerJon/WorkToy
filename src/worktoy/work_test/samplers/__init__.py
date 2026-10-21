"""
The 'worktoy.work_test.samplers' package provides random sample-data
generators for the test suite. 'BaseSampler' defines the shared shape, a
value type plus a single-sample recipe sized into items, rows, and
tables; each concrete sampler fills in one data type.

- LOREM_WORDS, randomWord, loremSentence
- BaseSampler
- IntSampler
- FloatSampler
- GaussianSampler
- SymbolicSampler
- WordSampler
- LoremSampler
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._lorem_text import LOREM_WORDS, randomWord, loremSentence
from ._base_sampler import BaseSampler
from ._int_sampler import IntSampler
from ._float_sampler import FloatSampler
from ._gaussian_sampler import GaussianSampler
from ._symbolic_sampler import SymbolicSampler
from ._word_sampler import WordSampler
from ._lorem_sampler import LoremSampler

__all__ = [
  'LOREM_WORDS',
  'randomWord',
  'loremSentence',
  'BaseSampler',
  'IntSampler',
  'FloatSampler',
  'GaussianSampler',
  'SymbolicSampler',
  'WordSampler',
  'LoremSampler',
]
