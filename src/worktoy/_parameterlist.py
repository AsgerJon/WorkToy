"""ParameterDict specifies the parameters used by an overloaded functions.
Each key should match a certain """
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, Any, Never

from worktoy import WorkMeta, searchKeys, maybeType, maybe, monoSpace
from worktoy.sharperexceptions import ReadOnlyError, ArgumentError


class Parameter:
  """The Parameter class represents a parameter in an overloaded
  function. """

  def __init__(self, *args, **kwargs) -> None:
    self._keywords = []
    nameKwarg = searchKeys('name') @ str >> kwargs
    nameArg = maybeType(str, *args)
    nameDefault = getattr(self, '__name__', None)
    self._name = maybe(nameKwarg, nameArg, nameDefault)
    typeKwarg = searchKeys('type', 'type_') @ type >> kwargs
    typeArg = maybeType(type, *args)
    typeDefault = None
    self._type = maybe(typeKwarg, typeArg, typeDefault)
    defKwarg = searchKeys('defVal') >> kwargs
    if self._type is None and defKwarg is None:
      msg = """If type is not given, then default value must be given on a 
      keyword argument, but neither were found! If default is given, 
      type will be inferred from its type."""
      raise ArgumentError(self, monoSpace(msg))
    defArg = maybeType(self._type, *args)
    defDefault = None
    self._defVal = maybe(defKwarg, defArg, defDefault)
    self._type = maybe(self._type, type(self._defVal))
    self._typeMap = []

  def __bool__(self) -> bool:
    """A parameter having required values defined are truthy. If any are
    missing the parameter is falsy."""
    if not self.type_:
      return False
    if not self.defVal:
      return False

  def _appendKey(self, *keys: str) -> NoReturn:
    """Appends given key to list of keywords used by searchKeys"""
    for key in keys:
      self._keywords.append(key.lower())

  def _getKeys(self) -> list[str]:
    """Getter-function for the list of str"""
    return self._keywords

  def _setKeys(self, *_) -> Never:
    """Illegal setter-function"""

  def _delKeys(self) -> Never:
    """Illegal deleter-function"""

  def _getName(self) -> str:
    """Getter-function for the name"""
    return self._name

  def _setName(self, *_) -> Never:
    """Illegal setter-function"""
    raise ReadOnlyError('type')

  def _delName(self, ) -> Never:
    """Illegal deleter-function"""
    raise ReadOnlyError('type')

  def _getType(self) -> type:
    """Getter-function for type"""
    return self._type

  def _setType(self, *_) -> Never:
    """Illegal setter-function"""
    raise ReadOnlyError('type')

  def _delType(self, ) -> Never:
    """Illegal deleter-function"""
    raise ReadOnlyError('type')

  def _getDefVal(self) -> Any:
    """Getter-function for default value"""
    return self._defVal

  def _setDefVal(self, *_) -> Never:
    """Illegal setter-function"""
    raise ReadOnlyError('type')

  def _delDefVal(self, ) -> Never:
    """Illegal deleter-function"""
    raise ReadOnlyError('type')

  defVal = property(_getDefVal, _setDefVal, _delDefVal)
  name = property(_getName, _setName, _delName)
  type_ = property(_getType, _setType, _delType)
  keys = property(_getKeys, _setKeys, _delKeys)


class ParameterList(list, WorkMeta):
  """Parameter list organizes the parameters in a list"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

  def append(self, obj: Any) -> NoReturn:
    """Reimplements a typeguard on the append method"""
    if isinstance(obj, Parameter):
      return super().append(obj)
    msg = """The ParameterList supports only instances of Parameter!"""
    raise TypeError(msg)

  def _allKeys(self) -> list[str]:
    """Getter-function for all keys defined on any parameter"""
    out = []
    for p in self:
      out += [*[p.keys]]
    return out

  def validate(self) -> bool:
    """The validation procedure goes through the parameters and checks
    that they are all validly defined, and that no conflicts exist. A
    conflict would generally be namespace collisions.  """
    soft = [0, 0]
    for p in self:
      soft[0 if not p else 1] += 1
    keys = self._allKeys()
    while keys:
      key = keys.pop()
      if key in keys:
        msg = """Found key collision at key: %s""" % key
        KeyError(msg)
    print(soft)
    return True
