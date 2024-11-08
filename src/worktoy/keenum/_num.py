"""Num represents enumerated members of a given enum class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import typeMsg

try:
  from typing import Any
except ImportError:
  Any = object


class Num:
  """Num represents enumerated members of a given enum class."""

  __public_value__ = None
  __public_name__ = None
  __private_value__ = None

  def __init__(self, *args, **kwargs) -> None:
    if args:
      self.setPublicValue(args[0])

  def setPrivateValue(self, privateValue: int) -> None:
    """Setter-function for the private value."""
    if self.__private_value__ is not None:
      e = """The private value is already set."""
      raise TypeError(e)
    if not isinstance(privateValue, int):
      e = typeMsg('privateValue', privateValue, int)
      raise TypeError(e)
    self.__private_value__ = privateValue

  def getPrivateValue(self) -> int:
    """Getter-function for the private value."""
    if self.__private_value__ is None:
      e = """The private value is not set."""
      raise TypeError(e)
    if isinstance(self.__private_value__, int):
      return self.__private_value__
    e = typeMsg('privateValue', self.__private_value__, int)
    raise TypeError(e)

  def setPublicName(self, publicName: str) -> None:
    """Setter-function for the public name."""
    if self.__public_name__ is not None:
      e = """The public name is already set."""
      raise TypeError(e)
    if not isinstance(publicName, str):
      e = typeMsg('publicName', publicName, str)
      raise TypeError(e)
    self.__public_name__ = publicName

  def getPublicName(self) -> str:
    """Getter-function for the public name."""
    if self.__public_name__ is None:
      e = """The public name is not set."""
      raise TypeError(e)
    if isinstance(self.__public_name__, str):
      return self.__public_name__
    e = typeMsg('publicName', self.__public_name__, str)
    raise TypeError(e)

  def setPublicValue(self, publicValue: Any) -> None:
    """Setter-function for the public value."""
    if self.__public_value__ is not None:
      e = """The public value is already set."""
      raise TypeError(e)
    self.__public_value__ = publicValue

  def getPublicValue(self, **kwargs) -> Any:
    """Getter-function for the public value."""
    if self.__public_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.setPublicValue(self.getPublicName())
      return self.getPublicValue(_recursion=True)
    return self.__public_value__


def auto(*args, **kwargs) -> Num:
  """Auto create a KeeNum class."""
  if args and kwargs:
    return Num((args, kwargs))
  if args:
    if len(args) > 1:
      return Num(args)
    return Num(args[0])
  if kwargs:
    return Num(kwargs)
  return Num()
