"""
Clock is a worktoy class that is its own iterator.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Clock(BaseObject):
  """
  A class acting as its own iterator returns itself from '__class_iter__'
  and hands out items from '__class_next__' until it raises
  'StopIteration'. 'Clock' hands out the front of 'ticks' at each step.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  ticks: list = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CLASS HOOKS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_iter__(cls) -> type:
    return cls

  @classmethod
  def __class_next__(cls) -> Any:
    if cls.ticks:
      return cls.ticks.pop(0)
    raise StopIteration
