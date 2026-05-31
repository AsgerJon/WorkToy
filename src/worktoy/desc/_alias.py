"""
Alias re-exposes another descriptor under a second name.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import Object

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type


class Alias(Object):
  """
  Alias is a descriptor that re-exposes another attribute under a
  second name, typically one inherited from a parent class.

  Usage:

  >>> class Parent(BaseObject):
  ...   value = AttriBox[int](0)
  >>> class Child(Parent):
  ...   v = Alias('value')   # 'child.v' now reads/writes 'child.value'

  Resolution strategy
  -------------------
  When the class body finishes and '__set_name__' fires, 'Alias'
  checks whether the target name ('value' in the example) already
  resolves on the owning class. If so, it short-circuits the
  descriptor protocol by writing the target object directly into
  the owning class under the alias name, effectively removing
  itself from the class. Subsequent attribute access on the alias
  goes straight to the real descriptor with no extra indirection.

  If the target name is not yet visible on the class at
  '__set_name__' time (e.g. the parent hasn't been built yet, or
  the name is contributed later), 'Alias' stays in place and
  forwards each '__get__' / '__set__' / '__delete__' to the real
  descriptor at runtime via 'getattr(owner, self.__real_name__)'.
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
    Object.__init__(self, realName)
    self.__real_name__ = realName
