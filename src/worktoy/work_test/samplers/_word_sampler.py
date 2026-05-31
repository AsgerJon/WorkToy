"""
WordSampler draws random words.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...lorem_ipsum import StochasticWord
from . import BaseSampler

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  WordSampleTuple: TypeAlias = tuple[str, ...]
  WordSamplesTuple: TypeAlias = tuple[WordSampleTuple, ...]


class WordSampler(BaseSampler):
  """
  WordSampler draws single random words, each realized from the
  'StochasticWord' distribution shared with 'lorem_ipsum'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables

  #  Public Variables
  stochWord = StochasticWord()

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return str

  def _getItem(self, *args, **kwargs) -> str:
    """
    The '_getItem' method realizes one random word from the
    'StochasticWord' distribution.
    """
    return self.stochWord.realize()
