"""
LoremSampler draws random lorem ipsum sentences.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...desc import AttriBox
from . import BaseSampler, loremSentence

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Any

  KeyGroups: TypeAlias = dict[str, tuple[str, ...]]


class LoremSampler(BaseSampler):
  """
  A test that needs text of a known length wants sentences of exactly
  that many characters. 'LoremSampler' draws random lorem ipsum
  sentences, each of exactly 'charCount' characters, forty unless set
  otherwise, built by 'loremSentence' from 'LOREM_WORDS'.

  Implementation
  --------------

  'charCount' is an 'AttriBox[int]' with the synonym 'chars' for the
  keyword constructor, held by each sampler apart, so narrowing one
  leaves every other at its own count; a 'preSet' notifier refuses a
  count below one with 'ValueError' as it is assigned. Each value is
  'loremSentence' drawing from 'self.random'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __key_groups__: KeyGroups = dict(
      charCount=('charCount', 'chars'),
  )

  #  Public Variables
  charCount = AttriBox[int](40)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @charCount.preSet
  def _refuseCharCount(self, value: Any) -> None:
    if isinstance(value, (int, float)) and value < 1:
      infoSpec = """Character count must be a positive integer, not %r!"""
      raise ValueError(infoSpec % (value,))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return str

  def _getItem(self, *args, **kwargs) -> str:
    return loremSentence(self.charCount, self.random)
