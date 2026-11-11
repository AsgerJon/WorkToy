"""
ShopRisk is the risk warning of the 'worktoy_shop' stand-in project.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import RiskWarning


class ShopRisk(RiskWarning):
  """
  A project built upon worktoy subclasses a warning of the family in a
  package of its own, and the warning then steps over the files of that
  project as well as those of worktoy. 'ShopRisk' is such a subclass,
  at home in 'worktoy_shop'.
  """

  __module__ = 'worktoy_shop'
  __slots__ = ()
