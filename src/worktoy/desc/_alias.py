"""
Alias re-exposes a descriptor under a second name.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import Object
from ..waitaminute import MissingVariable, TypeException
from ..waitaminute.desc import NotADescriptor
from ..waitaminute.desc import DanglingAlias, ReadOnlyError, ProtectedError

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Optional


class Alias(Object):
  """
  An attribute sometimes needs a second name, a short one or one an
  outside interface expects, without becoming a second attribute: both
  names must read, write and delete the very same value, run the same
  hooks, and follow a subclass that redeclares the attribute. A second
  name for something that is not an attribute protocol, or for a name
  that holds nothing, is a mistake in the class body.

    class Geometry(BaseObject):
      width = AttriBox[int](240)
      w = Alias('width')

  Implementation
  --------------

  Through an instance, every read, write and deletion is forwarded to
  the descriptor the real name holds, found afresh at each access as the
  first class dictionary along the resolution order of the class of the
  instance holds it. Through the class, the alias reads as itself. As
  the class is created, a real name no class holds, or the alias's own
  name, raises 'DanglingAlias'; a name holding a plain value raises
  'NotADescriptor'. A plain function, a 'staticmethod', a 'classmethod'
  and an overloaded method may be aliased, and an instance then reads
  through the alias what it reads through the real name; an alias of
  '__add__' at '__radd__' follows the overloads a subclass adds. A write
  or deletion through the alias of a method raises 'ReadOnlyError' or
  'ProtectedError' rather than shadowing the method on the instance. Two
  aliases naming each other are not detected and recurse at the first
  access.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __real_name__: Optional[str] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getRealName(self) -> str:
    if self.__real_name__ is None:
      raise MissingVariable(self, '__real_name__', str)
    return self.__real_name__

  def _getDescriptor(self, owner: type) -> Any:
    """
    The alias must reach the descriptor of the real name as the class of
    the instance holds it, not through its '__get__', which would give the
    value instead of the protocol.

    Implementation
    --------------

    The first own dictionary along the resolution order holding the name
    answers. An object whose type has no '__get__', asked as Python asks,
    is not a descriptor.

    Parameters
    ----------

    owner : type
      The class of the instance, or the class being created.

    Returns
    -------

    Any
      The descriptor.

    Raises
    ------

    DanglingAlias
      No class along the resolution order holds the name.

    NotADescriptor
      The name holds a plain value.
    """
    name = self._getRealName()
    for cls in owner.__mro__:
      if name in cls.__dict__:
        descriptor = cls.__dict__[name]
        break
    else:
      raise DanglingAlias(self, name, owner)
    #  Python reads '__get__' off the type, so a value whose class answers
    #  it only through '__getattr__', as a proxy does, is no descriptor.
    try:
      _ = type.__getattribute__(type(descriptor), '__get__')
    except AttributeError:
      raise NotADescriptor(self, name, descriptor)
    else:
      return descriptor

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, realName: str) -> None:
    if not isinstance(realName, str):
      raise TypeException('realName', realName, str)
    Object.__init__(self, realName)
    object.__setattr__(self, '__real_name__', realName)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    A mistaken alias must fail as the class is created, not at the first
    access.

    Parameters
    ----------

    owner : type
      The class being created.

    name : str
      The name of the alias.

    Raises
    ------

    DanglingAlias
      No class holds the real name, or it is the alias's own name.

    NotADescriptor
      The real name holds a plain value.
    """
    Object.__set_name__(self, owner, name, **kwargs)
    descriptor = self._getDescriptor(owner)
    if descriptor is self:
      raise DanglingAlias(self, self._getRealName(), owner)

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    if instance is None:
      return self
    return self._getDescriptor(owner).__get__(instance, owner)

  def __set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    A write through the alias must be the write through the real name.

    Parameters
    ----------

    instance : Any
      The instance written through.

    value : Any
      The value assigned.

    Raises
    ------

    ReadOnlyError
      The descriptor takes no write, as a plain function takes none.
    """
    descriptor = self._getDescriptor(type(instance))
    try:
      _ = type.__getattribute__(type(descriptor), '__set__')
    except AttributeError:
      raise ReadOnlyError(instance, self, value)
    descriptor.__set__(instance, value)

  def __delete__(self, instance: Any, **kwargs) -> None:
    """
    A deletion through the alias must be the deletion through the real
    name.

    Parameters
    ----------

    instance : Any
      The instance deleted through.

    Raises
    ------

    ProtectedError
      The descriptor takes no deletion, as a plain function takes none.
    """
    descriptor = self._getDescriptor(type(instance))
    try:
      _ = type.__getattribute__(type(descriptor), '__delete__')
    except AttributeError:
      raise ProtectedError(instance, self)
    descriptor.__delete__(instance)
