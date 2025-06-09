"""
_FieldProps holds the many properties used by the Field class. This
private class is intended solely to avoid excessive amounts of code in a
single file.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from functools import wraps

from ..parse import maybe
from ..static import AbstractObject
from ..text import typeMsg
from ..waitaminute import MissingVariable, TypeException, VariableNotNone

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

from types import FunctionType
from types import FunctionType as Func
from types import MethodType
from types import MethodType as Meth

if TYPE_CHECKING:
  from typing import Any, Self, Union, TypeAlias, Never, Callable


#
# def _flexSet(setterFunction: Callable) -> Callable:
#   """
#   Wraps setter functions calling them first with both new and old values,
#   then if raises 'TypeError', calls again with only the new value.
#   """
#
#   @wraps(setterFunction)
#   def wrapped(self: Any, value: Any, oldValue: Any = None) -> None:
#     """
#     Calls the setter function with both new and old values, then if
#     raises 'TypeError', calls again with only the new value.
#     """
#     try:
#       out = setterFunction(self, value, oldValue)
#     except TypeError as typeError:
#       if 'positional' in str(typeError):
#         try:
#           out = setterFunction(self, value)
#         except Exception as exception:
#           raise exception from typeError
#         else:
#           return out
#         finally:
#           pass
#       else:
#         raise typeError
#     else:
#       return out
#     finally:
#       pass
#
#   if isinstance(wrapped, Func):
#     return wrapped
#   raise TypeException('wrapped', wrapped, Func)
#
#
# def _flexDelete(deleterFunction: Callable) -> Callable:
#   """
#   Wraps deleter functions calling them first with the old value, then if
#   raises 'TypeError', calls again without the old value.
#   """
#
#   @wraps(deleterFunction)
#   def wrapped(self: Any, oldValue: Any = None) -> None:
#     """
#     Calls the deleter function with the old value, then if raises
#     'TypeError', calls again without the old value.
#     """
#     try:
#       out = deleterFunction(self, oldValue)
#     except TypeError as typeError:
#       if 'positional' in str(typeError):
#         try:
#           out = deleterFunction(self)
#         except Exception as exception:
#           raise exception from typeError
#         else:
#           return out
#         finally:
#           pass
#       else:
#         raise typeError
#     else:
#       return out
#     finally:
#       pass
#
#   if isinstance(wrapped, Func):
#     return wrapped
#   raise TypeException('wrapped', wrapped, Func)


