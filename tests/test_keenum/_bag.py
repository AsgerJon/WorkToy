"""
Bag is an enumeration whose values are lists, which do not hash.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class Bag(KeeNum):
  """
  A member hashes where its value hashes, and an enumeration of values
  that do not hash resolves them by comparing one by one. 'Bag' holds
  three lists, two of them equal, so the lowest-indexed member answers
  for the shared value.
  """

  FEW = Kee[list]([1])
  MANY = Kee[list]([1, 2, 3])
  SAME = Kee[list]([1])
