"""
WordSampler draws random words.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import BaseSampler, randomWord


class WordSampler(BaseSampler):
  """
  A test that needs short strings wants real words rather than random
  letters. 'WordSampler' draws single random words from 'LOREM_WORDS',
  the vocabulary of the 'worktoy.work_test.samplers' package.

  Implementation
  --------------

  The value type is 'str' and each value is 'randomWord' drawing from
  'self.random'. The sampler has no setting of its own, so the keyword
  constructor of the base takes the counts and the seed alone.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return str

  def _getItem(self, *args, **kwargs) -> str:
    return randomWord(self.random)
