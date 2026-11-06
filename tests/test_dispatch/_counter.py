"""
Counter is a worktoy class overloading a classmethod and a staticmethod.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject


class Counter(BaseObject):
  """
  An overloaded name may be a classmethod, as an alternative constructor
  taking several kinds of argument, or a staticmethod, with the kind
  written above or below '@overload'. 'Counter' declares one of each.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  @overload(int)
  def make(cls, n: int) -> tuple:
    return cls.__name__, 'int', n

  @overload(str)
  @classmethod
  def make(cls, s: str) -> tuple:
    return cls.__name__, 'str', s

  @staticmethod
  @overload(int, int)
  def add(a: int, b: int) -> int:
    return a + b
