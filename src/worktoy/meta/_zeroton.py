"""Zeroton introduces the novel idea of a class not having even one
instance, unlike a singleton class. The purpose of such classes is to have
universal objects that retain identity across modules."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.meta import BaseMetaclass, BaseNamespace


class ZeroSpace(BaseNamespace):
  """The Zeroton class is a class that has no instances. It is used to
  represent a universal object that retains identity across modules."""

  __virgin_namespace__ = None

  def setVirginNamespace(self, namespace: BaseNamespace) -> None:
    """This method sets the virgin namespace."""
    self.__virgin_namespace__ = namespace

  def getVirginNamespace(self) -> BaseNamespace:
    """This method returns the virgin namespace."""
    return self.__virgin_namespace__

  def __getitem__(self, key: str) -> Any:
    """If there is already a virgin namespace, this class always raises a
    KeyError"""
    if self.__virgin_namespace__ is None:
      return BaseNamespace.__getitem__(self, key)
    raise KeyError(key)

  def __setitem__(self, key: str, value: object) -> None:
    """If there is already a virgin namespace, this class always raises a
    KeyError"""
    if self.__virgin_namespace__ is None:
      BaseNamespace.__setitem__(self, key, value)


class ZeroMeta(BaseMetaclass):
  """The Zeroton class is a class that has no instances. It is used to
  represent a universal object that retains identity across modules."""

  __all__ = {}

  def __instancecheck__(cls, instance: Any) -> bool:
    """I know this is a bit lame, but the documentation took a very long
    time. You're welcome!"""
    if cls.__name__ == 'ATTR':
      if instance.__name__ == 'BOX':
        return True
      return False
    if cls.__name__ == 'TYPE':
      if instance.__name__ == 'THIS':
        return True
    return False

  @classmethod
  def __prepare__(mcls, name: str, *args, **kwargs) -> ZeroSpace:
    if mcls.__all__.get(name, None) is not None:
      return mcls.__all__.get(name).get('space')
    return ZeroSpace(mcls, name, *args, **kwargs)

  def __new__(mcls, name: str, *args, **kwargs) -> type:
    if mcls.__all__.get(name, None) is not None:
      return mcls.__all__.get(name).get('cls')
    return BaseMetaclass.__new__(ZeroMeta, name, *args, **kwargs)

  def __call__(cls, *args, **kwargs):
    return cls


class Zeroton(metaclass=ZeroMeta):
  """The Zeroton class is a class that has no instances. It is used to
  represent a universal object that retains identity across modules."""
