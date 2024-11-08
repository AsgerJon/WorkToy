"""KeeNum enumerates items."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field
from worktoy.keenum import MetaNum
from worktoy.meta import CallMeMaybe
from worktoy.text import typeMsg


def _root(callMeMaybe: CallMeMaybe) -> CallMeMaybe:
  """Return the root class."""
  setattr(callMeMaybe, '__trust_me_bro__', True)
  return callMeMaybe


class KeeNum(metaclass=MetaNum):
  """KeeNum enumerates items."""

  __private_value__ = None
  __public_value__ = None
  __public_name__ = None

  value = Field()
  name = Field()

  @value.GET
  def _getPublicValue(self) -> object:
    """Getter-function for the public value."""
    if self.__public_value__ is None:
      return self.name
    return self.__public_value__

  @name.GET
  def _getPublicName(self) -> str:
    """Getter-function for the public name."""
    if self.__public_name__ is None:
      e = """The public name is not set."""
      raise TypeError(e)
    if isinstance(self.__public_name__, str):
      return self.__public_name__
    e = typeMsg('publicName', self.__public_name__, str)
    raise TypeError(e)

  def setPrivateValue(self, privateValue: int) -> None:
    """Setter-function for the private value."""
    if self.__private_value__ is not None:
      e = """The private value is already set."""
      raise TypeError(e)
    if not isinstance(privateValue, int):
      e = typeMsg('privateValue', privateValue, int)
      raise TypeError(e)
    self.__private_value__ = privateValue

  def setPublicName(self, publicName: str) -> None:
    """Setter-function for the public name."""
    if self.__public_name__ is not None:
      e = """The public name is already set."""
      raise TypeError(e)
    if not isinstance(publicName, str):
      e = typeMsg('publicName', publicName, str)
      raise TypeError(e)
    self.__public_name__ = publicName

  def __int__(self, ) -> int:
    """Return the private value as an integer."""
    if self.__private_value__ is None:
      e = """The private value is not set."""
      raise TypeError(e)
    if isinstance(self.__private_value__, int):
      return self.__private_value__
    e = typeMsg('privateValue', self.__private_value__, int)
    raise TypeError(e)

  @_root
  def __init__(self, publicValue: object) -> None:
    self.__public_value__ = publicValue

  def __str__(self, ) -> str:
    """Return the public name as a string."""
    clsName = type(self).__name__
    return """%s.%s""" % (clsName, self.name.upper())

  def __repr__(self, ) -> str:
    """Return the public name as a string."""
    clsName = type(self).__name__
    return """%s(%s)""" % (clsName, self.name)

  def __eq__(self, other: object) -> bool:
    """Return True if the public value is equal to the other."""
    if isinstance(other, KeeNum):
      cls = type(self).__mro__[0]
      otherCls = type(other).__mro__[0]
      if cls is otherCls:
        return False if int(self) - int(other) else True
      return False
    if isinstance(other, int):
      return False if int(self) - other else True
    if isinstance(other, str):
      return True if self.name == other else False
    return False

  def __hash__(self, ) -> int:
    """Return the hash of the public value."""
    return hash((type(self), self.name, int(self)))
