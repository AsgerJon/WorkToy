"""WorkToy - SYM - SyMeta
Metaclass implementing Symbolic classes.

"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Union

from worktoy.base import DefaultClass
from worktoy.core import Bases
from worktoy.guards import TypeGuard, NoneGuard, SomeGuard
from worktoy.metaclass import AbstractMetaClass
from worktoy.sym import SymSpace, SYM
from icecream import ic

ic.configureOutput(includeContext=True)


class _SyMeta(AbstractMetaClass):
  """WorkToy - SYM - SyMeta
  Metaclass implementing Symbolic classes. """

  dictGuard = TypeGuard(dict)
  requireNone = SomeGuard()  # (arg: None) -> arg
  requireSome = NoneGuard()  # (arg: None) -> error

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    """Returning special namespace class."""
    return SymSpace(name, bases, **kwargs)

  def __new__(mcls, name: str, bases: Bases, data: SymSpace, **kw) -> type:
    nameSpace = data.getNameSpace()
    instanceSpace = data.getInstanceSpace()
    out = AbstractMetaClass.__new__(mcls, name, bases, nameSpace, **kw)
    setattr(out, '__instance_space__', instanceSpace)
    setattr(out, '__symbolic_instances__', {})
    return out

  def __init__(cls, *args, **kwargs) -> None:
    type.__init__(cls, *args, **kwargs)
    symbolicInstances = getattr(cls, '__symbolic_instances__', None)
    instanceSpace = getattr(cls, '__instance_space__', None)
    symbolicInstances = cls.dictGuard(symbolicInstances,
                                      '__symbolic_instances__')
    instanceSpace = cls.dictGuard(instanceSpace,
                                  '__instance_space__')
    for (i, (key, val)) in enumerate(instanceSpace.items()):
      val.setInnerClass(cls)
      val.setValue(i)
      newInstance = cls(*val.getArgs(), **val.getKwargs(), )
      instances = getattr(cls, '__symbolic_instances__')
      val.setInnerInstance(newInstance)
      instances |= {key.lower(): val}

  def __call__(cls, *args, **kwargs) -> Any:
    if kwargs.get('__instance_creation__', False):
      return type.__call__(cls, *args, **kwargs)
    strArg = None
    intArg = None
    for arg in args:
      if isinstance(arg, str) and strArg is None:
        strArg = arg
      if isinstance(arg, int) and intArg is None:
        intArg = arg
    instances = getattr(cls, '__symbolic_instances__')
    for (key, val) in instances.items():
      if key in [strArg, intArg]:
        return val

  def getInstances(cls, ) -> dict[str, SYM]:
    """Getter-function for symbolic instances."""
    return getattr(cls, '__symbolic_instances__')

  def getInstanceAtIndex(cls, index: int) -> SYM:
    """Getter-function for the item at the given index."""
    for (key, val) in cls.getInstances().items():
      if val._value == index:
        return val
    raise IndexError(index)

  def getInstanceAtKey(cls, key: str) -> SYM:
    """Getter-function for the item at the given key."""
    for (key, val) in cls.getInstances().items():
      if val._name == key:
        return val
    raise KeyError(key)

  def __len__(cls, ) -> int:
    """Number of symbolic instances"""
    return len(cls.getInstances().keys())

  def __iter__(cls, ) -> type:
    """Implementation of iteration"""
    setattr(cls, '__current_index__', 0)
    return cls

  def __next__(cls, ) -> SYM:
    """Implementation of iteration"""
    ind = getattr(cls, '__current_index__')
    if ind + 1 > len(cls):
      raise StopIteration
    setattr(cls, '__current_index__', ind + 1)
    return cls.getInstanceAtIndex(ind)

  def __getitem__(cls, key: Union[str, int]) -> SYM:
    """Getter implementation"""
    if isinstance(key, int):
      return cls.getInstanceAtIndex(key)
    if isinstance(key, str):
      return cls.getInstanceAtKey(key)
    raise TypeError


class SyMeta(DefaultClass, metaclass=_SyMeta):
  """In between class exposing the metaclass."""
  pass
