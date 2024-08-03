"""Dataclass for a point in the plane using EZData."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData
from worktoy.desc import AttriBox


class PlanePoint(EZData):
  """Dataclass representing a point in the plane."""
  x = AttriBox[float](0)
  y = AttriBox[float](0)

  def __str__(self, ) -> str:
    """String representation"""
    return """(%.3f, %.3f)""" % (self.x, self.y)
