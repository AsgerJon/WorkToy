"""
FlagRoll provides a KeeFlags for use with the NumLoad test.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, Kee

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class FlagRoll(KeeFlags):
  """
  FlagRoll provides a KeeFlags for use with the NumLoad test.
  """

  NEVER = Kee[int](0)
  GONNA = Kee[int](1)
  GIVE = Kee[int](2)
  YOU = Kee[int](3)
  UP = Kee[int](4)
