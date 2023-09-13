"""WorkToy - Core - MetaMetaClass
The meta-metaclass implements __repr__ and __str__ for even the
metaclasses themselves. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic

from worktoy.core import Bases

ic.configureOutput(includeContext=True)


class _MetaMetaClass(type):
  """The meta-metaclass implements __repr__ and __str__ for even the
  metaclasses themselves."""

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs) -> dict:
    """Implementing the nameSpace generation"""
    return dict()

  def __new__(mcls,
              name: str,
              bases: Bases,
              nameSpace: dict,
              **kwargs) -> type:
    out = type.__new__(mcls, name, bases, nameSpace, **kwargs)
    if mcls is _MetaMetaClass:
      setattr(out, '__meta_metaclass__', mcls)
    return out

  def __init__(cls,
               name: str,
               bases: Bases,
               nameSpace: dict,
               **kwargs) -> None:
    type.__init__(cls, name, bases, nameSpace, **kwargs)

  def __call__(cls, *args, **kwargs) -> Any:
    return type.__call__(cls, *args, **kwargs)

  def __str__(cls) -> str:
    """String Representation"""
    return cls.__qualname__

  def __repr__(cls) -> str:
    """Code Representation"""
    return cls.__qualname__


class MetaMetaClass(_MetaMetaClass, metaclass=_MetaMetaClass):
  """This class is both derived from and subclass of the _MetaMetaClass."""

  def __new__(mcls,
              name: str = None,
              bases: Bases = None,
              nameSpace: dict = None,
              **kwargs) -> type:
    return _MetaMetaClass.__new__(mcls, name, bases, nameSpace, **kwargs)

  def __init__(cls,
               name: str = None,
               bases: Bases = None,
               nameSpace: dict = None,
               **kwargs) -> None:
    _MetaMetaClass.__init__(cls, name, bases, nameSpace, **kwargs)

  def __call__(cls, *args, **kwargs) -> Any:
    return _MetaMetaClass.__call__(cls, *args, **kwargs)
