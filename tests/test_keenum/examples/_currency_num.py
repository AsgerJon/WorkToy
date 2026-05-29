"""
CurrencyNum subclasses 'KeeNum' and enumerates major world currencies.
Each currency is encapsulated by the 'CurrencyData' 'EZData' class,
which provides the 'value' of the members.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.keenum import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union
  from . import CurrencyNum

  NotImplementedType = type(NotImplemented)
  MaybeSelf: TypeAlias = Union[CurrencyNum, NotImplementedType]


class CurrencyData:
  """CurrencyNum encapsulates the name and symbol of a currency."""
  code = AttriBox[str]()
  symbol = AttriBox[str]()
  name = AttriBox[str]()
  decimals = AttriBox[int]()

  def __init__(self, *args) -> None:
    _code, _symbol, _name, _decimals = args
    self.code = _code if isinstance(_code, str) else str(_code)
    self.symbol = _symbol if isinstance(_symbol, str) else str(_symbol)
    self.name = _name if isinstance(_name, str) else str(_name)
    self.decimals = _decimals if isinstance(_decimals, int) else 0

  def __eq__(self, other: object) -> bool:
    cls = type(self)
    if not isinstance(other, cls):
      return NotImplemented
    return True if hash(self) == hash(other) else False

  def __hash__(self) -> int:
    return hash((self.code, self.symbol, self.name, self.decimals))


class CurrencyNum(KeeNum):
  """CurrencyNum enumerates major world currencies."""
  EUR = Kee[CurrencyData]('EUR', '€', 'Euro', 2)
  DKK = Kee[CurrencyData]('DKK', 'kr', 'Krone', 2)
  JPY = Kee[CurrencyData]('JPY', '¥', 'Yen', 0)
  GBP = Kee[CurrencyData]('GBP', '£', 'Sterling', 2)

  @classmethod
  def __class_resolve__(cls, curName: str) -> MaybeSelf:
    """Resolve a currency by ISO code or by unicode symbol."""
    for member in cls:
      if member.value.name == curName:
        return member
    return NotImplemented
