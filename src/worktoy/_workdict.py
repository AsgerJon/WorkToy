"""WorkDict implements dictionary like behaviour for use with custom
metaclass"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import inspect
from typing import NoReturn, Any, Callable, Never

from icecream import ic
from dis import dis

from worktoy import Field, CallMeMaybe, maybe

ic.configureOutput(includeContext=True)


class WorkDict(dict):
  """WorkDict implements dictionary like behaviour for use with custom
  metaclass.
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  _Overloaded = None

  @classmethod
  def _clearOverloaded(cls, ) -> NoReturn:
    """Clears the list of overloaded functions"""
    cls._Overloaded = None

  @classmethod
  def _createOverloaded(cls, ) -> NoReturn:
    """Creator-function for the list of functions marked for function
    overload."""
    cls._Overloaded = {}

  @classmethod
  def _getOverloaded(cls, ) -> dict[str, list[CallMeMaybe]]:
    """Getter-function for the list of functions marked for function
    overload"""
    if cls._Overloaded is None:
      cls._createOverloaded()
      return cls._getOverloaded()
    return cls._Overloaded

  @classmethod
  def _newOverloadName(cls, name: str) -> bool:
    """Creates an entry in the dictionary allowing for collection of
    overloads"""
    if cls._Overloaded is None:
      cls._createOverloaded()
      return cls._newOverloadName(name)
    if name in cls._Overloaded.keys():
      return True
    cls._Overloaded |= {name: []}
    return True if name in cls._Overloaded else False

  @classmethod
  def _checkName(cls, name: str = None) -> bool:
    """Checks if name is has function entries in the overloaded list"""
    if name is None or cls._Overloaded is None:
      return False
    return True if name in cls._Overloaded.keys() else False

  @classmethod
  def _validateName(cls, name: str = None) -> bool:
    """If the name does not appear in the overloaded dictionary, an entry
    is created. This method returns a boolean value indicating whether an
    entry in the overloaded dictionary matches the given name."""
    if cls._checkName(name):
      return True
    return cls._newOverloadName(name)

  @classmethod
  def _overloadName(cls, function: CallMeMaybe, name: str = None) -> bool:
    """Inserts given function at given name"""
    name = maybe(name, function.__name__, None)
    if name is None:
      raise TypeError('The name should not be NoneType')
    if cls._validateName(name):
      cls._getOverloaded().get(name, ).append(function)
      return True
    return True if function in cls._getOverloaded().get(name, ) else False

  @classmethod
  def applyOverload(cls, function: CallMeMaybe,
                    name: str = None) -> NoReturn:
    """Overloads the decorated function"""
    name = maybe(name, function.__name__, None)
    if name is None:
      raise TypeError('Function name missing')
    if cls._validateName(name):
      cls._overloadName(function, name)
    raise TypeError('The name should not be NoneType')

  @staticmethod
  def checkInit(init_func) -> CallMeMaybe:
    """Stops __init__ from running multiple times"""

    def wrapper(self, *args, **kwargs):
      if not getattr(self, '_initialized', False):
        init_func(self, *args, **kwargs)
        self._initialized = True

    return wrapper

  def __new__(cls, *args, **kwargs) -> WorkDict:
    """Implementation of new is necessary for builtins"""
    out = super().__new__(cls, *args, **kwargs)
    baseInit = WorkDict.__init__
    out.__init__ = WorkDict.checkInit(baseInit)
    WorkDict.__init__(out, **kwargs)
    out._initialized = True
    return out

  def __init__(self, **kwargs) -> None:
    Field.onFieldCreation(self._externalFieldSlot)
    self._fields = []
    self._backUp = []
    dict.__init__(self, **kwargs)

  def __setitem__(self, key: str, value: Any) -> NoReturn:
    """Setter-function for key"""
    if isinstance(value, Field):
      return self._appendField(value)
    dict.__setitem__(self, key, value)

  def __getitem__(self, key: str, ) -> Any:
    """Setter-function for key"""
    value = dict.__getitem__(self, key)
    return value

  def __delitem__(self, key: str) -> NoReturn:
    """Deleter-function for key"""
    self._backUp.append((key, self[key]))
    dict.__delitem__(self, key)

  def _externalFieldSlot(self, field: Field) -> NoReturn:
    """Invoked externally"""
    self._appendField(field)

  def _appendField(self, field: Field) -> NoReturn:
    """This method is invoked when encountering fields"""
    if field not in self._fields:
      self._fields.append(field)

  def _getFields(self) -> list[Field]:
    """Getter-function for the list of fields"""
    return self._fields

  def _setFields(self, *_) -> Never:
    """Illegal setter function"""
    raise TypeError('Read only variable')

  def _delFields(self, ) -> Never:
    """Illegal deleter function"""
    raise TypeError('Read only variable')

  fields = property(_getFields, _setFields, _delFields)
