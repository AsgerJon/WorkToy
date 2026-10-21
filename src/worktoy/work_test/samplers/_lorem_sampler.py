"""
LoremSampler draws random lorem ipsum sentences.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...desc import AttriBox
from . import BaseSampler, loremSentence


class LoremSampler(BaseSampler):
  """
  LoremSampler draws random lorem ipsum sentences, each of exactly
  'charCount' characters, forty unless set otherwise, built by
  'loremSentence' from 'LOREM_WORDS'. Each sampler holds a 'charCount' of
  its own, so narrowing one leaves every other at its own count. A count
  below one is refused with 'ValueError' as it is assigned.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  charCount = AttriBox[int](40)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @charCount.preSet
  def _refuseCharCount(self, value: int) -> None:
    if value < 1:
      infoSpec = """Character count must be a positive integer, not %r!"""
      raise ValueError(infoSpec % (value,))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return str

  def _getItem(self, *args, **kwargs) -> str:
    """
    The '_getItem' method draws one sentence of 'charCount' characters.
    """
    return loremSentence(self.charCount)
