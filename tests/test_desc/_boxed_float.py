"""
BoxedNumber provides a class suitable for use in an AttriBox without
being a subclass of 'worktoy.core.Object'. This class achieves this by
implementing '__set_name__'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field
from worktoy.waitaminute import TypeException


class BoxedFloat:
  """
  BoxedNumber provides a class suitable for use in an AttriBox without
  being a subclass of 'worktoy.core.Object'.
  """
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables
  __fallback_value__ = 0

  #  Private Variables
  __field_name__ = None
  __field_owner__ = None
  __private_value__ = None

  #  Public Variables
  name = Field()
  owner = Field()
  value = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @name.GET
  def _getName(self, ) -> str:
    return self.__field_name__

  @owner.GET
  def _getOwner(self, ) -> type:
    return self.__field_owner__

  @value.GET
  def _getValue(self, **kwargs) -> float:
    if self.__private_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__private_value__ = float(self.__fallback_value__)
      return self._getValue(_recursion=True)
    if isinstance(self.__private_value__, float):
      return self.__private_value__
    raise TypeException('__private_value__', self.__private_value__, float)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __int__(self, ) -> int:
    return int(self.value)

  def __float__(self, ) -> float:
    return self.value

  def __complex__(self, ) -> complex:
    return self.value + 0j

  def __str__(self, ) -> str:
    return """%f""" % (self.value,)

  def __repr__(self, ) -> str:
    infoSpec = """%s(%f)"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.value,)
    return info

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, ) -> None:
    if args:
      self.__private_value__ = float(args[0])
