"""
PlanetNum subclasses 'KeeNum' and enumerates the planets of the solar
system.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.keenum import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union
  from . import PlanetNum

  NotImplementedType = type(NotImplemented)
  MaybeSelf: TypeAlias = Union[PlanetNum, NotImplementedType]


class PlanetData:
  """PlanetData encapsulates the name and order of a planet."""

  name = AttriBox[str]()
  mass = AttriBox[float]()
  radius = AttriBox[float]()
  au = AttriBox[float]()

  def __init__(self, *args) -> None:
    self.name, self.mass, self.radius, self.au = args

  def __eq__(self, other: object) -> bool:
    cls = type(self)
    if not isinstance(other, cls):
      return NotImplemented
    return True if hash(self) == hash(other) else False

  def __hash__(self) -> int:
    return hash((self.name, self.mass, self.radius, self.au))


class PlanetNum(KeeNum):
  """PlanetNum enumerates the eight planets of the solar system."""
  MERCURY = Kee[PlanetData]('mercury', 3.301e23, 2440.0, 0.39)
  VENUS = Kee[PlanetData]('venus', 4.867e24, 6052.0, 0.72)
  EARTH = Kee[PlanetData]('earth', 5.972e24, 6371.0, 1.00)
  MARS = Kee[PlanetData]('mars', 6.417e23, 3390.0, 1.52)
  JUPITER = Kee[PlanetData]('jupiter', 1.898e27, 69911.0, 5.20)
  SATURN = Kee[PlanetData]('saturn', 5.683e26, 58232.0, 9.58)
  URANUS = Kee[PlanetData]('uranus', 8.681e25, 25362.0, 19.22)
  NEPTUNE = Kee[PlanetData]('neptune', 1.024e26, 24622.0, 30.05)

  @classmethod
  def __class_resolve__(cls, val: PlanetData) -> MaybeSelf:
    """Resolve a planet from its astronomical glyph."""
    for member in cls:
      if member.value == val:
        return member
    return NotImplemented
