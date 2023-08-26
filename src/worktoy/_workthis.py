"""WorkToy | WorkMethod
Applies __set_name__ to decorated function."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from icecream import ic

from worktoy.core import DefaultClass, Function

ic.configureOutput(includeContext=True)


class _WorkThisProperties(DefaultClass):
  """WorkToy | WorkMethod (Properties file)
  Applies __set_name__ to decorated function."""

  def __init__(self, func: Function) -> None:
    DefaultClass.__init__(self, func)
    self._targetClass = None
    self._name = None
    self._obj = None
    self._innerFunction = func

  def getTargetClass(self) -> type:
    """Getter-function for the target class"""
    if self._targetClass is not None:
      return self._targetClass

  def setTargetClass(self, target: type) -> None:
    """Setter-function for the target class"""
    self._targetClass = target

  def getName(self) -> str:
    """Getter-function for name"""
    return self._name

  def setName(self, name: str) -> None:
    """Setter-function for the name"""
    self._name = name

  def setInnerFunction(self, innerFunction: Function) -> None:
    """Setter function for the inner function"""
    if self._innerFunction is None or True:
      self._innerFunction = innerFunction
      self.__annotations__ = self._innerFunction.__annotations__

  def getInnerFunction(self, *__, **_) -> Function:
    """Invokes the inner function"""
    if self._innerFunction is None:
      raise TypeError
    return self._innerFunction

  def getObject(self) -> object:
    """Getter-function for the object most recently set"""
    return self._obj

  def setObject(self, obj: object) -> None:
    """Setter-function for the object"""
    self._obj = obj


class WorkThis(_WorkThisProperties):
  """WorkToy | WorkMethod
  Applies __set_name__ to decorated function."""

  def __init__(self, func: Function) -> None:
    _WorkThisProperties.__init__(self, func)
    # self._parseFunction = self.parseFactory(Function, 'function', 'method')
    self.__annotations__ = {}

  def getAnnotations(self) -> dict:
    """Getter-function for the annotations of the inner function"""
    return self.getInnerFunction().__annotations__

  def __call__(self, *args, **kwargs) -> Function:
    """Sets inner function or invokes inner function"""
    ic(args, kwargs)

  def __set_name__(self, cls: type, name: str) -> None:
    """Sets name and target class"""
    self._name = name
    self._targetClass = cls
    self.getInnerFunction = lambda *_: getattr(cls, name, None)

  def getWrappedFunction(self, obj) -> Function:
    """Getter-function for wrapped function"""
    innerFunc = self._innerFunction

    def wrapped(*args, **kwargs):
      """Function wrapping the inner function"""
      newArgs = [arg for arg in args if arg not in [obj, innerFunc]]
      ic(obj, innerFunc, newArgs, kwargs)
      return innerFunc(obj, innerFunc, *newArgs, **kwargs)

    return wrapped

  def __get__(self, obj: object, cls: type) -> Function:
    """Getter for the wrapped inner function."""
    if obj is None:
      return lambda *__, **_: None
    return self.getWrappedFunction(obj)

  def __set__(self, *_) -> Never:
    """
    Implementation of descriptor setter. Disabled, raises TypeError.
    :raise TypeError: Always raised as setting is disabled.
    """
    raise TypeError

  def __delete__(self, *_) -> Never:
    """
    Implementation of descriptor deletion. Disabled, raises TypeError.
    :raise TypeError: Always raised as deletion is disabled.
    """
    raise TypeError

  def __str__(self, ) -> str:
    """String Representation"""
    target = self.getTargetClass().__qualname__
    method = self.getName()
    return '%s.%s' % (target, method)

  def __repr__(self, ) -> str:
    """Code Representation"""
    target = self.getTargetClass().__qualname__
    method = self.getName()
    return '%s.%s' % (target, method)
