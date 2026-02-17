"""
HAlignum enumerates horizontal alignments.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover
  pass


class HAlignum(KeeNum):
  """
  HAlignum enumerates horizontal alignments.
  """

  LEFT = Kee[int](0)
  CENTER = Kee[int](1)
  RIGHT = Kee[int](2)
