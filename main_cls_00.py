"""
MutInt is a mutable integer class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import maybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Any


class MutInt:
  __slots__ = (
    '__inner_value__',
    '__first_minus__',
    '__first_plus__',
    '__recursion_counter__',
    )

  def __init__(self, value: int = None) -> None:
    self.__inner_value__ = maybe(value, 0)
    self.__recursion_counter__ = 0
    self.__first_minus__ = False
    self.__first_plus__ = False

  def __int__(self, ) -> int:
    return self.__inner_value__

  def __neg__(self, ) -> Self:
    if self.__first_minus__:
      self.__inner_value__ -= 1
    self.__first_minus__ = not self.__first_minus__
    return print('return self') or self

  def __pos__(self, ) -> Self:
    if self.__first_plus__:
      self.__inner_value__ += 1
    self.__first_plus__ = not self.__first_plus__
    return self

  def _resolveOther(self, other: Any) -> Self:
    cls = type(self)
    if isinstance(other, cls):
      return other
    try:
      otherInt = int(other)
    except (TypeError, ValueError) as exception:
      raise TypeError from exception
    else:
      return cls(otherInt)

  def __lt__(self, other: Any) -> bool:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return True if int(self) < int(resolved) else False

  def __le__(self, other: Any) -> bool:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return False if int(self) > int(resolved) else True

  def __gt__(self, other: Any) -> bool:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return True if int(self) > int(resolved) else False

  def __ge__(self, other: Any) -> bool:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return False if int(self) < int(resolved) else True

  def __eq__(self, other: Any) -> bool:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return True if int(self) == int(resolved) else False

  def __ne__(self, other: Any) -> bool:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return False if int(self) == int(resolved) else True

  def __or__(self, other) -> Self:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    cls = type(self)
    return cls(int(self) | int(resolved))

  def __and__(self, other) -> Self:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    cls = type(self)
    return cls(int(self) & int(resolved))

  def __add__(self, other) -> Self:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    cls = type(self)
    return cls(int(self) + int(resolved))

  def __invert__(self, ) -> Self:
    cls = type(self)
    return cls(-self.__inner_value__, )

  def __sub__(self, other: Any) -> Self:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return self + (-resolved)

  def __mod__(self, other: Any) -> Self:
    resolved = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    cls = type(self)
    out = cls(int(self) % int(resolved))
    return cls(int(self) % int(resolved))

  def __bool__(self, ) -> bool:
    return True if self.__inner_value__ else False

  def __str__(self, ) -> str:
    return '%d' % int(self)

  def __repr__(self, ) -> str:
    return 'MutInt(%d)' % int(self)


class isEven(
  metaclass=type('_', (type,), dict(__call__=lambda *a: not (a[1] % 2))),
  ):
  pass


def mainTester(*args):
  i = MutInt(0)

  while ++i < 10:
    print(isEven(i), i)
