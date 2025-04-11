"""NumCastException is a custom exception subclass of ValueError raised by
the 'numCast' function when unable to caste a value to a given type. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeCastException


class _Attr:
  """Descriptor for value. """

  __pvt_name__ = None

  def __init__(self, pvtName: str) -> None:
    self.__pvt_name__ = pvtName

  def __get__(self, instance: object, owner: type) -> object:
    if instance is None:
      return self
    out = getattr(instance, self.__pvt_name__, None)
    if out is None:
      e = """The value descriptor: '%s' has not been set!"""
      raise AttributeError(e % self.__pvt_name__)
    return out


class NumCastException(TypeCastException):
  """NumCastException is a custom exception subclass of ValueError raised by
  the 'numCast' function when unable to caste a value to a given type. """

  __offending_value__ = None
  __target_type__ = None

  value = _Attr('__offending_value__')
  target = _Attr('__target_type__')

  def __init__(self, value: object, target: type) -> None:
    TypeCastException.__init__(self, value, target)
    self.__offending_value__ = value
    self.__target_type__ = target
