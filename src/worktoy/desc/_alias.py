"""
Alias provides a descriptor allowing renaming of a descriptor, typically
one inherited from a parent.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import Object

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type


class Alias(Object):
  """
  Alias provides a descriptor allowing renaming of a descriptor, typically
  one inherited from a parent.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __real_name__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: Type[Object], name: str) -> None:
    try:
      realObject = getattr(owner, self.__real_name__)
    except AttributeError:
      #  If the real object does not exist, '__get__' will forward at
      #  runtime.
      pass
    else:
      #  Effectively makes the alias point to the real object, effectively
      #  removing 'self' from 'owner'.
      setattr(owner, name, realObject)
    Object.__set_name__(self, owner, name)

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    realObject = getattr(owner, self.__real_name__)
    return realObject.__get__(instance, owner, )

  def __set__(self, instance: Any, value: Any, **kwargs) -> None:
    realObject = getattr(type(instance), self.__real_name__)
    return realObject.__set__(instance, value)

  def __delete__(self, instance: Any, **kwargs) -> None:
    realObject = getattr(type(instance), self.__real_name__)
    return realObject.__delete__(instance)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, realName: str) -> None:
    """
    Initializes the Alias descriptor with the name of the real descriptor.
    """
    Object.__init__(self, realName)
    self.__real_name__ = realName
