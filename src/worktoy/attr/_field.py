"""AbstractField provides an implementation of the descriptor protocol
that allow the owning class to explicitly define the accessor methods.  """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func
from types import MethodType as Meth

from ..static import AbstractObject
from ..text import typeMsg
from ..waitaminute import MissingVariable, TypeException

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias

  Keys: TypeAlias = tuple[str, ...]
  Funcs: TypeAlias = tuple[Func, ...]


class Field(AbstractObject):
  """AbstractField provides an implementation of the descriptor protocol
  that allow the owning class to explicitly define the accessor methods.  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables

  #  Private variables
  #  #  Keys
  __getter_key__ = None  # Get
  __setter_keys__ = None  # Set
  __deleter_keys__ = None  # Delete
  #  #  Function Objects
  __getter_func__ = None  # Get
  __setter_funcs__ = None  # Set
  __deleter_funcs__ = None  # Delete

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  ________________________________________________________________________
  #  Getter for accessor keys
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def _getGetKey(self, ) -> str:
    """
    Getter-function for the name of the single and required method called
    to retrieve the value to be returned by '__get__'. The recommended
    design pattern is to decorate a method in the class body with 'GET'.
    The decorated method should simply be an instance method.
    """
    if self.__getter_key__ is None:
      raise MissingVariable('__getter_key__', str)
    if isinstance(self.__getter_key__, str):
      return self.__getter_key__
    name, value = '__getter_key__', self.__getter_key__
    raise TypeException(name, value, str)

  def _getSetKeys(self, **kwargs) -> Keys:
    """
    Getter-function for the names of the methods called to set the value
    of the field. The recommended design pattern is to decorate methods
    in the class body with 'SET'. The decorated methods should simply be
    instance methods.
    """
    if self.__setter_keys__ is None:
      return ()
    if isinstance(self.__setter_keys__, list):
      if kwargs.get('_recursion', False):
        raise RecursionError  # pragma: no cover
      self.__setter_keys__ = (*self.__setter_keys__,)
      return self._getSetKeys(_recursion=True, )
    if isinstance(self.__setter_keys__, tuple):
      for key in self.__setter_keys__:
        if not isinstance(key, str):
          raise TypeException('key', key, str)
      else:
        return self.__setter_keys__
    name, value = '__setter_keys__', self.__setter_keys__
    raise TypeException(name, value, tuple)

  def _getDeleteKeys(self, **kwargs) -> Keys:
    """
    Getter-function for the names of the methods called to delete the
    field. The recommended design pattern is to decorate methods in the
    class body with 'DELETE'. The decorated methods should simply be
    instance methods.
    """
    if self.__deleter_keys__ is None:
      return ()
    if isinstance(self.__deleter_keys__, list):
      if kwargs.get('_recursion', False):
        raise RecursionError  # pragma: no cover
      self.__deleter_keys__ = (*self.__deleter_keys__,)
      return self._getDeleteKeys(_recursion=True, )
    if isinstance(self.__deleter_keys__, tuple):
      for key in self.__deleter_keys__:
        if not isinstance(key, str):
          raise TypeException('key', key, str)
      else:
        return self.__deleter_keys__
    name, value = '__deleter_keys__', self.__deleter_keys__
    raise TypeException(name, value, tuple)

  #  ________________________________________________________________________
  #  Getter for accessor functions directly
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
  def _getGet(self, **kwargs) -> Func:
    """
    Getter-function for the getter function.

    This function receives the current instance as the single argument:
    func(self.instance) -> Any

    """
    if self.owner is self.__field_owner__:  # return function object
      if self.__getter_func__ is not None:
        return self._getGetFuncObject(**kwargs)
    getterKey = self._getGetKey()
    getterFunc = getattr(self.owner, getterKey)
    if getterFunc is None:
      raise MissingVariable(getterKey, Func)
    if isinstance(getterFunc, Func):
      return getterFunc
    name, value = getterKey, getterFunc
    raise TypeException(name, value, Func)

  def _getGetFuncObject(self, **kwargs) -> Func:
    """
    Getter-function for the getter function object.
    """
    if isinstance(self.__getter_func__, Func):
      return self.__getter_func__
    name, value = '__getter_func__', self.__getter_func__
    raise TypeException(name, value, Func)

  def _getSet(self, **kwargs) -> Funcs:
    """
    Getter-function for the setter functions.

    These functions receive:
    func(self.instance, value: Any) -> None
    """
    if self.owner is self.__field_owner__:  # return function objects
      if self.__setter_funcs__ is not None:
        return self._getSetFuncObjects(**kwargs)
    setterKeys = self._getSetKeys(**kwargs)
    setterFuncs = []
    for setterKey in setterKeys:
      setterFunc = getattr(self.owner, setterKey, None)
      if setterFunc is None:
        raise MissingVariable(setterKey, Func)
      if isinstance(setterFunc, Func):
        setterFuncs.append(setterFunc)
        continue
      name, value = setterKey, setterFunc
      raise TypeException(name, value, Func)
    return (*setterFuncs,)

  def _getSetFuncObjects(self, **kwargs) -> Funcs:  # tuple[Func, ...]
    """
    Getter-function for the setter function objects.
    """
    try:
      for setterFunc in self.__setter_funcs__:
        if not isinstance(setterFunc, Func):
          name, value = 'setterFunc', setterFunc
          raise TypeException(name, value, Func)
    except TypeError as typeError:
      if 'iterable' in str(typeError):
        name, value = '__setter_funcs__', self.__setter_funcs__
        raise TypeException(name, value, tuple)
      raise typeError
    else:
      return self.__setter_funcs__

  def _getDelete(self, **kwargs) -> Funcs:
    """
    Getter-function for the deleter functions.

    These functions receive:
    func(self.instance) -> None
    """
    if self.owner is self.__field_owner__:  # return function objects
      if self.__deleter_funcs__ is not None:
        return self._getDeleteFuncObjects(**kwargs)
    deleterKeys = self._getDeleteKeys(**kwargs)
    deleterFuncs = []
    for deleterKey in deleterKeys:
      deleterFunc = getattr(self.owner, deleterKey, None)
      if deleterFunc is None:
        raise MissingVariable(deleterKey, Func)
      if isinstance(deleterFunc, Func):
        deleterFuncs.append(deleterFunc)
        continue
      name, value = deleterKey, deleterFunc
      raise TypeException(name, value, Func)
    return (*deleterFuncs,)

  def _getDeleteFuncObjects(self, **kwargs) -> Funcs:
    """
    Getter-function for the deleter function objects.
    """
    try:
      for deleterFunc in self.__deleter_funcs__:
        if not isinstance(deleterFunc, Func):
          name, value = 'deleterFunc', deleterFunc
          raise TypeException(name, value, Func)
    except TypeError as typeError:
      if 'iterable' in str(typeError).lower():
        name, value = '__deleter_funcs__', self.__deleter_funcs__
        raise TypeException(name, value, tuple)
      raise typeError
    else:
      return self.__deleter_funcs__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setGetter(self, callMeMaybe: Func) -> Func:
    """
    Setter-function for the getter function.
    """
    if not isinstance(callMeMaybe, Func):
      name, value = 'getterFunc', callMeMaybe
      raise TypeException(name, value, Func)
    self.__getter_func__ = callMeMaybe
    self.__getter_key__ = callMeMaybe.__name__
    return callMeMaybe

  def _addSetter(self, callMeMaybe: Func) -> Func:
    """
    Add a setter function to the field.

    This function is used to add a setter function to the field. The
    function should be an instance method of the owner class.
    """
    if not isinstance(callMeMaybe, Func):
      name, value = 'setterFunc', callMeMaybe
      raise TypeException(name, value, Func)
    existingFuncs = self._getSet()
    existingKeys = self._getSetKeys()
    self.__setter_funcs__ = (*existingFuncs, callMeMaybe)
    self.__setter_keys__ = (*existingKeys, callMeMaybe.__name__,)
    return callMeMaybe

  def _addDeleter(self, callMeMaybe: Func) -> Func:
    """
    Add a deleter function to the field.

    This function is used to add a deleter function to the field. The
    function should be an instance method of the owner class.
    """
    if not isinstance(callMeMaybe, Func):
      name, value = 'deleterFunc', callMeMaybe
      raise TypeException(name, value, Func)
    existingFuncs = self._getDelete()
    existingKeys = self._getDeleteKeys()
    self.__deleter_funcs__ = (*existingFuncs, callMeMaybe)
    self.__deleter_keys__ = (*existingKeys, callMeMaybe.__name__,)
    return callMeMaybe

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Decorator shorthands
  GET = _setGetter
  SET = _addSetter
  DELETE = _addDeleter

  #  Implementing instance accessors

  def __instance_get__(self, **kwargs) -> Any:
    """
    Instance getter-function retrieves the value of the field by calling
    the getter function.
    """
    getter = self._getGet()
    return getter(self.instance, **kwargs)

  def __instance_set__(self, value: Any, **kwargs) -> None:
    """
    Instance setter-function sets the value of the field by calling the
    setter functions.
    """
    setters = self._getSet()
    if not setters:
      return AbstractObject.__instance_set__(self, value, **kwargs)
    for setter in setters:
      setter(self.instance, value, **kwargs)

  def __instance_delete__(self, **kwargs) -> None:
    """
    Instance deleter-function deletes the field by calling the deleter
    functions.
    """
    deleters = self._getDelete()
    if not deleters:
      return AbstractObject.__instance_delete__(self, **kwargs)
    for deleter in deleters:
      deleter(self.instance, **kwargs)
