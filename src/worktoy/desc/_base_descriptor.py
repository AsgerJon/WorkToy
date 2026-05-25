"""
BaseDescriptor subclasses 'Object' and provides decorators for setting
access notification callbacks.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic, overload
from types import FunctionType as Func

from ..utilities import maybe
from ..core import Object
from ..dispatch import flexCall

T = TypeVar('T', )

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias, Self, Union, Optional

  Keys: TypeAlias = tuple[str, ...]


class BaseDescriptor(Object, Generic[T]):
  """
  BaseDescriptor subclasses 'Object' and provides decorators for setting
  access notification callbacks. Each decorator may be applied to as many
  methods as desired. The functions are identified by name, and when a
  particular instance is accessed, the callbacks are retrieved from the
  'type(...)' of that instance.

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

  __instance_get__(self, instance: Any, owner: type) -> Any: ...
  __instance_set__(self, instance: Any, value: Any) -> None: ...
  __instance_delete__(self, instance: Any) -> None: ...

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

  def preGet(self, callback: Func) -> Func:
    existing = self._getPreGetKeys()
    self.__pre_get_keys__ = (*existing, callback.__name__)
    return callback

  def onGet(self, callback: Func) -> Func:
    existing = self._getOnGetKeys()
    self.__on_get_keys__ = (*existing, callback.__name__)
    return callback

  def preSet(self, callback: Func) -> Func:
    existing = self._getPreSetKeys()
    self.__pre_set_keys__ = (*existing, callback.__name__)
    return callback

  def onSet(self, callback: Func) -> Func:
    existing = self._getOnSetKeys()
    self.__on_set_keys__ = (*existing, callback.__name__)
    return callback

  def preDelete(self, callback: Func) -> Func:
    existing = self._getPreDeleteKeys()
    self.__pre_delete_keys__ = (*existing, callback.__name__)
    return callback

  def onDelete(self, callback: Func) -> Func:
    existing = self._getOnDeleteKeys()
    self.__on_delete_keys__ = (*existing, callback.__name__)
    return callback

  def setName(self, callback: Func) -> Func:
    existing = self._getSetNameKeys()
    self.__set_name_keys__ = (*existing, callback.__name__)
    return flexCall(callback)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def hookPreGet(self, instance: Any, **kwargs) -> None:
    keys = self._getPreGetKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      flexCall(getattr(owner, key))(instance, **kwargs)

  def hookOnGet(self, instance: Any, value: Any, **kwargs) -> None:
    keys = self._getOnGetKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      flexCall(getattr(owner, key))(instance, value, **kwargs)

  def hookPreSet(self, instance: Any, value: Any, **kwargs) -> None:
    keys = self._getPreSetKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      flexCall(getattr(owner, key))(instance, value, **kwargs)

  def hookOnSet(self, instance: Any, value: Any, **kwargs) -> None:
    keys = self._getOnSetKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      flexCall(getattr(owner, key))(instance, value, **kwargs)

  def hookPreDelete(self, instance: Any, **kwargs) -> None:
    keys = self._getPreDeleteKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      flexCall(getattr(owner, key))(instance, **kwargs)

  def hookOnDelete(self, instance: Any, **kwargs) -> None:
    keys = self._getOnDeleteKeys()
    if not keys:
      return
    owner = type(instance)
    for key in keys:
      flexCall(getattr(owner, key))(instance, **kwargs)

  def hookSetName(self, owner: type, name: str, **kwargs) -> None:
    for key in self._getSetNameKeys():
      callback = getattr(owner, key)
      callback = getattr(callback, '__func__', callback)
      callback(owner, self, **kwargs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # @formatter:off
  if TYPE_CHECKING:  # pragma: no cover
    @overload
    def __get__(self, instance: None, owner: type) -> Self: ...
    @overload
    def __get__(self, instance: Any, owner: type) -> T: ...

    def __get__(self, instance: Any, owner: type) -> Union[Self, T]:
      return super().__get__(instance, owner)

    #  Writes require T statically, so type-checked callers are held
    #  to the field type. Runtime salvage still rescues dynamic or
    #  untyped callers that pass something coercible.
    # noinspection PyMethodOverriding
    def __set__(self, instance: Any, value: T) -> None: ...
  # @formatter:on
