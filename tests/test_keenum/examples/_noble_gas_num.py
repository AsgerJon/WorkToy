"""
NobleGasNum subclasses 'KeeNum' and enumerates the noble gases and
provides as 'value' their atomic numbers.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class NobleGasNum(KeeNum):
  """NobleGasNum enumerates atomic numbers of noble gases."""
  NEON = Kee[int](10)
  ARGON = Kee[int](18)
  KRYPTON = Kee[int](36)
  XENON = Kee[int](54)
  RADON = Kee[int](86)
  OGANESSON = Kee[int](118)
