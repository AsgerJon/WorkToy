"""
Tally is a worktoy class with variadic overloads beside a concrete one.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject


class Tally(BaseObject):
  """
  A concrete signature wins the call it declares exactly, while a
  variadic one takes every other length. 'Tally' adds two integers as a
  pair, any number of integers, or any number behind a label.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int, int)
  def add(self, a: int, b: int) -> tuple:
    return 'pair', a + b

  @overload(ARGS[int])
  def add(self, *numbers: int) -> tuple:
    return 'ints', sum(numbers)

  @overload(str, ARGS[int])
  def add(self, label: str, *numbers: int) -> tuple:
    return label, sum(numbers)
