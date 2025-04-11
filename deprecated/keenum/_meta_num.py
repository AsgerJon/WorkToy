"""MetaNum provides the metaclass for the KeeNum class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

from worktoy.mcls import AbstractMetaclass
from worktoy.keenum import Num, SpaceNum

try:
  from typing import Any
except ImportError:
  Any = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

try:
  from typing import Self
except ImportError:
  Self = object

try:
  from typing import Callable
except ImportError:
  Callable = object

try:
  from typing import Never
except ImportError:
  try:
    from typing import NoReturn as Never
  except ImportError:
    Never = object

if TYPE_CHECKING:
  NumList = list[Num]


class MetaNum(AbstractMetaclass):
  """MetaNum provides the metaclass for the KeeNum class. """

  __iter_contents__ = None
  __allow_instantiation__ = None

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> SpaceNum:
    """The __prepare__ method is invoked before the class is created."""
    return SpaceNum(mcls, name, bases, **kwargs)

  def __new__(mcls,
              name: str,
              bases: tuple,
              space: SpaceNum,
              **kwargs) -> type:
    """The __new__ method is invoked when the class is created."""
    cls = AbstractMetaclass.__new__(mcls, name, bases, space, **kwargs)
    return cls

  def __init__(cls,
               name: str,
               bases: tuple,
               namespace: dict,
               **kwargs) -> None:
    """The __init__ method is invoked when the class is created."""
    AbstractMetaclass.__init__(cls, name, bases, namespace, **kwargs)
    setattr(cls, '__allow_instantiation__', True)
    numEntries = getattr(cls, '__num_entries__', [])
    keenumDict = getattr(cls, '__keenum_dict__', {})
    for num in numEntries:
      name = num.getPublicName()
      publicValue = num.getPublicValue()
      privateValue = num.getPrivateValue()
      keenum = cls(publicValue)
      keenum.setPrivateValue(privateValue)
      keenum.setPublicName(name)
      keenumDict[name] = keenum
    setattr(cls, '__keenum_dict__', keenumDict)
    setattr(cls, '__allow_instantiation__', False)

  def __call__(cls, key: object) -> Any:
    """Get the Num entry by key."""
    allowInstantiation = getattr(cls, '__allow_instantiation__', False)
    if allowInstantiation:
      self = AbstractMetaclass.__call__(cls, key)
      return self
    return cls._resolveNum(key)

  def _getKeeNumList(cls, ) -> list:
    """Get the list of KeeNum instances."""
    keenumDict = getattr(cls, '__keenum_dict__', {})
    keenumList = [v for (k, v) in keenumDict.items()]
    return sorted(keenumList, key=lambda x: int(x))

  def _getKeeNumDict(cls, ) -> dict:
    """Get the dictionary of KeeNum instances."""
    keenumDict = getattr(cls, '__keenum_dict__', {})
    if not keenumDict:
      e = """Class: '%s' has no KeeNum instances!""" % cls.__name__
      raise AttributeError(monoSpace(e))
    return keenumDict

  def _resolveNum(cls, identifier: object, **kwargs) -> Any:
    """Resolve the Num entry."""
    if isinstance(identifier, tuple):
      if len(identifier) == 1:
        return cls._resolveNum(identifier[0])
      e = """Received identifier: '%s' of type: '%s' which is not
      supported!""" % (identifier, type(identifier).__name__)
      raise TypeError(monoSpace(e))
    if isinstance(identifier, str):
      return cls._resolveKey(identifier)
    if isinstance(identifier, int):
      return cls._resolveIndex(identifier)
    if kwargs.get('_recursion', False):
      raise RecursionError
    if isinstance(identifier, cls):
      return identifier
    e1 = """Received identifier: '%s' of type: '%s' which is not 
    supported!"""
    e2 = """Supported types are: 'str' and 'int'!"""
    actType = type(identifier).__name__
    idStr = str(identifier)
    e = [e1 % (idStr, actType), e2]
    raise TypeError(monoSpace('\n'.join(e)))

  def _resolveKey(cls, key: str, ) -> Any:
    """Resolve a string typed key"""
    keenumDict = cls._getKeeNumDict()
    if key in keenumDict:
      return keenumDict[key]
    if key.lower() in keenumDict:
      return keenumDict[key.lower()]
    e1 = """KeeNum class: '%s' could not resolve the key: '%s'!"""
    e2 = """Supported keys are: \n%s """
    keys = ', '.join([k for k in keenumDict.keys()])
    e = [e1 % (cls.__name__, key), e2 % keys]
    raise KeyError(monoSpace('\n'.join(e)))

  def _rollIndex(cls, index: int) -> int:
    """Roll the index."""
    if index > len(cls):
      e1 = """Index: '%d' exceeds the length of the KeeNum class: '%s' 
      which has only '%d' members!"""
      e2 = e1 % (index, cls.__name__, len(cls))
      raise IndexError(monoSpace(e2))
    if index < 0:
      return cls._rollIndex(len(cls) + index)
    return index

  def _resolveIndex(cls, index: int) -> Any:
    """Resolve an integer typed index."""
    return cls._getKeeNumList()[cls._rollIndex(index)]

  def __iter__(cls, ) -> Self:
    """Implement the iterator protocol."""
    cls.__iter_contents__ = cls._getKeeNumList()
    return cls

  def __next__(cls, ) -> Any:
    """Implement the iterator protocol."""
    if cls.__iter_contents__:
      return cls.__iter_contents__.pop(0)
    raise StopIteration

  def __len__(cls, ) -> int:
    """Implement the length protocol."""
    return len(cls._getKeeNumList())

  def __getitem__(cls, key: object) -> Any:
    """Get the Num entry by key."""
    return cls._resolveNum(key)

  def __contains__(cls, key: object) -> bool:
    """Check if the key is in the KeeNum class."""
    try:
      cls._resolveNum(key)
      return True
    except (KeyError, TypeError):
      return False

  def __getattr__(cls, key: str) -> Any:
    """Get the Num entry by key."""
    try:
      return cls._resolveNum(key, _recursion=True)
    except (KeyError, TypeError):
      return object.__getattribute__(cls, key)
