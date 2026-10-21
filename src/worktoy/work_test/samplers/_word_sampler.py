"""
WordSampler draws random words.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import BaseSampler, randomWord

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  WordSampleTuple: TypeAlias = tuple[str, ...]
  WordSamplesTuple: TypeAlias = tuple[WordSampleTuple, ...]


class WordSampler(BaseSampler):
  """
  WordSampler draws single random words from 'LOREM_WORDS', the
  vocabulary of the 'worktoy.work_test.samplers' package.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return str

  def _getItem(self, *args, **kwargs) -> str:
    """
    The '_getItem' method draws one random word.
    """
    return randomWord()
