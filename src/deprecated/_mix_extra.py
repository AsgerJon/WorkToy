"""
MixExtra classes set slots as both regular slots and typehints within the
same class body.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData

if TYPE_CHECKING:  # pragma: no cover
  pass


class MixExtra(EZData):
  """
  MixExtra provides a class that sets slots as both regular slots and
  typehints within the same class body.
  """

  a = 0
  b: int
  c = 0
  d: int


class MixExtra2(MixExtra):
  """
  MixExtra2 continues from MixExtra and adds more regular slots.
  """

  e = 0
  f: int
  g = 0
  h: int


class MixExtra3(MixExtra2):
  """
  MixExtra3 continues from MixExtra2 and adds more regular slots.
  """

  i = 0
  j: int
  k = 0
  l: int
