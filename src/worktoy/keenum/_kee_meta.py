"""
KeeMeta provides the metaclass creating the KeeNum enumeration class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..attr import Field
from ..mcls import AbstractMetaclass
from ..parse import maybe
from ..static import AbstractObject
from ..waitaminute import MissingVariable, TypeException
from ..waitaminute import IllegalInstantiation
from . import KeeSpace, _KeeNumBase

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Any, Iterator

  Bases: TypeAlias = tuple[type, ...]
  MTypes: TypeAlias = dict[str, type]

try:
  from icecream import ic  # NOQA

  ic.configureOutput(includeContext=True, )
except ImportError:
  print('icecream not installed, using dummy ic function.')
  ic = print


class KeeMeta(AbstractMetaclass):
  """
  KeeMeta provides the metaclass creating the KeeNum enumeration class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __core_keenum__ = None  # Future KeeNum base class

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _createCoreKeeNum(mcls, ) -> Self:
    """
    Creator function for the core KeeNum class.
    """

    class KeeNum(_KeeNumBase, metaclass=mcls):
      """
      KeeNum provides the base class for enumerating classes with
      restricted and predefined instances called members.
      """
      pass

    setattr(mcls, '__core_keenum__', KeeNum)

  @classmethod
  def getCoreKeeNum(mcls, **kwargs) -> type:
    """
    Get the core KeeNum class.
    """
    if mcls.__core_keenum__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      mcls._createCoreKeeNum()
      return mcls.getCoreKeeNum(_recursion=True)
    if isinstance(mcls.__core_keenum__, type):
      return mcls.__core_keenum__
    name, value = '__core_keenum__', mcls.__core_keenum__
    raise TypeException(name, value, type)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> KeeSpace:
    """
    Prepare the class namespace.
    """
    return KeeSpace(mcls, name, bases, **kwargs)

  def __new__(mcls, name: str, bases: Bases, space: KeeSpace, **kw) -> Self:
    """
    Create a new instance of the KeeMeta metaclass.
    """
    if mcls.__core_keenum__ is None:
      if name == 'KeeNum' or kw.get('_root', False):
        return super().__new__(mcls, name, bases, space, **kw)
      raise RuntimeError
    coreKeeNum = mcls.getCoreKeeNum()
    return super().__new__(mcls, name, (coreKeeNum,), space, **kw)

  def __init__(cls, name: str, bases: Bases, space: KeeSpace, **kw) -> None:
    """
    Initialize the KeeMeta metaclass.
    """
    super().__init__(name, bases, space, **kw)
    if name == 'KeeNum':
      return
    futureEntries = getattr(cls, '__future_entries__', )
    if futureEntries is None:
      raise MissingVariable('__future_entries__', dict)
    if not isinstance(futureEntries, dict):
      raise TypeException('__future_entries__', futureEntries, dict)
    actualEntries = dict()
    valueType = getattr(cls, '__future_value_type__', )
    memberValues = []
    memberNames = []
    for i, (name, value) in enumerate(futureEntries.items()):
      entry = cls(_root=True)
      entry.__member_name__ = name
      entry.__member_value__ = value
      entry.__member_index__ = i
      memberValues.append(value)
      memberNames.append(name)
      actualEntries[name] = entry
      setattr(cls, name, entry)
      if name != name.upper():
        setattr(cls, name.upper(), entry)

    cls._validate(**actualEntries)

    setattr(cls, '__value_type__', valueType)
    setattr(cls, '__member_entries__', actualEntries)
    delattr(cls, '__future_entries__')
    delattr(cls, '__future_value_type__')

  def __call__(cls, *args, **kwargs) -> Any:
    """
    Only the _addMember method is allowed to create instances of the
    KeeNum class.
    """
    if not kwargs.get('_root', False):
      raise IllegalInstantiation(cls)
    self = super().__call__(**kwargs)
    return self

  def __len__(cls) -> int:
    """
    Get the number of members in the KeeNum class.
    """
    out = 0
    for _ in cls:
      out += 1
    else:
      return out

  def __iter__(cls, ) -> Iterator:
    """
    Iterate over the members of the KeeNum class.
    """
    yield from getattr(cls, '__member_entries__', ).values()

  def __getitem__(cls, key: str) -> Any:
    """
    Get a member by its name.
    """
    valueType = getattr(cls, '__value_type__', None)
    if valueType is int and isinstance(key, int):
      try:
        out = cls._getFromValue(key)
      except ValueError as valueError:
        try:
          out = cls._getFromIndex(key)
        except IndexError as indexError:
          raise indexError from valueError
        else:
          return out
      else:
        return out
    if valueType is str and isinstance(key, str):
      try:
        out = cls._getFromValue(key)
      except ValueError as valueError:
        try:
          out = cls._getFromName(key)
        except KeyError as keyError:
          raise keyError from valueError
        else:
          return out
      else:
        return out
    if isinstance(key, int):
      return cls._getFromIndex(key)
    if isinstance(key, str):
      return cls._getFromName(key)
    try:
      out = cls._getFromValue(key)
    except ValueError as valueError:
      raise KeyError(key) from valueError
    else:
      return out

  def _getFromIndex(cls, index: int) -> Any:
    """
    Get a member by its index. If the value type is 'int' and the index is
    negative, this method assumes that the index does not match any value
    type.
    """
    if index < 0:
      return cls._getFromIndex(len(cls) + index)
    if index >= len(cls):
      raise IndexError(f'Index {index} out of range for {cls.__name__}')
    for entry in cls:
      if entry.index == index:
        return entry
    raise IndexError(f'No member with index {index} in {cls.__name__}')

  def _getFromName(cls, name: str, **kwargs) -> Any:
    """
    Get a member by its name. If the value type is 'str', this method
    assumes that the identifier does not match any value type.
    """
    if not isinstance(name, str):
      raise TypeException('name', name, str)
    for entry in cls:
      if entry.name == name:
        return entry
    targetNames = [
        name,
        name.lower(),
        name.upper(),
    ]
    for entry in cls:
      entryNames = [
          entry.name,
          entry.name.lower(),
          entry.name.upper(),
      ]
      for i, j in zip(targetNames, entryNames):
        if i == j:
          return entry
    raise KeyError(name)

  def _getFromValue(cls, value: Any, **kwargs) -> Any:
    """
    Get a member by its value.
    """
    for entry in cls:
      if entry.value == value:
        return entry
    raise ValueError(value)

  def __str__(cls) -> str:
    """
    String representation of the KeeMeta metaclass.
    """
    if cls.__name__ == 'KeeNum':
      return object.__str__(cls)
    valueType = getattr(cls, '__value_type__', )
    typeName = '' if valueType is str else valueType.__name__
    clsName = cls.__name__
    if valueType is str:
      infoSpec = """%s%s(KeeNum)"""
    else:
      infoSpec = """%s(KeeNum)[%s]"""
    return infoSpec % (clsName, typeName)

  def __repr__(cls) -> str:
    """
    Representation of the KeeMeta metaclass.
    """
    return object.__repr__(cls)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _validateStrValues(**entries) -> None:
    """
    Validates that exactly one of the two following conditions is satisfied:
    1. Every name is the same as the member value
    2. No name is the name of a member value
    """
    memberValueNames = []
    for name, value in entries.items():
      if not isinstance(name, str):
        raise TypeException('name', name, str)
      memberValueNames.append(value)
      memberValueNames.append(value.lower())
      memberValueNames.append(value.upper())
    for name, value in entries.items():
      if name not in memberValueNames:
        break
    else:  # Means 'break' was never hit
      return
    for name, value in entries.items():
      if name in memberValueNames:
        break
    else:  # Means 'break' was never hit
      return
    raise NotImplementedError('name inconsistency: %s' % name)

  @staticmethod
  def _validateIntValues(**entries) -> None:
    """
    Validates that not value would match the index of a member or be
    negative.
    """
    for name, value in entries.items():
      if not isinstance(value, int):
        raise TypeException('value', value, int)
      if value < 0:
        raise ValueError('Negative values are not allowed: %s' % value)
      if value < len(entries):
        break
    else:  # Means 'break' was never hit
      return
    raise NotImplementedError('value inconsistency: %s' % value)

  @staticmethod
  def _validateValues(**entries) -> None:
    """
    Validates type consistency of the values in the entries. Please note
    that this method does not apply to validation of types 'int' and
    'str'. For those cases, use the methods '_validateIntValues' and
    '_validateStrValues' respectively.
    """
    valueType = None
    for name, value in entries.items():
      if valueType is None:
        valueType = type(value)
        continue
      if not isinstance(value, valueType):
        break
    else:  # Means 'break' was never hit
      return
    raise TypeException('value', value, valueType)

  @staticmethod
  def _validate(**entries) -> None:
    """
    Dispatches entries to the appropriate validation method based on
    the type of the values.
    """
    if not entries:
      return
    valueType = None
    for name, value in entries.items():
      valueType = type(value)
      break
    if valueType is str:
      KeeMeta._validateStrValues(**entries)
