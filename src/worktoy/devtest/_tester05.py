"""YOLO"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MissingKeyHandleError


class SusNameSpace(dict):
  """A custom namespace class."""

  def __init__(self, name, bases, *args, **kwargs) -> None:
    dict.__init__(self)
    self._className = name
    self._classBases = bases

  def __getitem__(self, key: str, ) -> object:
    if key in self:
      return self[key]


class MyMetaClass(type):
  """A Typical metaclass."""

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs):
    return SusNameSpace(name, bases)


try:
  class MyClass(metaclass=MyMetaClass):
    """A class derived from the metaclass"""

    @staticmethod
    def myMethod():
      """A static method. """
      pass
except TypeError as e:
  raise MissingKeyHandleError(SusNameSpace('test', ()), MyMetaClass)
