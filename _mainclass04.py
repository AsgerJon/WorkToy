"""blabla"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.core import Function
from worktoy import WorkThis


class Parent:
  """Parent class"""

  def parentMethod(self) -> str:
    """pass"""
    return 'parent method'


class Child(Parent):
  """child class"""

  def __init__(self, ) -> None:
    self._name = None
    self._owner = None

  def getName(self) -> str:
    """LOL"""
    return self._name

  def getOwner(self) -> type:
    """LOL"""
    return self._owner

  def __set_name__(self, owner: type, name: str):
    ic(owner, name)
    self._name = name
    self._owner = owner

  @WorkThis
  def testFunction(self, this: Function, a: int = None,
                   b: int = None, *args) -> object:
    """some function"""
    ic(self)
    ic(this)
    ic(a)
    ic(b)
    if not a and not b:
      return
    if a > b:
      return this(self, this, b, a)
    return b - a

  def childMethod(self) -> str:
    """pass"""
    return 'child method'

  def __str__(self, ) -> str:
    """String Representation"""
    return '%s.%s' % (self.__class__.__qualname__, self.getName())
