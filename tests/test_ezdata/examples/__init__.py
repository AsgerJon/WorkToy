"""
The 'tests.test_ezdata.examples' package provides example dataclasses for
testing the 'EZData' dataclass implementation provided by 'worktoy.ezdata'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._ez_complex import EZComplex
from ._point_2d import Point2D
from ._circle import Circle
from ._full_name import FullName
from ._rich_data import RichData

__all__ = (
  'EZComplex',
  'Point2D',
  'Circle',
  'FullName',
  'RichData',
)
