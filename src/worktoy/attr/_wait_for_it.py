"""WaitForIt provides a deferred descriptor.
Usage:
class Foo:
  bar = WaitForIt(func, *args, **kwargs)
Then:
foo = Foo()
foo.bar = Foo.bar.__get__(foo, Foo) = func(*args, **kwargs)

This allows lazy evaluation of the given function with the given
arguments. By passing 'THIS' as an argument, 'THIS' is replaced with the
instance passed to __get__.

By passing only a 'str' object as the first argument, __get__ returns:
getattr(instance, arg: str).

The first argument must be a callable, a str object pointing to a key or
THIS, which is redundant.

"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import re

from worktoy.attr import CurrentDescriptor
from worktoy.parse import maybe
from worktoy.static import THIS, OWNER, ATTR
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute import SubclassException
from worktoy.waitaminute import ReadOnlyError, ProtectedError

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias, Never
else:
  try:
    from types import FunctionType as Callable
  except ImportError:
    def func() -> None:
      pass


    Callable = type(func)


class WaitForIt(CurrentDescriptor):
  """Creates a deferred function that is called when the __get__ is first
  called. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Python API

  #  Private variables
  __call_me_maybe__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  def _getCallMeMaybe(self, ) -> Callable:
    """Get the call me maybe function."""
    if self.__call_me_maybe__ is None:
      raise MissingVariable('__call_me_maybe__', Callable)
    if callable(self.__call_me_maybe__):
      return self.__call_me_maybe__
    raise TypeException(
        '__call_me_maybe__',
        self.__call_me_maybe__,
        Callable
    )

  #  Setters
  def _setCurrentInstance(self, instance: Any) -> None:
    """Set the current instance."""
    if instance is not self.__current_instance__:
      self.__current_instance__ = instance

  def _setCurrentOwner(self, owner: type) -> None:
    """Set the current owner."""
    fieldOwner = self._getFieldOwner()
    if not issubclass(owner, fieldOwner):
      raise SubclassException(owner, fieldOwner)
    self.__current_owner__ = owner

  #  Others
  def _generatePrivateName(self, ) -> str:
    """Generates a private name for the field based on the field name. """
    fieldName = self._getFieldName()
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return '__%s__' % pattern.sub('_', fieldName).lower()

  #  Python API
  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """Get the value of the descriptor."""
    if instance is None:
      return self
    pvtName = self._generatePrivateName()
    if hasattr(instance, pvtName):
      return getattr(instance, pvtName)
    if kwargs.get('_recursion', False):
      raise RecursionError
    self._setCurrentInstance(instance)
    self._setCurrentOwner(owner)
    callMeMaybe = self._getCallMeMaybe()
    posArgs = self._getPosArgs()
    keyArgs = self._getKeyArgs()
    val = callMeMaybe(*posArgs, **keyArgs)
    setattr(instance, pvtName, val)
    return self.__get__(instance, owner, _recursion=True)

  def __set__(self, instance: Any, value: Any) -> Never:
    """The setter is disabled"""
    raise ReadOnlyError(instance, self, value)

  def __delete__(self, instance: Any) -> Never:
    """The deleter is disabled"""
    owner = self._getCurrentOwner()
    val = self.__get__(instance, owner)
    raise ProtectedError(self, instance, val)

  #  Constructors
  def __init__(self, *args: Any, **kwargs: Any) -> None:
    """Constructor for the WaitForIt class."""
    if not args:
      raise MissingVariable('__call_me_maybe__', Callable)
    if args[0] in [THIS, OWNER, ATTR]:
      self.__call_me_maybe__ = getattr
      self.__pos_args__ = (*args,)
    elif isinstance(args[0], str):
      self.__call_me_maybe__ = getattr
      self.__pos_args__ = (THIS, *args,)
    elif callable(args[0]):
      self.__call_me_maybe__ = args[0]
      self.__pos_args__ = (*args[1:],)
    else:
      raise TypeException('__call_me_maybe__', args[0], Callable)
    if kwargs:
      self.__key_args__ = kwargs
