"""
VAlignum example test.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class VAlignum(KeeNum):
  """
  VAlignum enumerates vertical alignments.
  """

  TOP = Kee[int](0)
  CENTER = Kee[int](1)
  BOTTOM = Kee[int](2)
