"""
Span is a dataclass with bare-value fields and a '__post_init__'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData


class Span(EZData):
  """
  A bare value in the body becomes a field of its type, and
  '__post_init__' is the hook for validation and derived state. 'Span'
  swaps its ends when given backwards and records the length it
  derived in 'lengths', a plain attribute beside the fields.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fields
  start = 0
  stop = 0

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __post_init__(self) -> None:
    if self.stop < self.start:
      self.start, self.stop = self.stop, self.start
    self.length = self.stop - self.start
