"""Documentation: Field"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, Never, Any

from worktoy import maybe, Kwargs, Value, Args, searchKeys, maybeType
from worktoy import CallMeMaybe
from worktoy.sharperexceptions import ReadOnlyError


class Field:
  """Instances of field are semantic. They have no effect except they are
  inside a subclass of WorkToy"""

  _SLOTS = []

  @staticmethod
  def _typeJsonToValue(json_: str, type_: type) -> Any:
    """Loads json strings to values"""
    if type_ is str:
      return json_
    json_ = json_.replace(' ', '')
    while json_[0] == '0':
      json_ = json_[1:]
    if not json_.isnumeric():
      raise ValueError('Found non numeric entries when parsing numeric!')
    return float(json_)

  @staticmethod
  def _typeValueToJson(value: Any, type_: type) -> str:
    """Converts value to json string"""
    if type_ in [str, int, float]:
      return '%s' % value

  @classmethod
  def clearSlots(cls) -> NoReturn:
    """Clears the slots"""
    while cls._SLOTS:
      cls._SLOTS.pop()

  @classmethod
  def _getSlots(cls) -> list[CallMeMaybe]:
    """Getter-function for the slots"""
    return cls._SLOTS

  @classmethod
  def _notifySlots(cls, field: Field) -> NoReturn:
    """Notifies all slots in _SLOTS on creation of new instance"""
    for s in cls._getSlots():
      s(field)

  @classmethod
  def onFieldCreation(cls, s: CallMeMaybe) -> NoReturn:
    """Appends s to the list of slots to notify"""
    cls._getSlots().append(s)

  @staticmethod
  def _parseDefaultTypeless(*args, **kwargs) -> Value:
    """Parses arguments to default value without a given type. The type is
    then inferred from the default value found. """
    defValKwarg = searchKeys('default', 'defVal', 'val0') >> kwargs
    defValArg = None
    if args:
      defValArg = args[0]
    defValDefault = None
    defVal = maybe(defValKwarg, defValArg, defValDefault)
    outArgs = [arg for arg in args if arg != defVal]
    outKwargs = {}
    for (key, val) in kwargs.items():
      outKwargs |= {key: val}
    return (defVal, outArgs, outKwargs)

  @staticmethod
  def _parseDefault(type_: type, *args: Args, **kwargs: Kwargs) -> Value:
    """General parsing method"""
    if type_ is type:
      raise TypeError('This method finds default values that are not types')
    defaultKwarg = searchKeys('default', 'defVal', 'val0') @ type_ >> kwargs
    defaultArg = maybeType(type_, *args)
    defaultDefault = None
    defVal = maybe(defaultKwarg, defaultArg, defaultDefault)
    outArgs = [arg for arg in args if arg != defVal]
    outKwargs = {}
    for (key, val) in kwargs.items():
      outKwargs |= {key: val}
    return (defVal, outArgs, outKwargs)

  @staticmethod
  def _parseDefaultType(*args, **kwargs) -> Value:
    """Parses arguments to find the default value that is a type. This
    method should be used if the field type is type. """
    defaultKwarg = searchKeys('default', 'defVal', 'val0') @ type >> kwargs
    defaultArg = maybeType(type, *[arg for arg in args if arg is not type])
    defaultDefault = None
    defVal = maybe(defaultKwarg, defaultArg, defaultDefault)
    outArgs = [arg for arg in args if arg != defVal]
    outKwargs = {}
    for (key, val) in kwargs.items():
      outKwargs |= {key: val}
    return (defVal, outArgs, outKwargs)

  @staticmethod
  def _parseName(*args, **kwargs) -> Value:
    """Parses the arguments to find the name and returns it along with
    unused arguments"""
    nameKwarg = searchKeys('name', 'field') @ str >> kwargs
    nameArg = maybeType(str, *args)
    nameDefault = None
    name = maybe(nameKwarg, nameArg, nameDefault)
    if name is None:
      raise TypeError('Failed to parse name!')
    outArgs = [arg for arg in args if arg != name]
    outKwargs = {}
    for (key, val) in kwargs.items():
      if val != name:
        outKwargs |= {key: val}
    return (name, outArgs, outKwargs)

  @staticmethod
  def _parseType(*args, **kwargs) -> Value:
    """Parses arguments to type"""
    outKwargs = {}
    for (key, val) in kwargs.items():
      outKwargs |= {key: val}
    if type in args:
      outArgs = [arg for arg in args if arg != type]
      return (type, outArgs, outKwargs)
    typeKwarg = searchKeys('type', 'type_', '_type') @ type >> kwargs
    typeArg = maybeType(type, *args)
    typeDefault = None
    type_ = maybe(typeKwarg, typeArg, typeDefault)
    outArgs = [arg for arg in args if arg != type]
    return (type_, outArgs, outKwargs)

  def __init__(self, *args, **kwargs) -> None:
    self._name, args, kwargs = self._parseName(*args, **kwargs)
    self._type, args, kwargs = self._parseType(*args, **kwargs)
    if self._type is type:
      self._defVal, args, kwargs = self._parseDefaultType(*args, **kwargs)
    elif isinstance(self._type, type):
      self._defVal, args, kwargs = self._parseDefault(
        self._type, *args, **kwargs)
    elif self._type is None:
      self._defVal = self._parseDefaultTypeless(*args, **kwargs)
      self._type = type(self._defVal)
    if self._type is None:
      e = """The type should be a type or None, but found: %s"""
      raise TypeError(e % type(self._type))
    Field._notifySlots(self)
    self._val = self._defVal

  def __str__(self) -> str:
    """String representation"""
    out = """Field named %s of type %s having default value: %s"""
    return out % (self.name, self.type_, self.defVal)

  def _asJson(self) -> str:
    """Value to json"""
    if self.type_ in [str, int, float]:
      return self._typeValueToJson(self.value, self.type_)
    func = self.type_.__dict__.get('asJson', None)
    if func is None:
      raise TypeError('Field type could not be cast as Json!')
    return func(self.value)

  def _fromJson(self, json_: str) -> NoReturn:
    """Json to value"""
    if self.type_ in [str, int, float]:
      self.value = self._typeJsonToValue(json_, self.type_)
    else:
      func = self.type_.__dict__.get('asJson', None)
      if func is None:
        raise TypeError('Field type could not be cast as Json!')
      self.value = func(json_)

  def _getVal(self) -> str:
    """Getter-function for the name attribute"""
    return self._val

  def _setVal(self, value: str) -> NoReturn:
    """Setter-function for the name attribute"""
    self._val = value

  def _delVal(self) -> Never:
    """Deleter-function for the name attribute"""
    raise TypeError("Attribute 'name' is read-only")

  def _getName(self) -> str:
    """Getter-function for the name attribute"""
    return self._name

  def _setName(self, value: str) -> Never:
    """Setter-function for the name attribute"""
    raise ReadOnlyError('name')

  def _delName(self) -> Never:
    """Deleter-function for the name attribute"""
    raise ReadOnlyError('name')

  def _getType(self) -> type:
    """Getter-function for the type_ attribute"""
    return self._type

  def _setType(self, value: type) -> Never:
    """Setter-function for the type_ attribute"""
    raise ReadOnlyError('type_')

  def _delType(self) -> Never:
    """Deleter-function for the type_ attribute"""
    raise ReadOnlyError('type_')

  def _getDefVal(self) -> Any:
    """Getter-function for the defVal attribute"""
    return self._defVal

  def _setDefVal(self, value: type_) -> Never:
    """Setter-function for the defVal attribute"""
    raise ReadOnlyError('defVal')

  def _delDefVal(self) -> Never:
    """Deleter-function for the defVal attribute"""
    raise ReadOnlyError('defVal')

  def _getJson(self) -> str:
    """Getter-function for the json string representation. Unless the type
    is primitive, the field instance must have defined a method directly.
    For custom classes used on fields, those classes should define methods
    for converting to and from json. """
    return self._asJson()

  def _setJson(self, json_: str) -> NoReturn:
    """Setter-function for json string representation. """
    self.value = self._fromJson(json_)

  def _delJson(self) -> Never:
    """Deleter-function for the JSON attribute"""
    raise ReadOnlyError('JSON')

  name = property(_getName, _setName, _delName)
  defVal = property(_getDefVal, _setDefVal, _delDefVal)
  type_ = property(_getType, _setType, _delType)
  value = property(_getVal, _setVal, _delVal)
  JSON = property(_getJson, _setJson, _delJson)
