"""
MixedSlotClass provides a class that mixes between regular slots and slots
set as type hints.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import baseValues

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

from worktoy.ezdata import EZData


class Mix1(EZData):
  """
  Mix1 provides a class that mixes between regular slots and slots
  set as type hints.
  """

  # Regular slots
  a = 0
  b = 0
  c = 0


class Mix2(Mix1):
  """
  Mix2 continues from Mix1 and adds more regular slots.
  """

  # Regular slots
  d: int
  e: int
  f: int


class Mix3(Mix2):
  """
  Mix3 continues from Mix2 and adds more regular slots.
  """

  # Regular slots
  g = 0
  h = 0
  i = 0


class MixedSlot(Mix3):
  """
  MixedSlot provides a class that mixes between regular slots and slots
  set as type hints.
  """

  # Regular slots
  j: int
  k: int
  l: int
