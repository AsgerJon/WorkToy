"""
BrushTest tests owning of RGBNum instances
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject
from . import RGBNum


class Brush(BaseObject):
  """BrushTest tests owning of RGBNum instances."""

  color = RGBNum.RED
