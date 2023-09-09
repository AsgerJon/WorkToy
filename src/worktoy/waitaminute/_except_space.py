"""WorkToy - Wait A Minute! - ErrorNameSpace
Special namespace class for use with the metaclass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Keys, Items, Values, Bases


class ExceptSpace(dict):
  """WorkToy - Wait A Minute! - ErrorNameSpace
  Special namespace class for use with the metaclass."""

  def __new__(cls, name: str, bases: tuple[type], **kwargs) -> object:
    return super().__new__(cls)

  def __init__(self, name: str, bases: tuple[type], **kwargs) -> None:
    dict.__init__(self, )
    self._name = name
    self._bases = bases
    self._kwargs = kwargs
    dict.__setitem__(self, '__name__', '\nWorkToy - Wait A Minute!\n')

  def __setitem__(self, key: str, val: object) -> None:
    dict.__setitem__(self, key, val, )

  def __getitem__(self, key: str) -> object:
    return dict.__getitem__(self, key)

  def __delitem__(self, key: str) -> None:
    dict.__delitem__(self, key)

  def __contains__(self, key: str) -> bool:
    val = dict.__contains__(self, key)
    return True if val else False

  def keys(self) -> Keys:
    """Implementation of keys"""
    return dict.keys(self)

  def items(self) -> Items:
    """Implementation of keys"""
    return dict.items(self)

  def values(self) -> Values:
    """Implementation of keys"""
    return dict.values(self)

  def __iter__(self) -> object:
    iterableObject = dict.__iter__(self, )
    return iterableObject

  def getName(self) -> str:
    """Getter-function for name of created class"""
    return self._name

  def getBases(self) -> Bases:
    """Getter-function for name of bases"""
    return self._bases

  def getKwargs(self) -> dict:
    """Getter-function for the keyword arguments"""
    return self._kwargs
