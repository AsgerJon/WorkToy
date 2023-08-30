"""WorkToy - Base - FunctionDecorator
General function decorator."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Function, RESULT


class FunctionDecorator:
  """General function decorator."""

  def __init__(self, *__, **_) -> None:
    self.__inner_function__ = None

  def preFunction(self, *args, **kwargs) -> RESULT:
    """Passes arguments on to the inner function. """
    return (args, kwargs)

  def postFunction(self, argument: object) -> object:
    """Receives the return value from the inner function. """
    return argument

  def implicitFunction(self, inner: Function, *args, **kwargs) -> object:
    """This function provides implicit decoration of the function:
    Let W and F be this function and the inner function respectively. Then
    F(args, kwargs) is replaced with: W(F, args, kwargs).
    """
    return inner(*args, **kwargs)

  def __call__(self, *args, **kwargs) -> object:
    """Sets inner function if not set, otherwise creates an instance of
    Exception where the set inner function will be the __str__. """
    if self.__inner_function__ is None:
      self.__set_inner_function__(*args, **kwargs)
      return self
    innerFunction = self.__inner_function__

    args, kwargs = self.preFunction(*args, **kwargs)
    argument = self.implicitFunction(innerFunction, *args, **kwargs)
    return self.postFunction(argument)

  def __set_inner_function__(self, *args, **_) -> None:
    """Setter-function for inner function"""

    if self.__inner_function__ is not None:
      raise TypeError('Inner function already set!')

    func = None
    for arg in args:
      if isinstance(arg, Function) and func is None:
        func = arg
      if func is None:
        raise TypeError(
          'Expected %s, but received %s' % (Function, type(func)))

    def wrapper(*args2, **kwargs2) -> object:
      """Wrapper methods on the given function"""
      return func(*args2, **kwargs2)

    self.__inner_function__ = wrapper
    notes = getattr(func, '__annotations__', None)
    doc = getattr(func, '__doc__', None)
    if notes is not None:
      setattr(self.__inner_function__, '__annotations__', notes)
    if doc is not None:
      setattr(self.__inner_function__, '__doc__', doc)

  def __invoke_inner_function__(self, *args, **kwargs) -> object:
    """Invokes the inner function in between the pre- and post-functions."""
    if self.__inner_function__ is None:
      raise TypeError('Inner function not set!')
    return self.__inner_function__(*args, **kwargs)

  def __get_inner_function__(self, ) -> Function:
    """Getter-function for the inner function"""
    if self.__inner_function__ is None:
      raise TypeError('Inner function not set!')
    return self.__inner_function__
 