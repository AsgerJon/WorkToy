"""
Point3D subclasses 'object' and provides an example class encapsulating a
space point.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class Point3D:
  x = AttriBox[float]()
  y = AttriBox[float]()
  z = AttriBox[float]()

  def __abs__(self, ) -> float:
    return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

  def __eq__(self, other: Self) -> bool:
    if self.x != other.x:
      return False
    if self.y != other.y:
      return False
    if self.z != other.z:
      return False
    return True

  def __init__(self, *args) -> None:
    keys = 'x', 'y', 'z'
    for key, val in zip(keys, args):
      setattr(self, key, float(val))
