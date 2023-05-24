"""Marker is a factory for method decorators. """
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import Any, Never, NoReturn

from worktoy.core import CallMeMaybe, maybe
from worktoy.field import Field
from worktoy.waitaminute import ExceptionCore


@Field('__doc__', type_=str, )
@Field('__annotations__', type_=dict, defVal={}, )
class Marker:
  """Marker is a factory for method decorators.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  @classmethod
  def _proceduralError(cls) -> Never:
    """Handles procedural errors"""
    raise ExceptionCore('Procedural error!')

  def __init__(self, *args, **kwargs) -> None:
    self._func = None
    self._loadDocs()

  def _loadDocs(self) -> NoReturn:
    """Loads the docs"""
    with open('_config.inf', 'r', encoding='utf-8') as f:
      doc = f.read()
    self.__doc__ = '\n'.join([self.__doc__, doc])

  def __call__(self, *args, **kwargs) -> Marker:
    """When called on a function, the function is absorbed, and the marker
    self is returned. """
    if self._func is None:
      self._func = args[0]
      return self
    self._invokeFunction(*args, **kwargs)

  def _functionSetter(self, func: CallMeMaybe) -> NoReturn:
    """Setter-function for the function. This may also be implemented in
    subclasses for customizing the function directly."""
    if self._func is not None:
      self._proceduralError()
    self._func = func

  def _invokeFunction(self, *args, **kwargs) -> Any:
    """This is the method responsible for invoking the absorbed function.
    It is also this method which subclasses should reimplement as it
    permits direct access to function calls."""
    if self._func is None:
      self._proceduralError()
    return self._func(*args, **kwargs)


@Field('key', type_=str, defVal=None, allowSet=False)
class Factory(Marker):
  """Marks the decorated function with a key value at the attribute named
  factory"""

  def __init__(self, *args, **kwargs) -> None:
    Marker.__init__(self, *args, **kwargs)

  def _functionSetter(self, func: CallMeMaybe) -> NoReturn:
    """Reimplementation"""
    setattr(func, '__factory__', self.key)
    return Marker._functionSetter(self, func)


class Validator(Marker):
  """Sets a method to be a validator"""

  def __init__(self, *args, **kwargs) -> None:
    Marker.__init__(self, *args, **kwargs)

  def _functionSetter(self, func: CallMeMaybe) -> NoReturn:
    """Reimplementation"""
    setattr(func, '__validator__', True)
    return Marker._functionSetter(self, func)


class Method(Marker):
  """Sets a method to be transferable meaning that it may be copied on to
  a target class."""

  def __init__(self, *args, **kwargs) -> None:
    Marker.__init__(self, *args, **kwargs)

  def _functionSetter(self, func: CallMeMaybe) -> NoReturn:
    """Reimplementation"""
    setattr(func, '__method__', True)
    return Marker._functionSetter(self, func)
