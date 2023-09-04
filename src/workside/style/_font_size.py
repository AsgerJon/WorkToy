"""WorkSide - Style - FontSize
Alias for positive integers for font sizes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QFont

from worktoy.fields import IntField
from worktoy.metaclass import MetaNumClass


class FontSize(int, metaclass=MetaNumClass):
  """WorkSide - Style - FontSize
  Alias for positive integers for font sizes."""

  innerValue = IntField(-1)

  @staticmethod
  def text2Int(text: str) -> int:
    """Finds integer representation of text"""
    if not text:
      return 0
    digs = {('%d' % i): i for i in range(10)}
    strVal = [c for c in (text or []) if c in digs]
    while strVal and strVal[0] == '0':
      strVal = strVal[1:]

    out = 0
    dec = 0
    for c in reversed([char for char in strVal]):
      dig = digs.get(c, None)
      if dig is not None:
        out += (dig * 10 ** dec)
        dec += 1

    return out

  def __new__(cls, *args, **kwargs) -> Any:
    intVal = None
    strVal = None
    for arg in args:
      if isinstance(arg, int) and intVal is None:
        intVal = arg
      if isinstance(arg, str) and strVal is None:
        strVal = arg
    strVal = cls.text2Int(strVal or '')
    val = strVal or intVal
    out = int.__new__(cls, val)
    if val < 0:
      raise ValueError('FontSize cannot be negative!')
    out.innerValue = val
    return out

  def __str__(self) -> str:
    return 'Font Size: %d' % self

  def __repr__(self, ) -> str:
    return '%s(%d)' % (self.__class__.__qualname__, 0 + self)

  def __radd__(self, other: Any) -> int:
    """Reversed operand ordered addition."""
    if isinstance(other, int):
      return self + other

  def __add__(self, other: Any) -> FontSize:
    """Regular addition"""
    if isinstance(other, int):
      return FontSize(int(self) + other)
    if isinstance(other, (FontSize, float)):
      return FontSize(self + int(other))

  def __iadd__(self, other: Any) -> FontSize:
    if isinstance(other, int):
      self = FontSize(int(self) + other)
    if isinstance(other, (FontSize, float)):
      self = FontSize(int(self) + int(other))
    return self

  def __sub__(self, other: Any) -> FontSize:
    if isinstance(other, int):
      return FontSize(int(self) - other)
    if isinstance(other, (FontSize, float)):
      return FontSize(int(self) - int(other))
    return NotImplemented

  def __eq__(self, other: Any) -> bool:
    return False if self - other else True

  def __ne__(self, other: Any) -> bool:
    return True if self - other else False

  def __int__(self, ) -> int:
    return self.innerValue

  def __rshift__(self, other: Any) -> Any:
    if isinstance(other, QFont):
      other.setPointSize(self.innerValue)
      return other
