"""WorkToy - SYM - SyMeta
Metaclass implementing Symbolic classes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from icecream import ic

from worktoy.base import DefaultClass
from worktoy.core import Bases
from worktoy.guards import TypeGuard, NoneGuard, SomeGuard
from worktoy.metaclass import AbstractMetaClass, MetaMetaClass
from worktoy.sym import SYM, SymSpace

if TYPE_CHECKING:
  pass

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
    instanceSpace = {k.lower(): v for (k, v) in instanceSpace.items()}
    out = AbstractMetaClass.__new__(mcls, name, bases, nameSpace, )
    setattr(out, '__instance_space__', instanceSpace)
    setattr(out, '__symbolic_instances__', {})
    setattr(out, '__symbolic_class__', True)
    return out

  def __init__(cls, *args, **kwargs) -> None:
    type.__init__(cls, *args, **kwargs)
    symNames = kwargs.get('symNames', {})
    for key, val in symNames.items():
      sym = SYM()
      sym.__set_name__(cls, key.lower())
      setattr(sym, 'value', val)

  def __call__(cls, *args, **kwargs) -> Any:
    if kwargs.get('__instance_creation__', False):
      return type.__call__(cls, *args, **kwargs)
    index, key = None, None
    for arg in args:
      if isinstance(arg, int) and index is None:
        index = arg
      if isinstance(arg, str) and key is None:
        key = arg
    if key is not None:
      keyVal = cls.getInstanceAtKey(key.lower(), _allowError=True)
      if keyVal is not None:
        return keyVal
    indexVal = cls.getInstanceAtIndex(index, _allowError=True)
    if indexVal is not None:
      return indexVal

  def getInstances(cls, ) -> list[SYM]:
    """Getter-function for symbolic instances."""
    return getattr(cls, '__symbolic_instances__')

  def getInstanceAtIndex(cls, index: int, **kwargs) -> SYM:
    """Getter-function for the item at the given index."""
    existing = getattr(cls, '__symbolic_instances__', None)
    for (i, item) in enumerate(existing):
      if i == index:
        return item

  def getInstanceAtKey(cls, name: str, **kwargs) -> SYM:
    """Getter-function for the item at the given key."""
    existing = getattr(cls, '__symbolic_instances__', [])
    for (i, item) in enumerate(existing):
      if item.getName().lower() == name.lower():
        return item
    raise KeyError(name)

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

  def __getattr__(cls, key: str) -> Any:
    try:
      return object.__getattribute__(cls, key.lower())
    except AttributeError as e:
      raise e


class BaseSym(DefaultClass, metaclass=SyMeta):
  """In between class exposing the metaclass."""

  def __call__(self, *args, **kwargs) -> Any:
    return self.__class__.__call__(*args, **kwargs)
