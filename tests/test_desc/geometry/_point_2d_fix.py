"""
Point2DFix subclasses 'Point2D' and replaces the 'AttriBox' descriptors
with 'FixBox' descriptors to create immutable 2D points.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import FixBox
from . import Point2D

if TYPE_CHECKING:  # pragma: no cover
  pass


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
