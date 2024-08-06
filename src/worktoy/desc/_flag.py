"""Flag provides a replacement for 'bool' which can't be instantiated or
managed correctly or something, so this is used by 'AttriBox' instances in
replacement of 'bool'."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.meta import BaseMetaclass


class _FlagMeta(BaseMetaclass):
  """Flag metaclass"""

  def __str__(cls, ) -> str:
    """String representation"""
    return type.__str__(bool)

  def __repr__(cls, ) -> str:
    """Code representation"""
    return type.__repr__(bool)

  def __instancecheck__(cls, instance) -> bool:
    """Instance check"""
    return bool.__instancecheck__(instance)

  def __subclasscheck__(cls, subclass) -> bool:
    """Subclass check"""
    return bool.__subclasscheck__(subclass)

  def __getattr__(cls, key: str) -> Any:
    """This method was implemented by a professional in a safe
    environment, do not try this at home!"""
    return type.__getattribute__(bool, key)


class Flag(metaclass=_FlagMeta):
  """Flag provides a replacement for 'bool' which can't be instantiated or
  managed correctly or something, so this is used by 'AttriBox' instances in
  replacement of 'bool'."""

  __inner_value__ = None

  def __init__(self, *args) -> None:
    if args:
      if args[0]:
        self.__inner_value__ = True
    else:
      self.__inner_value__ = False

  def __bool__(self) -> bool:
    """Bool representation"""
    return True if self.__inner_value__ else False

  def __getattribute__(self, key: str, **kwargs) -> Any:
    """This method was implemented by a professional in a safe
    environment, do not try this at home!"""
    if kwargs.get('_recursion', False):
      raise kwargs['_recursion']
    if key == '__class__':
      return bool
    if key == '__name__':
      return 'bool'
    if key == '__bases__':
      return (int,)
    if key == '__mro__':
      return bool, int, object
    if key == '__doc__':
      return bool.__doc__
    return object.__getattribute__(self, key)

  def __getattr__(self, key: str) -> Any:
    """This method was implemented by a professional in a safe
    environment, do not try this at home!"""
    try:
      if object.__getattribute__(self, '__inner_value__'):
        return object.__getattribute__(True, key)
      return object.__getattribute__(False, key)
    except AttributeError as attributeError:
      return type(self).__getattribute__(self, _recursion=attributeError)

  def __str__(self) -> str:
    """String representation"""
    if self.__inner_value__:
      return bool.__str__(True)
    return bool.__str__(False)

  def __repr__(self, ) -> str:
    """Code representation"""
    if self.__inner_value__:
      return bool.__repr__(True)
    return bool.__repr__(False)
