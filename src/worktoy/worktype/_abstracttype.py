"""AbstractType provides a basic implementation of the type related
classes"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from icecream import ic

from worktoy.worktype import AbstractMetaType, TypeNameSpace

ic.configureOutput(includeContext=True)


class AbstractType(AbstractMetaType):
  """AbstractType is the base metaclass for the type related classes"""

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple) -> TypeNameSpace:
    """Implementing the special type namespace class"""
    out = TypeNameSpace(name, bases)
    return out

  def __new__(mcls, name: str, bases: tuple, nameSpace: TypeNameSpace,
              **kwargs) -> type:
    nameSpace = nameSpace.asDict()
    return super().__new__(mcls, name, bases, nameSpace, **kwargs)

  def __init__(cls,
               name: str,
               bases: tuple,
               nameSpace: TypeNameSpace,
               **kwargs) -> None:
    """Invokes the protocolify method on the namespace after initializing
    the super init"""
    super().__init__(name, bases, nameSpace.asDict(), **kwargs)
    nameSpace.protocolify()

  def __contains__(cls, element: object) -> bool:
    return isinstance(element, cls)

  @abstractmethod
  def __instancecheck__(cls, obj: object) -> bool:
    """Subclasses must implement this method"""
