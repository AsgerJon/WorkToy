"""LMAO"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from icecream import ic

ic.configureOutput(includeContext=True)


class Namespace(dict):

  def __setitem__(self, key: str, value: object) -> None:
    ic(key, value)
    return dict.__setitem__(self, key, value)


class MetaType(type):

  @classmethod
  def __prepare__(mcls, *args, **kwargs) -> Namespace:
    return Namespace()


def sus(newName: str) -> Callable:
  def decorator(callMeMaybe: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> None:
      return callMeMaybe(*args, **kwargs)

    setattr(wrapper, '__name__', newName)
    return wrapper

  return decorator


class TestClass(metaclass=MetaType):
  lmao = True
  value = 68
  value += 1
  bla = type('bla', (), dict(lol=None))
  setattr(bla, 'lol', True)

  class Mom:
    __slots__ = ['fat']

  urMom = Mom()

  def whatever(self, ) -> None:
    pass

  urMom.fat = True

  blabla = []

  for _ in range(10):
    blabla.append('i suck')

  while blabla:
    yikes = blabla.pop()

  @sus('better name')
  def midName(self) -> None:
    pass
