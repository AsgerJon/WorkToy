"""
WorkToy - MetaClass - WorkToyMeta
This metaclass enhances class creation by exposing metaclass level dunder
methods to the normal class body.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic

from worktoy.core import Bases, Function
from worktoy.metaclass import AbstractMetaClass, AbstractNameSpace

ic.configureOutput(includeContext=True)


class WorkToyMeta(AbstractMetaClass):
  """WorkToy - MetaClass - WorkToyMeta
  This metaclass enhances class creation by exposing metaclass level dunder
  methods to the normal class body."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> Any:
    """Provides the default namespace"""
    nameSpace = AbstractNameSpace()
    return nameSpace

  def __str__(cls, ) -> str:
    """String representation"""
    clsStr = getattr(cls, '__cls_str__', None)
    if not isinstance(clsStr, Function):
      return AbstractMetaClass.__str__(cls)
    return clsStr(cls, )

  def __repr__(cls, ) -> str:
    """Code representation"""
    clsRepr = getattr(cls, '__cls_repr__', None)
    if not isinstance(clsRepr, Function):
      return AbstractMetaClass.__repr__(cls)
    return clsRepr(cls)

  def __iter__(cls) -> type:
    clsIter = getattr(cls, '__cls_iter__', None)
    if clsIter is None:
      msg = """'%s' object is not iterable""" % cls.__qualname__
      raise TypeError(msg)
    return clsIter()

  def __next__(cls, ) -> Any:
    clsNext = getattr(cls, '__cls_next__', None)
    if clsNext is None:
      msg = """AttributeError: type object '%s' has no attribute 
        '__next__'."""
      raise TypeError(msg % cls.__qualname__)
    return clsNext()

  def __contains__(cls, item) -> bool:
    clsContains = getattr(cls, '__cls_contains__', None)
    if clsContains is None:
      return AbstractMetaClass.__contains__(cls, item)
    return clsContains(cls, item)

  def __len__(cls, ) -> int:
    clsLen = getattr(cls, '__cls_len__', None)
    if clsLen is None:
      msg = """object of type '%s' has no len()"""
      raise TypeError(msg % cls.__qualname__)
    return clsLen()
