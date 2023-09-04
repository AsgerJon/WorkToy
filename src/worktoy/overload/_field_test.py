"""Testing fields and overloads"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import OverLoad
from worktoy.metaclass import MetaField


def func(a: int) -> int:
  """Some function"""


class TestField(metaclass=MetaField):
  """LMAO"""

  fuck = func

  cunt = lambda: None

  @classmethod
  def bla(cls) -> int:
    """blabla"""
    return 7777

  @staticmethod
  def lmao() -> str:
    """blabla"""
    return 'cunts'

  def __init__(self, a: str, b: str, c: int) -> None:
    """One"""
    self._a = a
    self._b = b
    self._c = c

  def __init__(self, a: str, b: int, c: str) -> None:
    """Two"""
    self._a = a
    self._b = b
    self._c = c

  def __init__(self, a: int, b: str, c: int) -> None:
    """Three"""
    self._a = a
    self._b = b
    self._c = c

  def __str__(self) -> str:
    out = ', '.join([str(arg) for arg in [self._a, self._b, self._c]])
    return '(%s)' % out

  def __repr__(self) -> str:
    out = ', '.join([str(arg) for arg in [self._a, self._b, self._c]])
    return '(%s)' % out
