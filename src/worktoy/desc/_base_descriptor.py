"""
BaseDescriptor subclasses 'Object' and provides decorators for setting
access notification callbacks.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from inspect import signature
from typing import TYPE_CHECKING

from worktoy.core import Object
from worktoy.utilities import maybe, argsCount, takesKwargs

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias

  from . import BaseDescriptor

  Keys: TypeAlias = tuple[str, ...]

  GetCallback: TypeAlias = Callable[[BaseDescriptor, Any], None]
  SetCallback: TypeAlias = Callable[[BaseDescriptor, Any], None]
  DeleteCallback: TypeAlias = Callable[[BaseDescriptor, ], None]


class BaseDescriptor(Object):
  """
  BaseDescriptor subclasses 'Object' and provides decorators for setting
  access notification callbacks. Each decorator may be applied to as many
  methods as desired. The functions are identified by name, and when a
  particular instance is accessed, the callbacks are retrieved from the
  'type(...)' of that instance.

  The following examples illustrates an exhaustively decorated descriptor
  in a class body:

  class Foo:

    bar = BaseDescriptor()

    @bar.preGet
    def _preGetBar(self, returnValue: Any ) -> None:
      # Triggered at the beginning of 'self.bar'. This allows early
      # detection of bad values or types.
      pass

    @bar.onGet
    def _onGetBar(self, returnValue: Any ) -> None:
      # Triggered when self.bar is accessed. 'self' is the instance passed
      # to '__get__' and 'returnValue' is the return value.
      pass

    @bar.preSet
    def _preSetBar(self, value: Any) -> None:
      # Triggered at the beginning of 'self.bar = value'. This allows
      # early detection of bad values or types. The 'value' argument is
      # what will be attempted set.
      pass

    @bar.onSet
    def  _onSetBar(self, value: Any) -> None:
      # Triggered *after* 'self.bar = value' has been executed. This
      # allows potential side effects to have been triggered before the
      # callback.
      pass

    @bar.preDelete
    def _onDeleteBar(self) -> None:
      # Triggered at the beginning of 'del self.bar'. This allows early
      # detection of bad values or types. The 'value' argument is what will
      # be attempted set.
      pass

    @bar.onDelete
    def _onDeleteBar(self) -> None:
      # Triggered *after* 'del self.bar' has been executed. This allows
      # potential side effects to have been triggered before the callback.
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
  __pre_get_keys__ = None
  __on_get_keys__ = None
  __pre_set_keys__ = None
  __on_set_keys__ = None
  __pre_delete_keys__ = None
  __on_delete_keys__ = None

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

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def preGet(self, callback: GetCallback) -> GetCallback:
    existing = self._getPreGetKeys()
    self.__pre_get_keys__ = (*existing, callback.__name__)
    return callback

  def onGet(self, callback: GetCallback) -> GetCallback:
    existing = self._getOnGetKeys()
    self.__on_get_keys__ = (*existing, callback.__name__)
    return callback

  def preSet(self, callback: SetCallback) -> SetCallback:
    existing = self._getPreSetKeys()
    self.__pre_set_keys__ = (*existing, callback.__name__)
    return callback

  def onSet(self, callback: SetCallback) -> SetCallback:
    existing = self._getOnSetKeys()
    self.__on_set_keys__ = (*existing, callback.__name__)
    return callback

  def preDelete(self, callback: DeleteCallback) -> DeleteCallback:
    existing = self._getPreDeleteKeys()
    self.__pre_delete_keys__ = (*existing, callback.__name__)
    return callback

  def onDelete(self, callback: DeleteCallback) -> DeleteCallback:
    existing = self._getOnDeleteKeys()
    self.__on_delete_keys__ = (*existing, callback.__name__)
    return callback

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def hookPreGet(self, instance: Any, **kwargs, ) -> None:
    owner = type(instance)
    for key in self._getPreGetKeys():
      callback = getattr(owner, key)
      args = (instance,)[:min(1, argsCount(callback))]
      kwargsFlag = takesKwargs(callback)
      if kwargsFlag:
        callback(*args, **kwargs)
      else:
        callback(*args)

  def hookOnGet(self, instance: Any, value: Any, **kwargs, ) -> None:
    owner = type(instance)
    for key in self._getOnGetKeys():
      callback = getattr(owner, key)
      args = (instance, value)[:min(2, argsCount(callback))]
      kwargsFlag = takesKwargs(callback)
      if kwargsFlag:
        callback(*args, **kwargs)
      else:
        callback(*args)

  def hookPreSet(self, instance: Any, value: Any, **kwargs, ) -> None:
    owner = type(instance)
    for key in self._getPreSetKeys():
      callback = getattr(owner, key)
      args = (instance, value)[:min(2, argsCount(callback))]
      kwargsFlag = takesKwargs(callback)
      if kwargsFlag:
        callback(*args, **kwargs)
      else:
        callback(*args)

  def hookOnSet(self, instance: Any, value: Any, **kwargs, ) -> None:
    owner = type(instance)
    for key in self._getOnSetKeys():
      callback = getattr(owner, key)
      args = (instance, value)[:min(2, argsCount(callback))]
      kwargsFlag = takesKwargs(callback)
      if kwargsFlag:
        callback(*args, **kwargs)
      else:
        callback(*args)

  def hookPreDelete(self, instance: Any, **kwargs, ) -> None:
    owner = type(instance)
    for key in self._getPreDeleteKeys():
      callback = getattr(owner, key)
      args = (instance,)[:min(1, argsCount(callback))]
      kwargsFlag = takesKwargs(callback)
      if kwargsFlag:
        callback(*args, **kwargs)
      else:
        callback(*args)

  def hookOnDelete(self, instance: Any, **kwargs, ) -> None:
    owner = type(instance)
    for key in self._getOnDeleteKeys():
      callback = getattr(owner, key)
      args = (instance,)[:min(1, argsCount(callback))]
      kwargsFlag = takesKwargs(callback)
      if kwargsFlag:
        callback(*args, **kwargs)
      else:
        callback(*args)