class AbstractDescriptor(AbstractObject):
  """
  AbstractField provides an implementation of the descriptor protocol
  that allow the owning class to explicitly define the accessor methods.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables

  #  Private variables
  #  # Function keys allowing a subclass to override
  #  #  # Accessors
  __getter_key__ = None  # Get
  __setter_keys__ = None  # Set
  __deleter_keys__ = None  # Delete
  #  #  # Notifiers
  __pre_get_keys__ = None  # Before get
  __post_get_keys__ = None  # After get (using try/finally)
  __pre_set_keys__ = None  # Before set
  __post_set_keys__ = None  # After set
  __pre_delete_keys__ = None  # Before delete
  __post_delete_keys__ = None  # After delete
  #  # Function objects
  #  #  # Accessors
  __getter_func__ = None  # Get
  __setter_funcs__ = None  # Set
  __deleter_funcs__ = None  # Delete
  #  #  # Notifiers
  __pre_get_funcs__ = None  # Before get
  __post_get_funcs__ = None  # After get (using try/finally)
  __pre_set_funcs__ = None  # Before set
  __post_set_funcs__ = None  # After set
  __pre_delete_funcs__ = None  # Before delete
  __post_delete_funcs__ = None  # After delete

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Getter for the names of the accessors

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

  def _getSetKeys(self, **kwargs) -> tuple[str, ...]:
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
        raise RecursionError
      self.__setter_keys__ = (*self.__setter_keys__,)
      return self._getSetKeys(_recursion=True, )
    if isinstance(self.__setter_keys__, tuple):
      for key in self.__setter_keys__:
        if not isinstance(key, str):
          raise TypeError(typeMsg('setterKey', key, str))
      else:
        return self.__setter_keys__
    name, value = '__setter_keys__', self.__setter_keys__
    raise TypeException(name, value, tuple)

  def _getDeleteKeys(self, **kwargs) -> tuple[str, ...]:
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
        raise RecursionError
      self.__deleter_keys__ = (*self.__deleter_keys__,)
      return self._getDeleteKeys(_recursion=True, )
    if isinstance(self.__deleter_keys__, tuple):
      for key in self.__deleter_keys__:
        if not isinstance(key, str):
          raise TypeError(typeMsg('deleterKey', key, str))
      else:
        return self.__deleter_keys__
    name, value = '__deleter_keys__', self.__deleter_keys__
    raise TypeException(name, value, tuple)

  def _getPreGetKeys(self) -> tuple[str, ...]:
    """
    Getter-function for the names of the methods called before '__get__'
    returns. """
    return maybe(self.__pre_get_keys__, ())

  def _getPostGetKeys(self) -> tuple[str, ...]:
    """
    Getter-function for keys to functions called after '__get__' has
    returned, using try/finally.
    """
    return maybe(self.__post_get_keys__, ())

  def _getPreSetKeys(self) -> tuple[str, ...]:
    """
    Getter-function for keys to functions called before '__set__' returns
    """
    return maybe(self.__pre_set_keys__, ())

  def _getPostSetKeys(self) -> tuple[str, ...]:
    """
    Getter-function for keys to functions called after '__set__' has
    returned, using try/finally.
    """
    return maybe(self.__post_set_keys__, ())

  def _getPreDeleteKeys(self) -> tuple[str, ...]:
    """
    Getter-function for keys to functions called before '__delete__'
    returns.
    """
    return maybe(self.__pre_delete_keys__, ())

  def _getPostDeleteKeys(self) -> tuple[str, ...]:
    """
    Getter-function for keys to functions called after '__delete__' has
    returned, using try/finally.
    """
    return maybe(self.__post_delete_keys__, ())

  #  Getter for accessor functions directly

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
    if self.__getter_func__ is not None:
      if isinstance(self.__getter_func__, Func):
        return self.__getter_func__
      name, value = '__getter_func__', self.__getter_func__
      raise TypeException(name, value, Func)
    if kwargs.get('_recursion', False):
      raise RecursionError
    self.__getter_func__ = self._getGet()
    return self._getGetFuncObject(_recursion=True, )

  def _getSet(self, **kwargs) -> tuple[Func, ...]:
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

  def _getSetFuncObjects(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the setter function objects.
    """
    if self.__setter_funcs__ is not None:
      if isinstance(self.__setter_funcs__, list):
        if kwargs.get('_recursion', False):
          raise RecursionError
        self.__setter_funcs__ = (*self.__setter_funcs__,)
        return self._getSet(_recursion=True, )
      if isinstance(self.__setter_funcs__, tuple):
        for setterFunc in self.__setter_funcs__:
          if not isinstance(setterFunc, Func):
            name, value = '__setter_funcs__', setterFunc
            raise TypeException(name, value, Func)
        else:
          return self.__setter_funcs__
      if isinstance(self.__setter_funcs__, Func):
        return (self.__setter_funcs__,)
      name, value = '__setter_funcs__', self.__setter_funcs__
      raise TypeException(name, value, tuple)
    return ()

  def _getDelete(self, **kwargs) -> tuple[Func, ...]:
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

  def _getDeleteFuncObjects(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the deleter function objects.
    """
    if self.__deleter_funcs__ is not None:
      if isinstance(self.__deleter_funcs__, list):
        if kwargs.get('_recursion', False):
          raise RecursionError
        self.__deleter_funcs__ = (*self.__deleter_funcs__,)
        return self._getDelete(_recursion=True, )
      if isinstance(self.__deleter_funcs__, tuple):
        for deleterFunc in self.__deleter_funcs__:
          if not isinstance(deleterFunc, Func):
            name, value = '__deleter_funcs__', deleterFunc
            raise TypeException(name, value, Func)
        else:
          return self.__deleter_funcs__
      if isinstance(self.__deleter_funcs__, Func):
        return (self.__deleter_funcs__,)
      name, value = '__deleter_funcs__', self.__deleter_funcs__
      raise TypeException(name, value, tuple)
    return ()

  def _getPreGet(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the pre-get functions.

    These functions are called before the __get__ returns, but after the
    return value has been determined including any side effects. These
    functions are then called with:
    func(self.instance, value: Any) -> None
    """
    if self.owner is self.__field_owner__:
      # return function objects
      if self.__pre_get_funcs__ is not None:
        return self._getPreGetFuncObjects(**kwargs)
    preGetKeys = self._getPreGetKeys()
    preGetFuncs = []
    for preGetKey in preGetKeys:
      preGetFunc = getattr(self.owner, preGetKey, None)
      if preGetFunc is None:
        raise MissingVariable(preGetKey, Func)
      if isinstance(preGetFunc, Func):
        preGetFuncs.append(preGetFunc)
        continue
      name, value = preGetKey, preGetFunc
      raise TypeException(name, value, Func)
    return (*preGetFuncs,)

  def _getPreGetFuncObjects(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the pre-get function objects.
    """
    if self.__pre_get_funcs__ is not None:
      if isinstance(self.__pre_get_funcs__, list):
        if kwargs.get('_recursion', False):
          raise RecursionError
        self.__pre_get_funcs__ = (*self.__pre_get_funcs__,)
        return self._getPreGet(_recursion=True, )
      if isinstance(self.__pre_get_funcs__, tuple):
        for preGetFunc in self.__pre_get_funcs__:
          if not isinstance(preGetFunc, Func):
            name, value = '__pre_get_funcs__', preGetFunc
            raise TypeException(name, value, Func)
        else:
          return self.__pre_get_funcs__
      if isinstance(self.__pre_get_funcs__, Func):
        return (self.__pre_get_funcs__,)
      name, value = '__pre_get_funcs__', self.__pre_get_funcs__
      raise TypeException(name, value, tuple)
    return ()

  def _getPostGet(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the post-get functions.

    These functions are called after the __get__ has returned:
    try:
      return value
    finally:
      func(self.instance, value: Any) -> None
    """
    if self.owner is self.__field_owner__:  # return function objects
      if self.__post_get_funcs__ is not None:
        return self._getPostGetFuncObjects(**kwargs)
    postGetKeys = self._getPostGetKeys()
    postGetFuncs = []
    for postGetKey in postGetKeys:
      postGetFunc = getattr(self.owner, postGetKey, None)
      if postGetFunc is None:
        raise MissingVariable(postGetKey, Func)
      if isinstance(postGetFunc, Func):
        postGetFuncs.append(postGetFunc)
        continue
      name, value = postGetKey, postGetFunc
      raise TypeException(name, value, Func)
    return (*postGetFuncs,)

  def _getPostGetFuncObjects(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the post-get function objects.
    """
    if self.__post_get_funcs__ is not None:
      if isinstance(self.__post_get_funcs__, list):
        if kwargs.get('_recursion', False):
          raise RecursionError
        self.__post_get_funcs__ = (*self.__post_get_funcs__,)
        return self._getPostGet(_recursion=True, )
      if isinstance(self.__post_get_funcs__, tuple):
        for postGetFunc in self.__post_get_funcs__:
          if not isinstance(postGetFunc, Func):
            name, value = '__post_get_funcs__', postGetFunc
            raise TypeException(name, value, Func)
        else:
          return self.__post_get_funcs__
      if isinstance(self.__post_get_funcs__, Func):
        return (self.__post_get_funcs__,)
      name, value = '__post_get_funcs__', self.__post_get_funcs__
      raise TypeException(name, value, tuple)
    return ()

  def _getPreSet(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the pre-set hooks.

    These functions are called before __set__ returns with:
    oldValue = __get__(...)  # The current value or exception
    func(self.instance, value: Any, oldValue: Any) -> None
    """
    if self.owner is self.__field_owner__:
      # return function objects
      if self.__pre_set_funcs__ is not None:
        return self._getPreSetFuncObjects(**kwargs)
    preSetKeys = self._getPreSetKeys()
    preSetFuncs = []
    for preSetKey in preSetKeys:
      preSetFunc = getattr(self.owner, preSetKey, None)
      if preSetFunc is None:
        raise MissingVariable(preSetKey, Func)
      if isinstance(preSetFunc, Func):
        preSetFuncs.append(preSetFunc)
        continue
      name, value = preSetKey, preSetFunc
      raise TypeException(name, value, Func)
    return (*preSetFuncs,)

  def _getPreSetFuncObjects(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the pre-set function objects.
    """
    if self.__pre_set_funcs__ is not None:
      if isinstance(self.__pre_set_funcs__, list):
        if kwargs.get('_recursion', False):
          raise RecursionError
        self.__pre_set_funcs__ = (*self.__pre_set_funcs__,)
        return self._getPreSet(_recursion=True, )
      if isinstance(self.__pre_set_funcs__, tuple):
        for preSetFunc in self.__pre_set_funcs__:
          if not isinstance(preSetFunc, Func):
            name, value = '__pre_set_funcs__', preSetFunc
            raise TypeException(name, value, Func)
        else:
          return self.__pre_set_funcs__
      if isinstance(self.__pre_set_funcs__, Func):
        return (self.__pre_set_funcs__,)
      name, value = '__pre_set_funcs__', self.__pre_set_funcs__
      raise TypeException(name, value, tuple)
    return ()

  def _getPostSet(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the post-set hooks.

    These functions are called after __set__ has returned:
    oldValue = __get__(...)  # The current value or exception
    __set__(...)  # The new value is set
    newValue = __get__(...)  # The new value retrieved through __get__
    __set__(...)
    func(self.instance, newValue: Any, oldValue: Any) -> None
    """
    if self.owner is self.__field_owner__:  # return function objects
      if self.__post_set_funcs__ is not None:
        return self._getPostSetFuncObjects(**kwargs)
    postSetKeys = self._getPostSetKeys()
    postSetFuncs = []
    for postSetKey in postSetKeys:
      postSetFunc = getattr(self.owner, postSetKey, None)
      if postSetFunc is None:
        raise MissingVariable(postSetKey, Func)
      if isinstance(postSetFunc, Func):
        postSetFuncs.append(postSetFunc)
        continue
      name, value = postSetKey, postSetFunc
      raise TypeException(name, value, Func)
    return (*postSetFuncs,)

  def _getPostSetFuncObjects(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the post-set function objects.
    """
    if self.__post_set_funcs__ is not None:
      if isinstance(self.__post_set_funcs__, list):
        if kwargs.get('_recursion', False):
          raise RecursionError
        self.__post_set_funcs__ = (*self.__post_set_funcs__,)
        return self._getPostSet(_recursion=True, )
      if isinstance(self.__post_set_funcs__, tuple):
        for postSetFunc in self.__post_set_funcs__:
          if not isinstance(postSetFunc, Func):
            name, value = '__post_set_funcs__', postSetFunc
            raise TypeException(name, value, Func)
        else:
          return self.__post_set_funcs__
      if isinstance(self.__post_set_funcs__, Func):
        return (self.__post_set_funcs__,)
      name, value = '__post_set_funcs__', self.__post_set_funcs__
      raise TypeException(name, value, tuple)
    return ()

  def _getPreDelete(self, **kwargs, ) -> tuple[Func, ...]:
    """
    Getter-function for the pre-delete hooks.

    These functions are called before __delete__ returns with:
    oldValue = __get__(...)  # The current value

    Please note that if oldValue is the 'DELETED' sentinel value or the
    __get__ raises AttributeError, then the error is expected to
    propagate. The same is not True for the set methods.

    func(self.instance, oldValue) -> None
    """
    if self.owner is self.__field_owner__:  # return function objects
      if self.__pre_delete_funcs__ is not None:
        return self._getPreDeleteFuncObjects(**kwargs)
    preDeleteKeys = self._getPreDeleteKeys()
    preDeleteFuncs = []
    for preDeleteKey in preDeleteKeys:
      preDeleteFunc = getattr(self.owner, preDeleteKey, None)
      if preDeleteFunc is None:
        raise MissingVariable(preDeleteKey, Func)
      if isinstance(preDeleteFunc, Func):
        preDeleteFuncs.append(preDeleteFunc)
        continue
      name, value = preDeleteKey, preDeleteFunc
      raise TypeException(name, value, Func)
    return (*preDeleteFuncs,)

  def _getPreDeleteFuncObjects(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the pre-delete function objects.
    """
    if self.__pre_delete_funcs__ is not None:
      if isinstance(self.__pre_delete_funcs__, list):
        if kwargs.get('_recursion', False):
          raise RecursionError
        self.__pre_delete_funcs__ = (*self.__pre_delete_funcs__,)
        return self._getPreDelete(_recursion=True, )
      if isinstance(self.__pre_delete_funcs__, tuple):
        for preDeleteFunc in self.__pre_delete_funcs__:
          if not isinstance(preDeleteFunc, Func):
            name, value = '__pre_delete_funcs__', preDeleteFunc
            raise TypeException(name, value, Func)
        else:
          return self.__pre_delete_funcs__
      if isinstance(self.__pre_delete_funcs__, Func):
        return (self.__pre_delete_funcs__,)
      name, value = '__pre_delete_funcs__', self.__pre_delete_funcs__
      raise TypeException(name, value, tuple)
    return ()

  def _getPostDelete(self, **kwargs, ) -> tuple[Func, ...]:
    """
    Getter-function for the post-delete hooks.

    These functions are called after __delete__ has returned:
    oldValue = __get__(...)  # The current value
    __delete__(...)  # The value is deleted
    func(self.instance, oldValue) -> None

    It is possible for a post delete hook to restore the value at this
    stage, although doing so will break the expectation that the following
    should raise AttributeError:

    foo.bar = 69
    del foo.bar
    foo.bar  # Raises AttributeError
    """
    if self.owner is self.__field_owner__:  # return function objects
      if self.__post_delete_funcs__ is not None:
        return self._getPostDeleteFuncObjects(**kwargs)
    postDeleteKeys = self._getPostDeleteKeys()
    postDeleteFuncs = []
    for postDeleteKey in postDeleteKeys:
      postDeleteFunc = getattr(self.owner, postDeleteKey, None)
      if postDeleteFunc is None:
        raise MissingVariable(postDeleteKey, Func)
      if isinstance(postDeleteFunc, Func):
        postDeleteFuncs.append(postDeleteFunc)
        continue
      name, value = postDeleteKey, postDeleteFunc
      raise TypeException(name, value, Func)
    return (*postDeleteFuncs,)

  def _getPostDeleteFuncObjects(self, **kwargs) -> tuple[Func, ...]:
    """
    Getter-function for the post-delete function objects.
    """
    if self.__post_delete_funcs__ is not None:
      if isinstance(self.__post_delete_funcs__, list):
        if kwargs.get('_recursion', False):
          raise RecursionError
        self.__post_delete_funcs__ = (*self.__post_delete_funcs__,)
        return self._getPostDelete(_recursion=True, )
      if isinstance(self.__post_delete_funcs__, tuple):
        for postDeleteFunc in self.__post_delete_funcs__:
          if not isinstance(postDeleteFunc, Func):
            name, value = '__post_delete_funcs__', postDeleteFunc
            raise TypeException(name, value, Func)
        else:
          return self.__post_delete_funcs__
      if isinstance(self.__post_delete_funcs__, Func):
        return (self.__post_delete_funcs__,)
      name, value = '__post_delete_funcs__', self.__post_delete_funcs__
      raise TypeException(name, value, tuple)
    return ()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setGetter(self, callMeMaybe: Func) -> Func:
    """
    Setter-function for the getter function.
    """
    if not isinstance(callMeMaybe, Func):
      name, value = '_setGetter', callMeMaybe
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
      name, value = '_addSetter', callMeMaybe
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
      name, value = '_addDeleter', callMeMaybe
      raise TypeException(name, value, Func)
    existingFuncs = self._getDelete()
    existingKeys = self._getDeleteKeys()
    self.__deleter_funcs__ = (*existingFuncs, callMeMaybe)
    self.__deleter_keys__ = (*existingKeys, callMeMaybe.__name__,)
    return callMeMaybe

  def _addPreGet(self, callMeMaybe: Func) -> Func:
    """
    Add a pre-get function to the field.

    This function is used to add a pre-get function to the field. The
    function should be an instance method of the owner class.
    """
    if not isinstance(callMeMaybe, Func):
      name, value = '_addPreGet', callMeMaybe
      raise TypeException(name, value, Func)
    existingKeys = self._getPreGetKeys()
    existingFuncs = self._getPreGetFuncs()
    self.__pre_get_keys__ = (*existingKeys, callMeMaybe.__name__,)
    self.__pre_get_funcs__ = (*existingFuncs, callMeMaybe)
    return callMeMaybe

  def _addPostGet(self, callMeMaybe: Func) -> Func:
    """
    Add a post-get function to the field.

    This function is used to add a post-get function to the field. The
    function should be an instance method of the owner class.
    """
    if not isinstance(callMeMaybe, Func):
      name, value = '_addPostGet', callMeMaybe
      raise TypeException(name, value, Func)
    existingKeys = self._getPostGetKeys()
    existingFuncs = self._getPostGet()
    self.__post_get_keys__ = (*existingKeys, callMeMaybe.__name__,)
    self.__post_get_funcs__ = (*existingFuncs, callMeMaybe)
    return callMeMaybe

  def _addPreSet(self, callMeMaybe: Func) -> Func:
    """
    Add a pre-set function to the field.

    This function is used to add a pre-set function to the field. The
    function should be an instance method of the owner class.
    """
    if not isinstance(callMeMaybe, Func):
      name, value = '_addPreSet', callMeMaybe
      raise TypeException(name, value, Func)
    existingFuncs = self._getPreSet()
    existingKeys = self._getPreSetKeys()
    self.__pre_set_keys__ = (*existingKeys, callMeMaybe.__name__,)
    self.__pre_set_funcs__ = (*existingFuncs, callMeMaybe)
    return callMeMaybe

  def _addPostSet(self, callMeMaybe: Func) -> Func:
    """
    Add a post-set function to the field.

    This function is used to add a post-set function to the field. The
    function should be an instance method of the owner class.
    """
    if not isinstance(callMeMaybe, Func):
      name, value = '_addPostSet', callMeMaybe
      raise TypeException(name, value, Func)
    existingFuncs = self._getPostSet()
    existingKeys = self._getPostSetKeys()
    self.__post_set_keys__ = (*existingKeys, callMeMaybe.__name__,)
    self.__post_set_funcs__ = (*existingFuncs, callMeMaybe)
    return callMeMaybe

  def _addPreDelete(self, callMeMaybe: Func) -> Func:
    """
    Add a pre-delete function to the field.

    This function is used to add a pre-delete function to the field. The
    function should be an instance method of the owner class.
    """
    if not isinstance(callMeMaybe, Func):
      name, value = '_addPreDelete', callMeMaybe
      raise TypeException(name, value, Func)
    existingKeys = self._getPreDeleteKeys()
    existingFuncs = self._getPreDelete()
    self.__pre_delete_keys = (*existingKeys, callMeMaybe.__name__,)
    self.__pre_delete_funcs__ = (*existingFuncs, callMeMaybe)
    return callMeMaybe

  def _addPostDelete(self, callMeMaybe: Func) -> Func:
    """
    Add a post-delete function to the field.

    This function is used to add a post-delete function to the field. The
    function should be an instance method of the owner class.
    """
    if not isinstance(callMeMaybe, Func):
      name, value = '_addPostDelete', callMeMaybe
      raise TypeException(name, value, Func)
    existingKeys = self._getPostDeleteKeys()
    existingFuncs = self._getPostDelete()
    self.__post_delete_keys__ = (*existingKeys, callMeMaybe.__name__,)
    self.__post_delete_funcs__ = (*existingFuncs, callMeMaybe)
    return callMeMaybe
