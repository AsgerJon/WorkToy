"""
HAlignum enumerates horizontal alignments.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class HAlignum(KeeNum):
  """
  HAlignum enumerates horizontal alignments.
  """

  LEFT = Kee[int](0)
  CENTER = Kee[int](1)
  RIGHT = Kee[int](2)
