"""
WordSampler subclasses 'BaseClass' and provides word samplers.
"""
#  AGPL-3.0 license
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
  WordSampler subclasses 'BaseClass' and provides word samplers.
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

  def _getItem(self, *args, **kwargs) -> WordSampleTuple:
    """
    Generates a word using the 'StochasticWord' class.
    """
    return self.stochWord.realize()
