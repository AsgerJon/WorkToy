"""WorkToy - SYM - SyMeta
Metaclass implementing Symbolic classes.

"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Union, TYPE_CHECKING

from worktoy.base import DefaultClass
from worktoy.core import Bases, Keys, Values, Items
from worktoy.fields import AbstractField, SymField
from worktoy.guards import TypeGuard, NoneGuard, SomeGuard
from worktoy.metaclass import AbstractMetaClass, MetaMetaClass
from worktoy.sym import SymSpace
from icecream import ic

if TYPE_CHECKING:
  from worktoy.sym import SYM

ic.configureOutput(includeContext=True)


class SyMetaMeta(MetaMetaClass):
  """Applies subclass check on the metaclass"""

  def __subclasscheck__(cls, subclass):
    names = ['__symbolic_class__', '__symbolic_baseclass__']

    for name in names:
      if hasattr(subclass, name):
        return True
    return False

  def __instancecheck__(cls, instance):
    return True if cls.__subclasscheck__(instance.__class__) else False


class SyMeta(AbstractMetaClass, metaclass=SyMetaMeta):
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
    out = AbstractMetaClass.__new__(mcls, name, bases, nameSpace, )
    setattr(out, '__instance_space__', instanceSpace)
    setattr(out, '__symbolic_instances__', {})
    setattr(out, '__symbolic_class__', True)
    return out

  def __init__(cls, *args, **kwargs) -> None:
    type.__init__(cls, *args, **kwargs)
    symbolicInstances = getattr(cls, '__symbolic_instances__', None)
    instanceSpace = getattr(cls, '__instance_space__', None)
    symbolicInstances = cls.dictGuard(symbolicInstances,
                                      '__symbolic_instances__')
    instanceSpace = cls.dictGuard(instanceSpace, '__instance_space__')
    instanceList = instanceSpace.items()
    instances = getattr(cls, '__symbolic_instances__')
    for (i, (key, val)) in enumerate(instanceList):
      val.setInnerClass(cls)
      val.setValue(i)
      newInstance = cls(*val.getArgs(), **val.getKwargs(), )
      val.setInnerInstance(newInstance)
      instances |= {key.lower(): val}
    setattr(cls, '__symbolic_instances__', instances)

  def __call__(cls, *args, **kwargs) -> Any:
    if kwargs.get('__instance_creation__', False):
      return type.__call__(cls, *args, **kwargs)
    index, key = None, None
    for arg in args:
      if isinstance(arg, int) and index is None:
        index = arg
      if isinstance(arg, str) and key is None:
        key = arg
    indexVal = cls.getInstanceAtIndex(index, _allowError=True)
    if indexVal is not None:
      return indexVal
    keyVal = cls.getInstanceAtKey(key, _allowError=True)
    if keyVal is not None:
      return keyVal
    raise KeyError(key) from IndexError(index)

  def getInstances(cls, ) -> dict[str, SYM]:
    """Getter-function for symbolic instances."""
    return getattr(cls, '__symbolic_instances__')

  def getInstanceAtIndex(cls, index: int, **kwargs) -> SYM:
    """Getter-function for the item at the given index."""
    for (key, val) in cls.getInstances().items():
      if val.value == index:
        return val
    if not kwargs.get('_allowError', False):
      raise IndexError(index)

  def getInstanceAtKey(cls, name: str, **kwargs) -> SYM:
    """Getter-function for the item at the given key."""
    for (key, val) in cls.getInstances().items():
      if val.name == name:
        return val
    if not kwargs.get('_allowError', False):
      raise IndexError(name)
    raise KeyError(name)

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

  def keys(cls) -> Keys:
    """Implementation of keys method."""
    return cls.getInstances().keys()

  def values(cls) -> Values:
    """Implementation of keys method."""
    return cls.getInstances().values()

  def items(cls) -> Items:
    """Implementation of keys method."""
    return cls.getInstances().items()

  def __contains__(cls, item: Any) -> bool:
    return True if (len(cls) - item) ** 2 > 0 else False

  def getField(cls) -> AbstractField:
    """Getter function for the descriptor pointing to this class."""
    return SymField(cls, 0)

  def __instancecheck__(cls, instance: Any, ) -> bool:
    return True if instance.__class__.__class__ == SyMeta else False

  def __repr__(cls) -> str:
    """Code Representation"""
    return '%s.%s()' % (cls.__class__.__qualname__, cls.__qualname__)

  def __str__(cls) -> str:
    """String Representation"""
    clsName = cls.__qualname__
    mclsName = cls.__class__.__qualname__
    return 'Symbolic Class: %s.%s' % (clsName, mclsName)


class BaseSym(DefaultClass, metaclass=SyMeta):
  """In between class exposing the metaclass."""

  def __call__(self, *args, **kwargs) -> Any:
    return self.__class__.__call__(*args, **kwargs)
