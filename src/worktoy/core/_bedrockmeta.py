"""BedrockMeta is a metaclass providing other metaclass with __str__ and
__repr__ such that the metaclass itself can have reasonable
representations."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import MutableMapping, Any, Never

from icecream import ic

from worktoy.core import nameSpaceValidator

ic.configureOutput(includeContext=True)

ArgTuple = tuple[list[object], dict[str, object]]

Bases = tuple[type]
Map = MutableMapping[str, Any]


class _BedrockMetaMeta(type):
  """This is the actual bedrock meta. The metaclass imported has this
  class as both metaclass and parent class."""

  _methodNames = ['__init_subclass__', '__repr__', '__str__', '__new__']

  @staticmethod
  def errorHandleFactory(cls, nameSpace: object, ) -> object:
    """Raises the NameSpaceError"""
    nameSpaceClass = nameSpace.__class__
    originClass = cls

    def errorHandle(exception: Exception) -> Never:
      """Error handler"""
      from worktoy.waitaminute import NameSpaceError
      raise NameSpaceError(nameSpaceClass, originClass, exception)

    return errorHandle

  @staticmethod
  def __validate_namespace__(cls, nameSpace: object) -> bool:
    """Validates that the name space returned by the __prepare__ method
    supports the necessary functionality."""
    nameSpaceClass = nameSpace.__class__
    callBack = cls.errorHandleFactory(cls, nameSpaceClass)
    return True if nameSpaceValidator(nameSpaceClass, callBack) else False

  def __init_subclass__(cls, *args, **kwargs) -> None:
    """This must be stated explicitly"""
    # ic(cls, args, kwargs)

  def __repr__(cls) -> str:
    """Code Representation"""
    return cls.__qualname__

  def __str__(cls) -> str:
    """String Representation"""
    return cls.__qualname__

  def __new__(mcls, *args, **kwargs) -> type:
    """Implementation of __new__"""
    cls = super().__new__(mcls, *args, **kwargs)
    for name in mcls._methodNames:
      existingMethod = getattr(cls, name, None)
      metaclassMethod = getattr(mcls, name, None)
      if metaclassMethod is None:
        errorMessage = 'Method named %s must be defined on metaclass!'
        raise NameError(errorMessage % name)
      if existingMethod is None:
        setattr(cls, name, metaclassMethod)
    originalPrepare = getattr(cls, '__prepare__', None)
    if originalPrepare is None:
      return cls

    def wrap(metaclass, *args2, **kwargs2) -> object:
      """Wrapper on the __prepare__"""
      nameSpace = originalPrepare(metaclass, *args2, **kwargs2)
      if cls.__validate_namespace__(cls, nameSpace):
        return nameSpace

    setattr(cls, '__prepare__', wrap)

    return cls


class BedrockMeta(_BedrockMetaMeta, metaclass=_BedrockMetaMeta):
  """This in between class both inherits and uses as metaclass the
  meta-metaclass. This is a convenient parent class for new metaclasses."""

  def __new__(mcls,
              name: str,
              bases: Bases,
              nameSpace: Map,
              **kwargs) -> type:
    return super().__new__(mcls, name, bases, nameSpace, **kwargs)

  def __init__(cls,
               name: str,
               bases: Bases,
               nameSpace: Map,
               **kwargs) -> None:
    if isinstance(nameSpace, dict):
      super().__init__(name, bases, nameSpace, **kwargs)

  def __call__(cls, *args, **kwargs) -> object:
    """Instance Creation and initialization"""
    return super().__call__(*args, **kwargs)


class Bedrock(metaclass=BedrockMeta):
  """This regular class provides a parent class for new classes."""
  pass
