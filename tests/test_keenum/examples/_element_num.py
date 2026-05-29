"""
ElementNum subclasses 'KeeNum' and enumerates chemical elements.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee
from worktoy.desc import AttriBox

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union
  from . import ElementNum

  NotImplementedType = type(NotImplemented)
  MaybeSelf: TypeAlias = Union[ElementNum, NotImplementedType]


class ElementData:
  """ElementData encapsulates the basics of a chemical element."""

  name = AttriBox[str]()
  symbol = AttriBox[str]()
  number = AttriBox[int]()
  mass = AttriBox[float]()

  def __init__(self, *args) -> None:
    self.name, self.symbol, self.number, self.mass = args

  def __eq__(self, other: object) -> bool:
    cls = type(self)
    if not isinstance(other, cls):
      return NotImplemented
    return True if hash(self) == hash(other) else False

  def __hash__(self) -> int:
    return hash((self.name, self.symbol, self.number, self.mass))


class ElementNum(KeeNum):
  """ElementNum enumerates the first ten chemical elements."""
  HYDROGEN = Kee[ElementData]('hydrogen', 'H', 1, 1.008)
  HELIUM = Kee[ElementData]('helium', 'He', 2, 4.0026)
  LITHIUM = Kee[ElementData]('lithium', 'Li', 3, 6.94)
  BERYLLIUM = Kee[ElementData]('beryllium', 'Be', 4, 9.0122)
  BORON = Kee[ElementData]('boron', 'B', 5, 10.81)
  CARBON = Kee[ElementData]('carbon', 'C', 6, 12.011)
  NITROGEN = Kee[ElementData]('nitrogen', 'N', 7, 14.007)
  OXYGEN = Kee[ElementData]('oxygen', 'O', 8, 15.999)
  FLUORINE = Kee[ElementData]('fluorine', 'F', 9, 18.998)
  NEON = Kee[ElementData]('neon', 'Ne', 10, 20.180)

  @classmethod
  def __class_resolve__(cls, elementSymbol: str) -> MaybeSelf:
    """Resolve an element from its chemical symbol."""
    for member in cls:
      if member.value.symbol == elementSymbol:
        return member
    return NotImplemented
