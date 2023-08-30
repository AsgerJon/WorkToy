"""LMAO"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from random import choices
from string import ascii_letters, digits

from icecream import ic

from worktoy.core import Decorator
from typing import TYPE_CHECKING

from worktoy.core._quick import Quick


class MetaLine(type):
  """LOL"""

  def __call__(cls, name=None, val=None) -> str:
    ic(cls, )
    return '%s = %s' % (name, val)


class Line(metaclass=MetaLine):
  """LMAO"""

  def __init__(self, ) -> None:
    self._name = self.__class__.__name__

  def __call__(self, name: str, val: int) -> str:
    return '%s = %d' % (name, val)


class Meta(type):
  """LMAO"""

  def __new__(typ, name, bases, nameSpace, **kwargs) -> object:
    ic(nameSpace)
    ic(kwargs)
    return type.__new__(typ, name, bases, nameSpace, **kwargs)


class M(metaclass=Meta):
  """LOL"""

  fuck = 0
  object.__new__(Line)('a', 7)


####
#
class LMAO:
  """LMAO"""

  def __init__(self, *args, **kwargs) -> None:
    pass


if TYPE_CHECKING:
  from worktoy.base import DefaultClass as LMAO


@Quick()
class Rectangle(LMAO):
  """FUCK"""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._width = 777
    self._height = 6666

    print(self.monoSpace)

    print(self.maybe)
    print(self.maybeType)

  def testMono(self) -> str:
    chars = [ascii_letters, digits, 10 * ' ']
    chars = [c for c in chars]
    return ''.join(choices(chars, k=100))

  def test(self) -> list:
    return self.stringList('a, b, c')

  def __str__(self) -> str:
    return 'Rectangle: %d-%d' % (self._width, self._height)
