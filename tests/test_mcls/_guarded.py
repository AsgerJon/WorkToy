"""
Guarded is a worktoy class that records every attribute written to it or
deleted from it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Guarded(BaseObject):
  """
  A class may watch its own attributes through '__class_setattr__' and
  '__class_delattr__', which then perform the operation themselves with
  the methods of 'type'. 'Guarded' records each write in 'writes' and
  each deletion in 'deletes'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  writes: list = []
  deletes: list = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CLASS HOOKS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_setattr__(cls, name: str, value: Any) -> None:
    cls.writes.append((name, value))
    type.__setattr__(cls, name, value)

  @classmethod
  def __class_delattr__(cls, name: str) -> None:
    cls.deletes.append(name)
    type.__delattr__(cls, name)
