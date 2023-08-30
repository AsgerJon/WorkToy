"""WorkToy - Core - Quick
This class sets a descriptor on the decorated class pointing to the
DefaultClass, but which defers import to avoid circular imports."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from worktoy.base import DefaultClass


class Quick:
  """WorkToy - Core - Quick
  This class sets a descriptor on the decorated class pointing to the
  DefaultClass, but which defers import to avoid circular imports."""
  _varName = '__default_class_instance__'

  def __init__(self, *args, **kwargs) -> None:
    pass

  def __call__(self, cls: type) -> type:
    self.__set_attributes__(cls)
    return cls

  @staticmethod
  def __set_attributes__(cls: type) -> None:
    """Setter function for the attributes"""
    _varName = Quick._varName
    setattr(cls, _varName, None)

    originalInit = getattr(cls, '__init__', None)
    if originalInit is None:
      raise TypeError

    def wrapInit(*args, **kwargs) -> None:
      """Wrapped Init"""
      self = None
      newArgs = []
      for arg in args:
        if isinstance(arg, cls) and self is None:
          self = arg
        else:
          newArgs.append(arg)
      setattr(self, _varName, getattr(cls, Quick._varName))
      originalInit(self, *newArgs, **kwargs)

    setattr(cls, '__init__', wrapInit)

    def wrap__getattr__(obj: object, key: str) -> object:
      """Wrapped getattr"""
      if isinstance(obj, type):
        theClass = obj
      else:
        theClass = object.__getattribute__(obj, '__class__')
      try:
        base = object.__getattribute__(theClass, _varName)
        if base is None:
          raise AttributeError('lmao')
      except AttributeError:
        from worktoy.base import DefaultClass
        base = DefaultClass()
        setattr(theClass, _varName, base)
      return object.__getattribute__(base, key)

    setattr(cls, '__getattr__', wrap__getattr__)

  @staticmethod
  def __explicit_getter_function__(cls: type, ) -> DefaultClass:
    return getattr(cls, Quick._varName, None)

  @staticmethod
  def __explicit_creator_function__() -> DefaultClass:
    from worktoy.base import DefaultClass
    return DefaultClass()

  @staticmethod
  def __getter_function__(cls: object) -> DefaultClass:
    if not isinstance(cls, type):
      raise NotImplementedError
    value = getattr(cls, Quick._varName, None)
    if value is None:
      raise NotImplementedError
    return value
