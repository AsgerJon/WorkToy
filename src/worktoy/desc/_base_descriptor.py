"""
BaseDescriptor adds access-notification hook decorators to a descriptor.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic, overload, Callable, Any
from types import FunctionType as Func

from ..utilities import maybe
from ..core import Object
from ..dispatch import flexCall
from ..waitaminute.desc import NamelessCallback, SharedDescriptor

T = TypeVar('T', )
#  A decorated callback keeps its own type for a checker.
F = TypeVar('F', bound=Callable[..., Any])

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Self, Union, Optional

  Keys: TypeAlias = tuple[str, ...]


class BaseDescriptor(Object, Generic[T]):
  """
  BaseDescriptor subclasses 'Object' and provides decorators for setting
  access notification callbacks. Each decorator may be applied to any
  number of methods; the callbacks are recorded by name in registration
  order and fire in that order. They are looked up by name on
  'type(instance)', so a subclass override is used in place of the
  original. Registering the same method name twice records it twice and
  fires it twice.

  A callback may declare fewer parameters than the descriptor passes it,
  and the positional arguments it does not declare are dropped. Each
  decorator returns the callback wrapped by 'flexCall' for this, so the
  wrapping happens once as the class body runs, and an override that was
  never decorated is wrapped as it is called. An override that is a
  classmethod is unwrapped to the function behind the bound method, as
  'hookSetName' does with the '@classmethod' it requires, and that
  function is then called as the plain method would be, the instance
  first; a bound method used to be refused by 'flexCall' on every
  access. A lambda, which has no name of its own, could never be found by
  name, so each decorator refuses one with 'NamelessCallback'; a callable
  with no '__name__' at all fails with the 'AttributeError' of reading
  the name. A private callback, written with
  two leading underscores, is recorded under the name the class body
  stores it at, '_Foo__seen' for '__seen' in 'Foo', so it is found as
  well; like any private name it is not overridden by a subclass, whose
  own '__seen' mangles to the subclass's name.

  A descriptor is placed on one class, as that class is created, and
  '__set_name__' decides what a second placement means for every
  descriptor based on this class: a second name in the same class body
  receives a clone made by 'clone', so the two names are two descriptors,
  and another class is refused with 'SharedDescriptor'.

  The following example illustrates an exhaustively decorated descriptor
  in a class body:

  class Foo(BaseObject):

    bar = BaseDescriptor()

    @bar.preGet
    def _preGetBar(self) -> None:
      # Triggered at the beginning of 'self.bar', before retrieval
      # of the underlying value. 'self' is the instance whose
      # attribute is being read.
      pass

    @bar.onGet
    def _onGetBar(self, returnValue: Any) -> None:
      # Triggered after 'self.bar' has produced 'returnValue', so
      # subclasses can observe what is about to be returned.
      pass

    @bar.preSet
    def _preSetBar(self, value: Any) -> None:
      # Triggered at the beginning of 'self.bar = value', before
      # the assignment is applied. 'value' is the incoming value.
      pass

    @bar.onSet
    def _onSetBar(self, value: Any) -> None:
      # Triggered after 'self.bar = value' has completed, with
      # 'value' equal to the value that was stored.
      pass

    @bar.preDelete
    def _preDeleteBar(self) -> None:
      # Triggered at the beginning of 'del self.bar'.
      pass

    @bar.onDelete
    def _onDeleteBar(self) -> None:
      # Triggered after 'del self.bar' has completed.
      pass

    @classmethod
    @bar.setName
    def _setNameBar(cls: type, desc: BaseDescriptor) -> None:
      # Triggered when the descriptor is assigned to a class body.
      # The callback must be a classmethod and receives the owning
      # class 'cls' and the descriptor 'desc'. No instance exists
      # at __set_name__ time, so there is no 'self'.
      pass

  Please note, that 'BaseDescriptor' does not implement any particular
  customization of the descriptor protocol. It inherits the 'Object'
  default behaviour, which is characterized by returning 'self' for all
  '__get__' calls, raising 'ReadOnlyError' for all '__set__' calls and
  'ProtectedError' for all '__delete__' calls.

  The 'BaseDescriptor' is intended to be subclassed by other descriptor
  classes. These should implement their functionality by overriding the
  three instance access methods defined on 'Object':

  __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any: ...
  __instance_set__(self, instance: Any, value: Any, **kwargs) -> Any: ...
  __instance_delete__(self, instance: Any, old: Any = None,
                      **kwargs) -> None: ...

  Care should be taken when implementing the native accessor methods:
  '__get__', '__set__' and '__delete__', as these are responsible for
  notifying the hooks on the 'Object' class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __pre_get_keys__: Optional[tuple[str, ...]] = None
  __on_get_keys__: Optional[tuple[str, ...]] = None
  __pre_set_keys__: Optional[tuple[str, ...]] = None
  __on_set_keys__: Optional[tuple[str, ...]] = None
  __pre_delete_keys__: Optional[tuple[str, ...]] = None
  __on_delete_keys__: Optional[tuple[str, ...]] = None
  __set_name_keys__: Optional[tuple[str, ...]] = None

  #  Public Variables

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Key getters

  def _getPreGetKeys(self) -> tuple[str, ...]:
    return maybe(self.__pre_get_keys__, ())

  def _getOnGetKeys(self) -> tuple[str, ...]:
    return maybe(self.__on_get_keys__, ())

  def _getPreSetKeys(self) -> tuple[str, ...]:
    return maybe(self.__pre_set_keys__, ())

  def _getOnSetKeys(self) -> tuple[str, ...]:
    return maybe(self.__on_set_keys__, ())

  def _getPreDeleteKeys(self) -> tuple[str, ...]:
    return maybe(self.__pre_delete_keys__, ())

  def _getOnDeleteKeys(self) -> tuple[str, ...]:
    return maybe(self.__on_delete_keys__, ())

  def _getSetNameKeys(self) -> tuple[str, ...]:
    return maybe(self.__set_name_keys__, ())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getCallbackName(self, role: str, callback: Any) -> str:
    """
    The '_getCallbackName' method returns the name a decorator records
    for 'callback', the name the hooks look it up by on the class of the
    instance, and raises 'NamelessCallback' for a lambda, named
    '<lambda>', which has no name of its own. A callable with no
    '__name__' at all raises the 'AttributeError' of reading it. 'role'
    is the name of the decorator, for the message.

    A private name, two leading underscores and not two trailing, is
    recorded as the class body stores it: '__audit' defined in 'Account'
    as '_Account__audit'. The class is the part of the callback's
    '__qualname__' before its own name; a private callback whose
    qualified name names no class, one made inside another function, is
    refused with 'NamelessCallback', since no lookup could find it.
    """
    name: str = object.__getattribute__(callback, '__name__')
    if name == '<lambda>':
      raise NamelessCallback(self, role, callback)
    if str.startswith(name, '__') and not str.endswith(name, '__'):
      qualName: str = object.__getattribute__(callback, '__qualname__')
      qualParts = str.split(qualName, '.')
      if len(qualParts) < 2 or qualParts[-2] == '<locals>':
        raise NamelessCallback(self, role, callback)
      className = str.lstrip(qualParts[-2], '_')
      if not className:
        #  Python mangles nothing in a class named with underscores alone.
        return name
      return '_%s%s' % (className, name)
    return name

  def preGet(self, callback: F) -> F:
    existing = self._getPreGetKeys()
    name = self._getCallbackName('preGet', callback)
    self.__pre_get_keys__ = (*existing, name)
    return flexCall(callback)

  def onGet(self, callback: F) -> F:
    existing = self._getOnGetKeys()
    name = self._getCallbackName('onGet', callback)
    self.__on_get_keys__ = (*existing, name)
    return flexCall(callback)

  def preSet(self, callback: F) -> F:
    existing = self._getPreSetKeys()
    name = self._getCallbackName('preSet', callback)
    self.__pre_set_keys__ = (*existing, name)
    return flexCall(callback)

  def onSet(self, callback: F) -> F:
    existing = self._getOnSetKeys()
    name = self._getCallbackName('onSet', callback)
    self.__on_set_keys__ = (*existing, name)
    return flexCall(callback)

  def preDelete(self, callback: F) -> F:
    existing = self._getPreDeleteKeys()
    name = self._getCallbackName('preDelete', callback)
    self.__pre_delete_keys__ = (*existing, name)
    return flexCall(callback)

  def onDelete(self, callback: F) -> F:
    existing = self._getOnDeleteKeys()
    name = self._getCallbackName('onDelete', callback)
    self.__on_delete_keys__ = (*existing, name)
    return flexCall(callback)

  def setName(self, callback: F) -> F:
    existing = self._getSetNameKeys()
    name = self._getCallbackName('setName', callback)
    self.__set_name_keys__ = (*existing, name)
    return flexCall(callback)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def clone(self) -> Self:
    """
    The 'clone' method returns a fresh descriptor of the same class
    carrying what this one captured, the constructor arguments, the field
    type of a box and every registered callback name, and no owner, field
    name or context. A class body decorating an inherited descriptor
    through 'THIS' takes its own copy this way, so the base keeps its
    descriptor as it was. The copy is made by hand, since a box answers
    'copy.copy' with itself.
    """
    cls = type(self)
    new = object.__new__(cls)
    skipped = (
      '__field_owner__',
      '__field_name__',
      '__private_name__',
      '__call_chain__',
    )
    for key, value in vars(self).items():
      if key in skipped:
        continue
      object.__setattr__(new, key, value)
    object.__setattr__(new, '__call_chain__', [])
    return new

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _findCallback(owner: type, key: str) -> Any:
    """
    The '_findCallback' method returns what 'owner' holds under 'key',
    read with 'type.__getattribute__' so that no '__getattr__',
    '__class_getattr__' or reimplemented '__getattribute__' of the owner
    can answer in its place. A bound method, as a classmethod gives, is
    unwrapped to the function behind it.
    """
    callback = type.__getattribute__(owner, key)
    try:
      return object.__getattribute__(callback, '__func__')
    except AttributeError:
      return callback

  @staticmethod
  def _getCallback(owner: type, key: str) -> Func:
    """
    The '_getCallback' method returns the callback registered under
    'key' as 'owner' holds it, found by '_findCallback', wrapped by
    'flexCall'. A bound method, as a classmethod gives, is unwrapped to
    the function behind it, as 'hookSetName' does, so an override of that
    kind is called as the plain method would be.
    """
    return flexCall(BaseDescriptor._findCallback(owner, key))

  def hookPreGet(self, instance: Any, **kwargs) -> None:
    keys = self._getPreGetKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      self._getCallback(owner, key)(instance, **kwargs)

  def hookOnGet(self, instance: Any, value: Any, **kwargs) -> None:
    keys = self._getOnGetKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      self._getCallback(owner, key)(instance, value, **kwargs)

  def hookPreSet(self, instance: Any, value: Any, **kwargs) -> None:
    keys = self._getPreSetKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      self._getCallback(owner, key)(instance, value, **kwargs)

  def hookOnSet(self, instance: Any, value: Any, **kwargs) -> None:
    keys = self._getOnSetKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      self._getCallback(owner, key)(instance, value, **kwargs)

  def hookPreDelete(self, instance: Any, **kwargs) -> None:
    keys = self._getPreDeleteKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      self._getCallback(owner, key)(instance, **kwargs)

  def hookOnDelete(self, instance: Any, **kwargs) -> None:
    keys = self._getOnDeleteKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      self._getCallback(owner, key)(instance, **kwargs)

  def hookSetName(self, owner: type, name: str, **kwargs) -> None:
    for key in self._getSetNameKeys():
      self._findCallback(owner, key)(owner, self, **kwargs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    The '__set_name__' method records the class and the name, as 'Object'
    does, for a descriptor not placed yet, and decides, for every
    descriptor based on this class, what a second placement means. Bound
    to a second name in the same class body, as in
    'width = height = AttriBox[int](0)', the descriptor keeps its first
    name and places a clone of itself, made by 'clone', at the second, so
    the two names are two descriptors. Placed on another class, as one
    object bound in the bodies of two classes, it is refused with
    'SharedDescriptor', since it cannot serve two classes.
    """
    placedOwner: Optional[type] = self.__field_owner__
    if placedOwner is not None:
      placedName = self.__field_name__
      if placedOwner is not owner:
        raise SharedDescriptor(self, placedOwner, placedName, owner, name)
      if placedName != name:
        #  'type.__new__' runs '__set_name__' over a copy of the class
        #  dict, so the second name may take the clone here.
        clone = self.clone()
        type.__setattr__(owner, name, clone)
        return clone.__set_name__(owner, name, **kwargs)
    return super().__set_name__(owner, name, **kwargs)

  # @formatter:off
  if TYPE_CHECKING:  # pragma: no cover
    @overload
    def __get__(self, instance: None, owner: type) -> Self: ...
    @overload
    def __get__(self, instance: Any, owner: type) -> T: ...

    def __get__(self, instance: Any, owner: type) -> Union[Any, T]:
      return super().__get__(instance, owner)

    #  Writes require T statically, so type-checked callers are held
    #  to the field type. Runtime salvage still rescues dynamic or
    #  untyped callers that pass something coercible.
    # noinspection PyMethodOverriding
    def __set__(self, instance: Any, value: Any) -> None: ...
  # @formatter:on
