"""MetaType provides a meta-metaclass for use across modules in the
WorkToy package"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, MutableMapping, Any

from icecream import ic

from worktoy import DefaultClass

if TYPE_CHECKING:
  Bases = tuple[type]
  Map = MutableMapping[str, Any]

ic.configureOutput(includeContext=True)  # Removed before production


class _MetaMeta(type):
  """The meta type is a meta-metaclass required to implement __str__ and
  __repr__ on the class level."""

  def __repr__(cls) -> str:
    """Code Representation"""
    if cls is _MetaMeta:
      return '_MetaMeta'
    return cls.__qualname__

  def __str__(cls) -> str:
    """String Representation"""
    if cls is _MetaMeta:
      return '_MetaMeta'
    return cls.__qualname__


class AbstractMetaType(_MetaMeta, metaclass=_MetaMeta):
  """The abstract metaclass intended for use in the rest of the package"""

  @classmethod
  def __prepare__(mcls, name, bases) -> object:
    """Implements the prepare method. Subclasses should primarily use a
    custom namespace class to customize the classes."""
    return super().__prepare__(name, bases)

  def __new__(mcls,
              name: str,
              bases: Bases,
              nameSpace: dict,
              **kwargs) -> type:
    newBases = []
    for base in bases:
      if base not in newBases:
        newBases.append(base)
    if DefaultClass not in newBases:
      newBases.append(DefaultClass)
    bases = (*newBases,)
    return super().__new__(mcls, name, bases, nameSpace, **kwargs)

  def __init__(cls,
               name: str,
               bases: Bases,
               nameSpace: dict,
               **kwargs) -> None:
    super().__init__(name, bases, nameSpace, **kwargs)


class AbstractType(DefaultClass, metaclass=AbstractMetaType):
  """Classes no implementing a custom metaclass should inherit this class"""
  pass
