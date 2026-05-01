"""
The 'tests.test_desc.geometry' package provides geometry flavoured classes
used by test modules.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._point_2d import Point2D
from ._point_2d_fix import Point2DFix
from ._circle import Circle
from ._circle_fix import CircleFix

__all__ = [
  'Point2D',
  'Point2DFix',
  'Circle',
  'CircleFix',
]
