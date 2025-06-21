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

from ..waitaminute import MissingVariable, TypeException, VariableNotNone
from . import Field

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class WaitForIt(Field):
  """Creates a deferred function that is called when the __get__ is first
  called. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __creator_function__ = None  # The function that creates the descriptor

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getCreatorFunction(self) -> Func:
    """Get the creator function."""
    if self.__creator_function__ is None:
      raise MissingVariable('__creator_function__', Func)
    if not isinstance(self.__creator_function__, Func):
      name, value = '__creator_function__', self.__creator_function__
      raise TypeException(name, value, Func)
    #  _getCreatorFunction should never be invoked, except when both owner
    #  and instance have objects other than None. Thus, the creator may be
    #  retrieved from the instance ensuring it is a bound method.
    #  Therefore, the 'self/cls' first argument will not swallow one of
    #  the expected values. If the function is not present, it means it is
    #  not a method in the class. In this case, the function is called
    #  directly.
    key = self.__creator_function__.__name__
    return getattr(self.instance, key, self.__creator_function__)

  def _hasCreatorFunction(self, ) -> bool:
    """Check if the creator function is set."""
    if self.__creator_function__ is None:
      return False
    if isinstance(self.__creator_function__, Func):
      return True
    name, value = '__creator_function__', self.__creator_function__
    raise TypeException(name, value, Func)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setCreatorFunction(self, creator: Func) -> None:
    """Set the creator function."""
    if self.__creator_function__ is not None:
      name, value = '__creator_function__', self.__creator_function__
      raise VariableNotNone(name, value)
    if not isinstance(creator, Func):
      name, value = '__creator_function__', creator
      raise TypeException(name, value, Func)
    self.__creator_function__ = creator

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    posArgs = []
    tempArgs = [*args, ]
    while tempArgs:
      arg = tempArgs.pop(0)
      if isinstance(arg, Func):
        self._setCreatorFunction(arg)
        posArgs.extend(tempArgs)
        Field.__init__(self, *posArgs, **kwargs)
        break
      posArgs.append(arg)
    else:
      Field.__init__(self, *args, **kwargs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, **kwargs) -> Any:
    """
    Get the value of the descriptor, which is the result of calling the
    creator function with the given arguments.
    """
    creator = self._getCreatorFunction()
    pvtName = self.getPrivateName()
    if not hasattr(self.instance, pvtName, ):
      if kwargs.get('_recursion', False):
        raise RecursionError
      args = self._getPositionalArgs()
      kwargs = self._getKeywordArgs()
      value = creator(*args, **kwargs)
      setattr(self.instance, pvtName, value)
      return self.__instance_get__(_recursion=True, )
    return getattr(self.instance, pvtName, )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __call__(self, func: Func) -> Any:
    """Call the descriptor with the given arguments."""
    self._setCreatorFunction(func)
    return func
