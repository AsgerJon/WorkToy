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
  - Additionally, the reset method is available, however only by the
  awkward syntax of first accessing it through the owning class.
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
from typing import Any

from worktoy.desc import MissingValueException, CoreDescriptor
from worktoy.parse import maybe
from worktoy.text import monoSpace


class AbstractDescriptor(CoreDescriptor):
  """AbstractDescriptor provides common boilerplate for descriptor
  classes. """

  __get_subscribers__ = None
  __set_subscribers__ = None
  __del_subscribers__ = None
  __suppress_notification__ = None
  __silenced_instances__ = None

  def getSilencedInstances(self) -> list:
    return maybe(self.__silenced_instances__, [])

  def silenceInstance(self, instance: object) -> None:
    silencedInstances = self.getSilencedInstances()
    if instance in silencedInstances:
      e = """Tried to silence '%s' which was already silenced!"""
      raise AttributeError(e % str(instance))
    self.__silenced_instances__ = [*silencedInstances, instance]

  def unsilenceInstance(self, instance: object) -> None:
    silencedInstances = self.getSilencedInstances()
    self.__silenced_instances__ = []
    while silencedInstances:
      silencedInstance = silencedInstances.pop()
      if silencedInstance is instance:
        while silencedInstances:
          self.silenceInstance(silencedInstances.pop())
        break
    else:
      e = """Tried to unsilence '%s' which was not silenced!"""
      raise AttributeError(e % str(instance))

  def isSilenced(self, instance: object) -> bool:
    silencedInstances = self.getSilencedInstances()
    return True if instance in silencedInstances else False

  def pauseNotifications(self) -> None:
    """Suppress notification for the descriptor."""
    self.__suppress_notification__ = True

  def resumeNotifications(self) -> None:
    """Resume notification for the descriptor."""
    self.__suppress_notification__ = None

  def notifyGet(self, instance: object, value: object) -> None:
    if self.__suppress_notification__ or self.isSilenced(instance):
      return
    for callMeMaybe in self._getGetSubscribers():
      try:
        callMeMaybe(instance, value)
      except TypeError as typeError:
        if 'positional argument' in str(typeError):
          try:
            callMeMaybe(value)
          except Exception as exception:
            raise exception from typeError

  def notifySet(self,
                instance: object,
                oldValue: object,
                newValue: object) -> None:
    if self.__suppress_notification__ or self.isSilenced(instance):
      return
    for callMeMaybe in self._getSetSubscribers():
      try:
        callMeMaybe(instance, oldValue, newValue)
      except TypeError as typeError:
        if 'positional argument' in str(typeError):
          try:
            callMeMaybe(instance, newValue)
          except TypeError as typeError2:
            if 'positional argument' in str(typeError2):
              try:
                callMeMaybe(newValue)
              except Exception as exception:
                raise exception from typeError2

  def notifyDel(self, instance: object, value: object) -> None:
    if self.__suppress_notification__ or self.isSilenced(instance):
      return
    for callMeMaybe in self._getDelSubscribers():
      try:
        callMeMaybe(instance, value)
      except TypeError as typeError:
        if 'positional argument' in str(typeError):
          try:
            callMeMaybe(instance)
          except Exception as exception:
            raise exception from typeError

  def _getGetSubscribers(self) -> list[callable]:
    return maybe(self.__get_subscribers__, [])

  def _getSetSubscribers(self) -> list[callable]:
    return maybe(self.__set_subscribers__, [])

  def _getDelSubscribers(self) -> list[callable]:
    return maybe(self.__del_subscribers__, [])

  def _addGetSubscriber(self, callMeMaybe: callable) -> None:
    """Subscribes the callable received to be notified when the field
    getter is called. The instance and the value are passed as arguments.
    If instance is None, the AttriBox is accessed through the owning class,
    which does not result in a notification.

    Similar to this method, the _addSetSubscriber and _addDelSubscriber
    methods are used to subscribe callables to be notified when the field
    is accessed. """
    getSubscribers = self._getGetSubscribers()
    self.__get_subscribers__ = [*getSubscribers, callMeMaybe]

  def _addSetSubscriber(self, callMeMaybe: callable) -> None:
    """Registers the callable for notification when field setter is
    called."""
    setSubscribers = self._getSetSubscribers()
    self.__set_subscribers__ = [*setSubscribers, callMeMaybe]

  def _addDelSubscriber(self, callMeMaybe: callable) -> None:
    """Registers the callable for notification when field deleter is
    called."""
    delSubscribers = self._getDelSubscribers()
    self.__del_subscribers__ = [*delSubscribers, callMeMaybe]

  def ONGET(self, callMeMaybe: callable) -> callable:
    """Decorator for subscribing to the getter."""
    self._addGetSubscriber(callMeMaybe)
    return callMeMaybe

  def ONSET(self, callMeMaybe: callable) -> callable:
    """Decorator for subscribing to the setter."""
    self._addSetSubscriber(callMeMaybe)
    return callMeMaybe

  def ONDEL(self, callMeMaybe: callable) -> callable:
    """Decorator for subscribing to the deleter."""
    self._addDelSubscriber(callMeMaybe)
    return callMeMaybe

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the value of the field."""
    if instance is None:
      return self
    try:
      value = self.__instance_get__(instance)
    except MissingValueException as missingValueException:
      raise AttributeError from missingValueException
    self.notifyGet(instance, value)
    return value

  def __set__(self, instance: object, value: object) -> None:
    """Set the value of the field."""
    try:
      oldValue = self.__instance_get__(instance)
    except MissingValueException:
      oldValue = None
    self.notifySet(instance, oldValue, value)
    self.__instance_set__(instance, value)

  def __delete__(self, instance: object) -> None:
    """Delete the value of the field."""
    try:
      oldValue = self.__instance_get__(instance)
    except MissingValueException as missingValueException:
      if missingValueException == (instance, self):
        oldValue = None
      else:
        raise missingValueException
    self.notifyDel(instance, oldValue)
    self.__instance_del__(instance)

  def __instance_reset__(self, instance: object) -> None:
    """Subclasses may implement this method to specify a way for the
    instance to have its value reset. """
    e = """The instance reset method is not implemented by the descriptor!"""
    raise TypeError(monoSpace(e))

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

  def reset(self, instance: object) -> None:
    """Reset the value of the field."""
    self.__instance_reset__(instance)
