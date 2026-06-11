"""
Point2DFix subclasses 'Point2D' and replaces the 'AttriBox' descriptors
with 'FixBox' descriptors to create immutable 2D points.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import FixBox
from . import Point2D


class Point2DFix(Point2D):
  """
  Point2DFix subclasses 'Point2D' and replaces the 'AttriBox' descriptors
  with 'FixBox' descriptors to create immutable 2D points.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  x = FixBox[float](0.0)
  y = FixBox[float](0.0)
