"""
LoremSampler draws random lorem ipsum text.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...desc import Field
from ...lorem_ipsum import Sentence
from . import BaseSampler
from ...waitaminute.control_flow import SkipSet


class LoremSampler(BaseSampler):
  """
  LoremSampler draws random lorem ipsum sentences, each realized from a
  'Sentence' of the configured 'charCount'. The backing 'Sentence' is
  reset after every draw, so successive samples are independent rather
  than repeating one frozen sentence.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables

  #  Public Variables
  sentence = Sentence()

  #  Virtual Variables
  charCount: Field[int] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @charCount.GET
  def _getCharCount(self, ) -> int:
    return self.sentence.charCount

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @charCount.SET
  def _setCharCount(self, value: int, ) -> None:
    self.sentence.charCount = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @charCount.preSet
  def _preSetCharCount(self, value: int, ) -> None:
    if self.charCount == value:
      raise SkipSet

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return str

  def _getItem(self, *args, **kwargs) -> str:
    """
    The '_getItem' method realizes one sentence from the backing
    'Sentence', resetting it afterward so the next draw is independent.
    """
    try:
      return str(self.sentence)
    finally:
      self.sentence.reset()
