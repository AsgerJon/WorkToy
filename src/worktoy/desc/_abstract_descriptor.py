"""AbstractDescriptor subclasses the CoreDescriptor and expands the basic
descriptor functionality with the following functionalities:

 - Notification hooks for each accessor
 - Instance specific silencing of notifications
 - Global suppression of notifications by the descriptor instance
 - The basic accessor methods '__get__', '__set__' and '__delete__' are
 replaced with explicit methods, except for '__get__' which returns the
 descriptor instance itself, when the owning instance passed to it is
 None. This is the case when the descriptor is accessed on the owning
 class directly. This distinction is important, as it is the only way to
 reach the actual descriptor instance.
  - Subclasses should implement the instance specific accessor functions
  as appropriate for their intended function. Only the '__instance_get__'
  is strictly required. The other methods will raise a TypeError if
  invoked. Subclasses are free to reimplement this.
  - This class implements the notification mechanisms leaving subclasses
  with the above instance specific accessors.
  - The notification system requires that owning class should decorate the
  methods it wishes to be notified of with the ONGET, ONSET and ONDEL
  decorators.

"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable

from worktoy.desc import CoreDescriptor
from worktoy.parse import maybe
from worktoy.text import monoSpace

try:
  from typing import Never
except ImportError:
  Never = object


class AbstractDescriptor(CoreDescriptor):
  """AbstractDescriptor provides common boilerplate for descriptor
  classes. """
  __on_set_callbacks__ = None
  __pre_set_callbacks__ = None
  __on_del_callbacks__ = None
  __pre_del_callbacks__ = None
  __pre_get_callbacks__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Wrapper factories

  @staticmethod
  def wrapGet(callMeMaybe: Callable) -> Callable:
    """This method creates a flexible wrapper for the using the callable
    as a getter. """

    def wrapper(instance: object, value: object) -> Any:
      """Wrapper function handling the notification. The wrapper first
      tries passing the instance and values to the given callable. If the
      callable raises a TypeError relating to 'positional arguments', it
      will then attempt to call with only the instance. """
      try:
        return callMeMaybe(instance, value)
      except TypeError as typeError:
        if 'positional arguments' in str(typeError):
          try:
            return callMeMaybe(value)
          except Exception as exception:
            raise exception from typeError
        else:
          raise typeError

    return wrapper

  @staticmethod
  def wrapDel(callMeMaybe: Callable) -> Callable:
    """Wrapper function for the deleter notifier."""

    def wrapper(instance: object, value: object) -> None:
      """Wrapper function handling the notification. The wrapper first
      tries passing the instance and values to the given callable. If the
      callable raises a TypeError relating to 'positional arguments', it
      will then attempt to call with only the instance. """
      try:
        callMeMaybe(instance, value)
      except TypeError as typeError:
        if 'positional arguments' in str(typeError):
          try:
            callMeMaybe(value)
          except Exception as exception:
            raise exception from typeError
        else:
          raise typeError

    return wrapper

  @staticmethod
  def wrapSet(callMeMaybe: Callable) -> Callable:
    """This method creates a flexible wrapper for the using the callable
    as a setter. """

    def wrapper(instance: object, oldVal: object, newVal: object) -> None:
      """Wrapper function handling the notification. The wrapper first
      tries passing the instance, old value and new value to the given
      callable. If the callable raises a TypeError relating to 'positional
      arguments', it will then attempt to call with only the instance and
      the new value. """
      try:
        callMeMaybe(instance, oldVal, newVal)
      except TypeError as typeError:
        if 'positional arguments' in str(typeError):
          try:
            callMeMaybe(instance, newVal)
          except Exception as exception:
            raise exception from typeError
        else:
          raise typeError

    return wrapper

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Getter-functions for notification callbacks

  def _onSetCallbacks(self, ) -> tuple[Callable, ...]:
    """This method returns the set callbacks."""
    return maybe(self.__on_set_callbacks__, [])

  def _preSetCallbacks(self, ) -> tuple[Callable, ...]:
    """This method returns the set callbacks."""
    return maybe(self.__pre_set_callbacks__, [])

  def _onDelCallbacks(self, ) -> tuple[Callable, ...]:
    """This method returns the set callbacks."""
    return maybe(self.__on_del_callbacks__, [])

  def _preDelCallbacks(self, ) -> tuple[Callable, ...]:
    """This method returns the set callbacks."""
    return maybe(self.__pre_del_callbacks__, [])

  def _preGetCallbacks(self, ) -> tuple[Callable, ...]:
    """This method returns the set callbacks."""
    return maybe(self.__pre_get_callbacks__, [])

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Append-functions for notification callbacks

  def _addPreSetCallback(self, callMeMaybe: Callable) -> None:
    """Registers the given callable to receive notifications when the
    value is about to change. """

    preSetCallbacks = self._preSetCallbacks()
    wrapper = self.wrapSet(callMeMaybe)
    self.__pre_set_callbacks__ = [*preSetCallbacks, wrapper]

  def _addOnSetCallback(self, callMeMaybe: Callable) -> None:
    """Registers the given callable to receive notifications when the
    value has changed. """

    onSetCallbacks = self._onSetCallbacks()
    wrapper = self.wrapSet(callMeMaybe)
    self.__on_set_callbacks__ = [*onSetCallbacks, wrapper]

  def _addPreDelCallback(self, callMeMaybe: Callable) -> None:
    """Registers the given callable to receive notifications when the
    value is about to be deleted. """

    preDelCallbacks = self._preDelCallbacks()
    wrapper = self.wrapDel(callMeMaybe)
    self.__pre_del_callbacks__ = [*preDelCallbacks, wrapper]

  def _addOnDelCallback(self, callMeMaybe: Callable) -> None:
    """Registers the given callable to receive notifications when the
    value has been deleted. """

    onDelCallbacks = self._onDelCallbacks()
    wrapper = self.wrapDel(callMeMaybe)
    self.__on_del_callbacks__ = [*onDelCallbacks, wrapper]

  def _addPreGetCallback(self, callMeMaybe: Callable) -> None:
    """Registers the given callable to receive notifications when the
    value is about to be accessed. """

    preGetCallbacks = self._preGetCallbacks()
    wrapper = self.wrapGet(callMeMaybe)
    self.__pre_get_callbacks__ = [*preGetCallbacks, wrapper]

  @staticmethod
  def _addOnGetCallback(*_) -> Never:
    """It is not possible to be notified 'after' the getter has returned!"""
    e = """It is not possible to be notified 'after' the getter has 
    returned!"""
    raise TypeError(monoSpace(e))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Decorators for subscribing to the notifications

  @staticmethod
  def ONGET(*_) -> Never:
    """It is not possible to be notified 'after' the getter has returned!"""
    e = """It is not possible to be notified 'after' the getter has 
    returned!"""
    raise TypeError(monoSpace(e))

  def ONSET(self, callMeMaybe: Callable) -> Callable:
    """Decorator for subscribing to the setter."""
    self._addOnSetCallback(callMeMaybe)
    return callMeMaybe

  def ONDEL(self, callMeMaybe: Callable) -> Callable:
    """Decorator for subscribing to the deleter."""
    self._addOnDelCallback(callMeMaybe)
    return callMeMaybe

  def PREGET(self, callMeMaybe: Callable) -> Callable:
    """Decorator for subscribing to the pre-getter."""
    self._addPreGetCallback(callMeMaybe)
    return callMeMaybe

  def PRESET(self, callMeMaybe: Callable) -> Callable:
    """Decorator for subscribing to the pre-setter."""
    self._addPreSetCallback(callMeMaybe)
    return callMeMaybe

  def PREDEL(self, callMeMaybe: Callable) -> Callable:
    """Decorator for subscribing to the pre-deleter."""
    self._addPreDelCallback(callMeMaybe)
    return callMeMaybe

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Dispatcher methods for the notifications

  @staticmethod
  def notifyOnGET(*_) -> Never:
    """It is not possible to be notified 'after' the getter has returned!"""
    e = """It is not possible to be notified 'after' the getter has 
    returned!"""
    raise TypeError(monoSpace(e))

  def notifyPreGet(self, instance: object, *values) -> None:
    """Dispatches the pre-get notifications."""
    for callMeMaybe in self._preGetCallbacks():
      callMeMaybe(instance, *values)

  def notifyOnSet(self, instance: object, *values) -> None:
    """Dispatches the on-set notifications."""
    for callMeMaybe in self._onSetCallbacks():
      callMeMaybe(instance, *values)

  def notifyPreSet(self, instance: object, *values) -> None:
    """Dispatches the pre-set notifications."""
    for callMeMaybe in self._preSetCallbacks():
      callMeMaybe(instance, *values)

  def notifyOnDel(self, instance: object, *values) -> None:
    """Dispatches the on-del notifications."""
    for callMeMaybe in self._onDelCallbacks():
      callMeMaybe(instance, *values)

  def notifyPreDel(self, instance: object, *values) -> None:
    """Dispatches the pre-del notifications."""
    for callMeMaybe in self._preDelCallbacks():
      callMeMaybe(instance, *values)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Implementation of the descriptor protocol

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Get the value of the field."""
    if instance is None:
      return self
    try:
      value = self.__instance_get__(instance)
    except Exception as exception:
      if kwargs.get('_setterAsks', False):
        return None
      else:
        raise exception
    if kwargs.get('_setterAsks', False):
      return value
    self.notifyPreGet(instance, value)
    return value

  def __set__(self, instance: object, value: object) -> None:
    """Set the value of the field."""
    oldValue = self.__get__(instance, type(instance), _setterAsks=True)
    self.notifyPreSet(instance, oldValue, value)
    self.__instance_set__(instance, value)
    self.notifyOnSet(instance, oldValue, value)

  def __delete__(self, instance: object) -> None:
    """Delete the value of the field."""
    value = self.__get__(instance, type(instance), _setterAsks=True)
    self.notifyPreDel(instance, value)
    self.__instance_del__(instance)
    self.notifyOnDel(instance, value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Instance-specific accessor methods

  @abstractmethod
  def __instance_get__(self, instance: object) -> Any:
    """Subclasses should implement this method to provide the getter. """

  def __instance_set__(self, instance: object, value: object) -> None:
    """Subclasses should implement this method to provide the setter. """
    descName = self.__class__.__name__
    ownerName = self.getFieldOwner().__name__
    fieldName = self.getFieldName()
    e = """The attribute '%s' on class '%s' belongs to descriptor of type: 
    '%s' which does not implement setting!"""
    raise TypeError(monoSpace(e % (fieldName, ownerName, descName)))

  def __instance_del__(self, instance: object) -> None:
    """Subclasses should implement this method to provide the deleter. """
    descName = self.__class__.__name__
    ownerName = self.getFieldOwner().__name__
    fieldName = self.getFieldName()
    e = """The attribute '%s' on class '%s' belongs to descriptor of type: 
    '%s' which does not implement deletion!"""
    raise TypeError(monoSpace(e % (fieldName, ownerName, descName)))
