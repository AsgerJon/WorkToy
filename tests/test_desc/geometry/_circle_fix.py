"""
CircleFix subclasses 'Circle' and replaces the 'AttriBox' descriptors
with 'FixBox' descriptors to create immutable circles.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import FixBox
from . import Circle, Point2DFix


class CircleFix(Circle):
  """
  CircleFix subclasses 'Circle' and replaces the 'AttriBox' descriptors
  with 'FixBox' descriptors to create immutable circles.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables

  center = FixBox[Point2DFix]()
  radius = FixBox[float](1.0)
