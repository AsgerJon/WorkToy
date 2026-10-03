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
  descriptor at runtime.

  Either way the target is the object as a class along the method
  resolution order holds it, before the descriptor protocol applies, as
  'inspect.getattr_static' finds it; see '_getRealObject'. A staticmethod
  therefore stays a staticmethod, and a classmethod binds to the class it
  is read from.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __real_name__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getRealObject(self, owner: type) -> Any:
    """
    The '_getRealObject' method returns the object the alias stands for:
    the first entry under the real name in the namespaces of the classes
    along the method resolution order of 'owner'. Reading the name from
    the class instead would apply the descriptor protocol first, turning
    a staticmethod into a plain function, which then binds as a method,
    and a classmethod into a method bound to 'owner' for good. A name no
    class along the order holds, such as one a metaclass supplies, is
    read from 'owner' as before, which raises 'AttributeError' when
    nothing supplies it.
    """
    for cls in owner.__mro__:
      if self.__real_name__ in cls.__dict__:
        return cls.__dict__[self.__real_name__]
    return getattr(owner, self.__real_name__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: Type[Object], name: str) -> None:
    try:
      realObject = self._getRealObject(owner)
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
    realObject = self._getRealObject(owner)
    return realObject.__get__(instance, owner, )

  def __set__(self, instance: Any, value: Any, **kwargs) -> None:
    realObject = self._getRealObject(type(instance))
    return realObject.__set__(instance, value)

  def __delete__(self, instance: Any, **kwargs) -> None:
    realObject = self._getRealObject(type(instance))
    return realObject.__delete__(instance)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, realName: str) -> None:
    Object.__init__(self, realName)
    self.__real_name__ = realName
