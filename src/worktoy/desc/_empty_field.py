"""EmptyField provides a flexible implementation of the descriptor
protocol allowing owning classes to decorate methods as accessor methods. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any

from worktoy.desc import AbstractDescriptor
from worktoy.parse import maybe
from worktoy.text import typeMsg


class EmptyField(AbstractDescriptor):
  """EmptyField provides a flexible implementation of the descriptor
  protocol allowing owning classes to decorate methods as accessor
  methods. """
  __field_type__ = None
  __getter_name__ = None
  __setter_name__ = None
  __deleter_name__ = None
  __getter_function__ = None
  __setter_function__ = None
  __deleter_function__ = None

  def getFieldType(self) -> type:
    """Getter-function for the field type."""
    if self.__field_type__ is None:
      return object
    if isinstance(self.__field_type__, type):
      return self.__field_type__
    e = typeMsg('__field_type__', self.__field_type__, type)
    raise TypeError(e)

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the value of the field."""
    getter = None
    if instance is None:
      return self
    try:
      getter = self.__get_getter__()
    except Exception as exception:
      if isinstance(exception, (AttributeError, TypeError)):
        getter = getattr(owner, self.__getter_name__, None)
        if getter is None:
          raise exception
    value = getter(instance)
    self.notifyGet(instance, value)
    return value

  def __set__(self, instance: object, value: object) -> None:
    """Set the value of the field."""
    owner = self.getFieldOwner()
    fieldType = self.getFieldType()
    setter = None
    if not isinstance(value, fieldType):
      e = typeMsg('value', value, fieldType)
      raise TypeError(e)
    try:
      setter = self.__get_setter__()
    except Exception as exception:
      if isinstance(exception, (AttributeError, TypeError)):
        owner = self.getFieldOwner()
        setter = getattr(owner, self.__setter_name__, None)
        if setter is None:
          raise exception
    if not callable(setter):
      e = typeMsg('setter', setter, Callable)
      raise TypeError(e)
    oldValue = self.__get__(instance, owner)
    self.notifySet(instance, oldValue, value)
    setter(instance, value)

  def __delete__(self, instance: object) -> None:
    """Delete the value of the field."""
    owner = self.getFieldOwner()
    deleter = None
    try:
      deleter = self.__get_deleter__()
    except Exception as exception:
      if isinstance(exception, (AttributeError, TypeError)):
        deleter = getattr(owner, self.__deleter_name__, None)
        if deleter is None:
          raise exception
    if not callable(deleter):
      e = typeMsg('deleter', deleter, Callable)
      raise TypeError(e)
    oldValue = self.__get__(instance, owner)
    self.notifyDel(instance, oldValue)

  def __get_getter__(self, ) -> Callable:
    """Getter-function for the getter-function, getter-ception."""
    if self.__getter_function__ is None:
      e = """The field instance does not have a getter function!"""
      raise AttributeError(e)
    if callable(self.__getter_function__):
      return self.__getter_function__
    e = typeMsg('getter', self.__getter_function__, Callable)
    raise TypeError(e)

  def __get_setter__(self, ) -> Callable:
    """Getter-function for the setter-function of the field."""
    if self.__setter_function__ is None:
      e = """The field instance does not have a setter function!"""
      raise AttributeError(e)
    if callable(self.__setter_function__):
      return self.__setter_function__
    e = typeMsg('setter', self.__setter_function__, Callable)
    raise TypeError(e)

  def __get_deleter__(self, ) -> Callable:
    """Getter-function for the deleter-function of the field."""
    if self.__deleter_function__ is None:
      e = """The field instance does not have a deleter function!"""
      raise AttributeError(e)
    if callable(self.__deleter_function__):
      return self.__deleter_function__
    e = typeMsg('deleter', self.__deleter_function__, Callable)
    raise TypeError(e)

  def __set_getter__(self, callMeMaybe: Callable) -> Callable:
    """Set the getter function of the field."""
    if maybe(self.__getter_function__, self.__getter_name__) is not None:
      e = """The getter function has already been set!"""
      raise AttributeError(e)
    self.__getter_name__ = callMeMaybe.__name__
    self.__getter_function__ = callMeMaybe
    return callMeMaybe

  def __set_setter__(self, callMeMaybe: Callable) -> Callable:
    """Set the setter function of the field."""
    if maybe(self.__setter_name__, self.__setter_function__) is not None:
      e = """The setter function has already been set!"""
      raise AttributeError(e)
    self.__setter_name__ = callMeMaybe.__name__
    self.__setter_function__ = callMeMaybe
    return callMeMaybe

  def __set_deleter__(self, callMeMaybe: Callable) -> Callable:
    """Set the deleter function of the field."""
    if maybe(self.__deleter_name__, self.__deleter_function__) is not None:
      e = """The deleter function has already been set!"""
      raise AttributeError(e)
    self.__deleter_name__ = callMeMaybe.__name__
    self.__deleter_function__ = callMeMaybe
    return callMeMaybe

  def GET(self, callMeMaybe: Callable) -> Callable:
    """Decorator for setting the getter function of the field."""
    return self.__set_getter__(callMeMaybe)

  def SET(self, callMeMaybe: Callable) -> Callable:
    """Decorator for setting the setter function of the field."""
    return self.__set_setter__(callMeMaybe)

  def DELETE(self, callMeMaybe: Callable) -> Callable:
    """Decorator for setting the deleter function of the field."""
    return self.__set_deleter__(callMeMaybe)
