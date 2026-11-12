"""
Field is a property-like descriptor whose accessors are methods decorated
in the class body.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Callable, Any

from . import BaseDescriptor
from ..utilities import maybe
from ..waitaminute import TypeException
from ..waitaminute.desc import ProtectedError, ReadOnlyError, AccessError

T = TypeVar('T')
#  A decorated accessor keeps its own type for a checker.
F = TypeVar('F', bound=Callable[..., Any])

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Self


class Field(BaseDescriptor[T]):
  """
  An attribute computed or guarded by methods of the class, as a
  'property' is, must let a subclass change those methods by overriding
  them, with no need to declare the attribute again; a 'property' holds
  the very functions it was given and does not follow an override. The
  attribute must also take the notification decorators every worktoy
  descriptor takes.

    class Circle(BaseObject):

      radius = Field()

      @radius.GET
      def _getRadius(self) -> float:
        return self.__radius__

  Implementation
  --------------

  'GET' records one getter, a second one replacing the first; 'SET' and
  'DELETE' record any number of setters and deleters, run in order. Each
  is recorded by name and found on the class of the instance at every
  access, so an override is found, and called by its kind, as Python
  would call 'instance.name()': a method with the instance, a classmethod
  with the class, a staticmethod with nothing, plus the value for a
  setter, and nothing else, no surplus being cut. Anything with no
  function to look up by name is refused with 'TypeException', and a
  lambda has no name to look up and is refused; a private name is
  recorded mangled. Without a getter a read raises 'AccessError', without
  a setter a write raises 'ReadOnlyError', without a deleter a deletion
  raises 'ProtectedError'. The decorators return the method unchanged.
  'Field(other)' copies another field.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  # -- Accessor Keys
  __get_key__ = None
  __set_keys__ = None
  __delete_keys__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getGetterKey(self) -> str:
    if self.__get_key__ is None:
      raise AccessError(self)
    if isinstance(self.__get_key__, str):
      return self.__get_key__
    raise TypeException('__get_key__', self.__get_key__, str)

  def _getSetterKeys(self, ) -> tuple[str, ...]:
    return (*[k for k in maybe(self.__set_keys__, ()) if k],)

  def _getDeleterKeys(self) -> tuple[str, ...]:
    return (*[k for k in maybe(self.__delete_keys__, ()) if k],)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def GET(self, callMeMaybe: F) -> F:
    """
    The field needs the method answering a read.

    Parameters
    ----------

    callMeMaybe : F
      The method, called as 'method(self)'.

    Returns
    -------

    F
      The same method.
    """
    name = self._getCallbackName('GET', callMeMaybe)
    object.__setattr__(self, '__get_key__', name)
    return callMeMaybe

  def SET(self, callMeMaybe: F) -> F:
    """
    The field needs the methods performing a write, if it takes writes.

    Parameters
    ----------

    callMeMaybe : F
      The method, called as 'method(self, value)' with the value as
      assigned.

    Returns
    -------

    F
      The same method.
    """
    existing = maybe(self.__set_keys__, ())
    name = self._getCallbackName('SET', callMeMaybe)
    object.__setattr__(self, '__set_keys__', (*existing, name,))
    return callMeMaybe

  def DELETE(self, callMeMaybe: F) -> F:
    """
    The field needs the methods performing a deletion, if it takes
    deletions. A deleter storing 'DELETED' where the getter reads makes
    the next read raise 'MissingVariable'.

    Parameters
    ----------

    callMeMaybe : F
      The method, called as 'method(self)'.

    Returns
    -------

    F
      The same method.
    """
    existing = maybe(self.__delete_keys__, ())
    name = self._getCallbackName('DELETE', callMeMaybe)
    object.__setattr__(self, '__delete_keys__', (*existing, name,))
    return callMeMaybe

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    A read must reach the getter as the class of the instance defines it.

    Implementation
    --------------

    The getter is found by name on 'owner' and called by its kind, as
    'BaseDescriptor._bindCallback' binds it. A read made by a deletion goes
    to '_peekValue'.

    Parameters
    ----------

    instance : Any
      The instance read through.

    owner : type
      The class read through.

    Returns
    -------

    Any
      What the getter returns.

    Raises
    ------

    AccessError
      No getter is marked.
    """
    if kwargs.get('_deleting', False):
      return self._peekValue(instance, owner)
    getterKey = self._getGetterKey()
    return self._bindCallback(instance, owner, getterKey)()

  def _peekValue(self, instance: Any, owner: type) -> Any:
    """
    A deletion reports the current value, and a getter that raises, as one
    for a value not ready yet may, must not stop the deleters from
    running.

    Implementation
    --------------

    Any 'Exception' from the getter gives 'None', here and only here.
    """
    try:
      getterKey = self._getGetterKey()
      return self._bindCallback(instance, owner, getterKey)()
    except Exception:
      return None

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    A write must reach every setter as the class of the instance defines
    it.

    Parameters
    ----------

    instance : Any
      The instance written through.

    value : Any
      The value assigned.

    Raises
    ------

    ReadOnlyError
      No setter is marked.
    """
    setterKeys = self._getSetterKeys()
    owner = type(instance)
    if not setterKeys:
      raise ReadOnlyError(instance, self, value, )
    for key in setterKeys:
      self._bindCallback(instance, owner, key)(value, )

  def __instance_delete__(
      self,
      instance: Any,
      old: Any = None,
      **kwargs,
  ) -> None:
    """
    A deletion must reach every deleter as the class of the instance
    defines it.

    Parameters
    ----------

    instance : Any
      The instance deleted through.

    old : Any
      The value '_peekValue' reported.

    Raises
    ------

    ProtectedError
      No deleter is marked.
    """
    deleterKeys = self._getDeleterKeys()
    owner = type(instance)
    if not deleterKeys:
      raise ProtectedError(instance, self, old)
    for key in deleterKeys:
      self._bindCallback(instance, owner, key)(**kwargs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, other: Self = None) -> None:
    BaseDescriptor.__init__(self, other)
    if isinstance(other, Field):
      getKey = object.__getattribute__(other, '__get_key__')
      object.__setattr__(self, '__get_key__', getKey)
      keyGroups = (
        '__pre_get_keys__',
        '__on_get_keys__',
        '__pre_set_keys__',
        '__on_set_keys__',
        '__pre_delete_keys__',
        '__on_delete_keys__',
        '__set_name_keys__',
        '__set_keys__',
        '__delete_keys__',
      )
      for keyGroup in keyGroups:
        otherValue = object.__getattribute__(other, keyGroup)
        if otherValue is not None:
          object.__setattr__(self, keyGroup, (*otherValue,))
    elif other is not None:
      raise TypeException('other', other, type(self))
