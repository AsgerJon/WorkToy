"""WorkToy - Core - Local
Provides the class with access to the base classes with delayed local
import."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from icecream import ic

from worktoy.core import Function, Bases

if TYPE_CHECKING:
  from worktoy.base import DefaultClass

ic.configureOutput(includeContext=True)


class MetaDecorator(type):
  """Allows calling the decorator to behave the same as an instance."""

  __core_instance__ = None

  def __init__(cls, name: str, bases: Bases, nameSpace: dict, **kw) -> None:
    type.__init__(cls, name, bases, nameSpace, **kw)
    self = cls.__new__(cls, )
    setattr(cls, '__core_instance__', self)


class Decorator(metaclass=MetaDecorator):
  """WorkToy - Core - Local
  Provides the class with access to the base classes with delayed local
  import."""

  __core_instance__ = None

  def __call__(self, other: type) -> type:
    """Decorates the other class."""
    ic(other)
    setattr(other, '__default_class_instance__', None)
    source = getattr(self.__class__, '__create_default_instance__', None)
    if source is None:
      raise TypeError
    setattr(other, '__create_default_instance__', source)
    source = getattr(self.__class__, '__get_default_instance__', None)
    if source is None:
      raise TypeError
    setattr(other, '__get_default_instance__', source)
    source = getattr(self.__class__, '__getattr__', None)
    if source is None:
      raise TypeError
    setattr(other, '__getattr__', source)
    return other

  def __create_default_instance__(cls, *args, **kwargs) -> None:
    """Creator-function for the default class instance."""
    if not isinstance(cls, type):
      if kwargs.get('_recursion', False):
        raise RecursionError
      return cls.__create_default_instance__(cls.__class__, _recursion=True)
    ic(cls)
    if getattr(cls, '__default_class_instance__', None) is None:
      from worktoy.base import DefaultClass
      setattr(cls, '__default_class_instance__', DefaultClass())

  def __get_default_instance__(cls, *args, **kwargs, ) -> DefaultClass:
    """Getter-function for the default class instance."""
    if not isinstance(cls, type):
      return cls.__get_default_instance__(cls.__class__)
    if getattr(cls, '__default_class_instance__', None) is None:
      if kwargs.get('_recursion', False):
        msg = ['Encountered RecursionError when trying to create',
               'instance of DefaultClass.']
        raise RecursionError(' '.join(msg))
      from worktoy.base import DefaultClass
      setattr(cls, '__default_class_instance__', DefaultClass())
    return getattr(cls, '__default_class_instance__', None)

  def __getattr__(cls, *args, **kwargs) -> Function:
    """Tries to find key on instance of default class"""
    key = None
    for arg in args:
      if isinstance(arg, str) and key is None:
        key = arg
    if not isinstance(cls, type):
      parent = object.__getattribute__(cls, '__class__')
      return object.__getattribute__(parent, key)
    defaultInstanceGetter = (
      object.__getattribute__(cls, '__get_default_instance__'))
    defaultInstance = defaultInstanceGetter()

    def __wrapped_method__(*args, **kwargs) -> object:
      """Wrapper on the method retrieved from the defaultInstance."""
      from worktoy.base import DefaultClass
      func = getattr(DefaultClass, key, None)
      if func is None:
        raise AttributeError(key)
      if not isinstance(func, Function):
        msg = 'Expected callable key: %s, but received type: %s!'
        raise TypeError(msg % (key, type(func)))
      try:
        return func(defaultInstance, *args, **kwargs)
      except TypeError as e:
        if 'argument' in str(e).lower():
          try:
            func(*args)
          except TypeError as e2:
            raise e2 from e

    ic(cls)

    return __wrapped_method__
