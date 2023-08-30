"""WorkToy - Wait A Minute! - MetaXcept
Metaclass creating the exception types"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Union

from worktoy.core import Bases
from worktoy.metaclass import AbstractMetaClass
from worktoy.waitaminute import ExceptSpace


class _MetaXcept(AbstractMetaClass):
  """WorkToy - Wait A Minute! - MetaXcept
  Metaclass creating the exception types"""

  @classmethod
  def __prepare__(mcls, *args, **kwargs) -> dict:
    name, bases = args[0], args[1]
    return ExceptSpace(name, bases, **kwargs)

  def __new__(mcls, *args, **kwargs) -> type:
    name = args[0]
    bases = args[1]
    nameSpace = args[2]
    out = AbstractMetaClass.__new__(mcls, name, bases, nameSpace, **kwargs)
    out.__name_space__ = nameSpace
    return out

  def __init__(cls, *args, **kwargs) -> None:
    name = args[0]
    bases = args[1]
    nameSpace = args[2]
    if isinstance(nameSpace, dict):
      AbstractMetaClass.__init__(cls, name, bases, nameSpace, **kwargs)
    else:
      raise TypeError

  def __eq__(cls, other: type) -> bool:
    """Other must be a type"""
    return True if cls is other else False


class MetaXcept(Exception, metaclass=_MetaXcept):
  """In between class exposing the metaclass."""

  def __init__(self, *args, **kwargs) -> None:
    Exception.__init__(self, *args)
    self._kwargs = kwargs

  def __getattr__(self, key: str) -> object:
    cls = object.__getattribute__(self, '__class__')
    return object.__getattribute__(cls, key)

  def __eq__(self, other: object) -> bool:
    """Implementation of equal operator. Please note that this method is
    relates to the instance, not to the class. The class (MetaXcept) has
    its own implementation.
    If other is a type, this method returns MetaXcept == other
    If other is a string:
      self.__str__() == other
    Otherwise:
      self.__str__() == other.__str__()"""
    if isinstance(other, type):
      return self.__class__ == other
    if isinstance(other, str):
      return other in [self.__str__(), self.__class__.__qualname__]
    return self == object.__str__(other)

  def handle(self, *args, **kwargs) -> Never:
    """Should be invoked after the exception is caught. By default,
    it raises itself. """
    raise self
