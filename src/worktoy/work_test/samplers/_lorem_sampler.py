"""
LoremSampler subclasses 'BaseSample' and provides lorem ipsum samplers.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...desc import Field
from ...lorem_ipsum import Sentence
from . import BaseSampler
from ...waitaminute.control_flow import SkipSet

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union

  IntField: TypeAlias = Union[int, Field]


class LoremSampler(BaseSampler):
  """
  LoremSampler subclasses 'BaseSample' and provides lorem ipsum samplers.
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
  charCount: IntField = Field()

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
    Generates a sentence using the 'Sentence' class.
    """
    try:
      return str(self.sentence)
    finally:
      self.sentence.reset()
