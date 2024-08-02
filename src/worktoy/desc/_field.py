"""EmptyField provides a flexible implementation of the descriptor
protocol allowing owning classes to decorate methods as accessor methods. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from worktoy.desc import AbstractDescriptor, MissingValueException
from worktoy.text import typeMsg


class Field(AbstractDescriptor):
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

  def __instance_get__(self, instance: object) -> object:
    """Get the instance object."""
    try:
      return self.__get_getter__()(instance)
    except AttributeError:
      raise MissingValueException(instance, self)

  def __instance_set__(self, instance: object, value: object) -> None:
    """Set the instance object."""
    self.__get_setter__()(instance, value)

  def __instance_del__(self, instance: object) -> None:
    """Delete the instance object."""
    self.__get_deleter__()(instance)

  def __get_getter__(self, ) -> Callable:
    """Getter-function for the getter-function, getter-ception."""
    if self.__getter_function__ is None:
      raise AttributeError
    if callable(self.__getter_function__):
      return self.__getter_function__
    e = typeMsg('getter', self.__getter_function__, Callable)
    raise TypeError(e)

  def __get_setter__(self, ) -> Callable:
    """Getter-function for the setter-function of the field."""
    if callable(self.__setter_function__):
      return self.__setter_function__
    e = typeMsg('setter', self.__setter_function__, Callable)
    raise TypeError(e)

  def __get_deleter__(self, ) -> Callable:
    """Getter-function for the deleter-function of the field."""
    if callable(self.__deleter_function__):
      return self.__deleter_function__
    e = typeMsg('deleter', self.__deleter_function__, Callable)
    raise TypeError(e)

  def __set_getter__(self, callMeMaybe: Callable) -> Callable:
    """Set the getter function of the field."""
    if self.__getter_function__ is not None:
      e = """The getter function has already been set!"""
      raise AttributeError(e)
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
    self.__getter_function__ = callMeMaybe
    return callMeMaybe

  def __set_setter__(self, callMeMaybe: Callable) -> Callable:
    """Set the setter function of the field."""
    if self.__setter_function__ is not None:
      e = """The setter function has already been set!"""
      raise AttributeError(e)
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
    self.__setter_function__ = callMeMaybe
    return callMeMaybe

  def __set_deleter__(self, callMeMaybe: Callable) -> Callable:
    """Set the deleter function of the field."""
    if self.__deleter_function__ is not None:
      e = """The deleter function has already been set!"""
      raise AttributeError(e)
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
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
