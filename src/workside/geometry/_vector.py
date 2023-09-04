"""WorkSide - Geometry - Vector
Representation of planar vectors."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.geometry import Point
from worktoy.fields import IntField


class Vector(Point):
  """WorkSide - Geometry - Size
  Rectangular size representation."""

  __geometry_class_name__ = 'Vector'
  vertical = IntField(1)
  horizontal = IntField(1)
