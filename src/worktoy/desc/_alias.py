"""
Alias provides a descriptor allowing renaming of a descriptor, typically
one inherited from a parent.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..core import Object

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeVar, Type


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

  def __get__(self, instance: Any, owner: type) -> Any:
    realDesc = getattr(type(instance), self.__real_name__, )
    return realDesc.__get__(instance, owner)

  def __set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    Sets the value of the aliased descriptor.
    """
    realDesc = getattr(type(instance), '__real_name__', )
    return realDesc.__set__(instance, value, **kwargs)

  def __delete__(self, instance: Any, **kwargs) -> None:
    """
    Deletes the value of the aliased descriptor.
    """
    realDesc = getattr(type(instance), '__real_name__', )
    return realDesc.__delete__(instance, **kwargs)

  def __set_name__(self, owner: Type[Object], name: str) -> None:
    try:
      _ = getattr(owner, self.__real_name__)
    except AttributeError as attributeError:
      raise RuntimeError from attributeError
    else:
      Object.__set_name__(self, owner, name)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, realName: str) -> None:
    """
    Initializes the Alias descriptor with the name of the real descriptor.
    """
    self.__real_name__ = realName
