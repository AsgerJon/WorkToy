"""
Alias re-exposes a descriptor under a second name.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import Object
from ..waitaminute import MissingVariable, TypeException
from ..waitaminute.desc import NotADescriptor, NotAliasable
from ..waitaminute.desc import DanglingAlias

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional


class Alias(Object):
  """
  Alias is a descriptor that re-exposes a descriptor of its class, or of
  a base, under a second name:

    class Geometry(BaseObject):
      width = AttriBox[int](240)
      w = Alias('width')

  Through an instance, the alias forwards each read, write and deletion
  to the descriptor the real name holds on the class of that instance.
  The descriptor is found afresh at every access, as the first class
  dict along the resolution order holds it, with no '__get__' run on it,
  and the alias then runs that protocol once itself. So 'g.w' is the
  very object 'g.width' gives, and a subclass that redeclares the field
  is served by its own box whichever name is read first. Through the
  class, the alias is itself.

  As the class is created, the alias is held to what it stands for. A
  name no class along the resolution order holds is refused with
  'DanglingAlias'; a name holding something that is not a descriptor, a
  plain value, with 'NotADescriptor', since there is no protocol to
  forward to, and a plain value takes a second name by assignment; and a
  descriptor the class does not read as itself, a 'staticmethod' or a
  'classmethod', with 'NotAliasable', since the two names would not
  agree on what the class gives. A plain function is read as itself and
  may be aliased. The first two refusals come again from an access,
  should the name be removed or replaced on the class afterwards.
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
    The '_getDescriptor' method returns the descriptor the real name holds
    on 'owner' or a base of it, as the class dict holds it, with no
    '__get__' run on it yet, or raises 'NotADescriptor' when the name
    holds something else.
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
    self.__real_name__ = realName

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    The '__set_name__' method records the owner and the name, then holds
    the alias to what it stands for: a name no class holds, a name
    holding no descriptor, and a descriptor the class does not read as
    itself are each refused.
    """
    Object.__set_name__(self, owner, name, **kwargs)
    realName: str = self._getRealName()
    expected = self._getDescriptor(owner)
    try:
      actual = type.__getattribute__(owner, realName)
    except AttributeError:
      raise DanglingAlias(self, realName, owner)
    else:
      if expected is not actual:
        raise NotAliasable(self, realName, expected, actual)

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    if instance is None:
      return self
    return self._getDescriptor(owner).__get__(instance, owner)

  def __set__(self, instance: Any, value: Any, **kwargs) -> None:
    self._getDescriptor(type(instance)).__set__(instance, value)

  def __delete__(self, instance: Any, **kwargs) -> None:
    self._getDescriptor(type(instance)).__delete__(instance)
