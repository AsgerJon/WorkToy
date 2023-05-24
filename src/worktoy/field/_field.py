"""FieldTest. PyCharm refuses to apply formatting to non-project files and
I don't have an hour to spend fixing that, so now it's added."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from enum import IntEnum
from typing import Any, Never

from icecream import ic

from worktoy.core import searchKeys, maybeType, maybe, maybeTypes
from worktoy.core import CallMeMaybe
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError, ExceptionCore

ic.configureOutput(includeContext=True)


class NameFormat(IntEnum):
  """For a variable, the name can take different styles:"""
  NAME = 0
  CAPNAME = 1
  DASHNAME = 2
  ALTNAME = 3


class Field:
  """FieldTest. PyCharm refuses to apply formatting to non-project files and
  I don't have an hour to spend fixing that, so now it's added.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  @staticmethod
  def _proceduralError(varName: str = None) -> Never:
    """Raises the procedural error. Temporary implementation, replace with
    dedicated ExceptionCore instance"""
    name = maybe(varName, 'unnamed')
    raise ExceptionCore('Variable "%s" not ready!' % name)

  def __init__(self, *args, **kwargs) -> None:
    nameKwarg = searchKeys('fieldName', 'name') @ str >> kwargs
    nameArg = maybeType(str, *args)
    nameDefault = None
    self._fieldName = maybe(nameKwarg, nameArg, nameDefault)
    if self._fieldName is None:
      self._proceduralError('_fieldName')
    typeKwarg = searchKeys('type', 'class', 'type_') @ type >> kwargs
    typeArg = maybeType(type, *args)
    typeDefault = None
    type_ = maybe(typeKwarg, typeArg, typeDefault, )
    defValKwarg = searchKeys('default', 'defVal') @ type_ >> kwargs
    defValArg = None
    if type_ is not None:
      defValArg = maybeType(type_, *args)
    defValDefault = None
    defVal = maybe(defValKwarg, defValArg, defValDefault)
    if defVal is None and type_ is None:
      self._proceduralError('_fieldName')
    type_ = maybe(type_, type(defVal))
    self._fieldDefault = defVal
    self._fieldType = type_
    getterKeys = stringList('getter allowGetter get allowGet', ' ')
    setterKeys = stringList('setter allowSetter set allowSet', ' ')
    deleterKeys = stringList('deleter allowDel del allowDel', ' ')
    allowGetterKwarg = searchKeys(*getterKeys) @ bool >> kwargs
    allowSetterKwarg = searchKeys(*setterKeys) @ bool >> kwargs
    allowDelKwarg = searchKeys(*deleterKeys) @ bool >> kwargs
    boolArgs = maybeTypes(bool, *args, padLen=3, padChar=None)
    allowGetterArg, allowSetterArg, allowDelArg = boolArgs
    allowGetterDefault = True
    allowSetterDefault = True
    allowDelDefault = False
    allowGetter = maybe(allowGetterKwarg, allowGetterArg, allowGetterDefault)
    allowSetter = maybe(allowSetterKwarg, allowSetterArg, allowSetterDefault)
    allowDel = maybe(allowDelKwarg, allowDelArg, allowDelDefault)
    self._allowGetter = allowGetter
    self._allowSetter = allowSetter
    self._allowDel = allowDel
    self._useLegacyGetter = kwargs.get('legacyGetter', False)
    self._useLegacySetter = kwargs.get('legacySetter', False)
    self._useLegacyDeleter = kwargs.get('legacyDeleter', False)

  def _getFieldName(self, which: NameFormat = None) -> str:
    """Getter-function for field name"""
    which = maybe(which, NameFormat.NAME)
    name = self._fieldName
    Name = '%s%s' % (name[0].upper(), name[1:])
    return [name, Name, '_%s' % name, '_%sAlt' % name][which]

  def _getFieldType(self) -> type:
    """Getter-function for field type"""
    return self._fieldType

  def _getFieldDefault(self, ) -> Any:
    """Getter-function for the default value"""
    return self._fieldDefault

  def getterFactory(self, ) -> CallMeMaybe:
    """Creates the getter-function"""

    def func(instance: Any) -> Any:
      """Getter-function"""
      dashName = self._getFieldName(NameFormat.DASHNAME)
      altName = self._getFieldName(NameFormat.ALTNAME)
      base = getattr(instance, dashName, )
      alt = getattr(instance, altName, lambda: None)
      return maybe(base, alt)

    func.__annotations__ = {'return': '%s' % self._getFieldType()}

    return func

  def setterFactory(self, ) -> CallMeMaybe:
    """Creates the setter-function"""

    def func(instance: Any, value: Any) -> Any:
      """Setter-function"""
      setattr(instance, self._getFieldName(NameFormat.DASHNAME), value)

    func.__annotations__ = {
      'value' : self._getFieldType(),
      'return': 'NoReturn'}

    return func

  def deleterFactory(self) -> CallMeMaybe:
    """Creates the deleter-function"""

    def func(instance: Any) -> Any:
      """Deleter-function"""
      setattr(instance, self._getFieldName(NameFormat.DASHNAME), None)

    func.__annotations__ = {'return': 'NoReturn'}

    return func

  def badGetterFactory(self) -> CallMeMaybe:
    """Creates bad getter-function which raises ReadOnlyError"""
    raise NotImplementedError

  def badSetterFactory(self, ) -> CallMeMaybe:
    """Creates bad setter-function which raises ReadOnlyError"""

    def func(_, *__) -> Never:
      """Illegal setter function"""
      raise ReadOnlyError(self._getFieldName(NameFormat.NAME))

    func.__annotations__ = {'return': 'Never'}

    return func

  def badDeleterFactory(self) -> CallMeMaybe:
    """Creates bad deleter function which raises ReadOnlyError"""

    def func(_, ) -> Never:
      """Illegal deleter function"""
      raise ReadOnlyError(self._getFieldName(NameFormat.NAME))

    func.__annotations__ = {'return': 'Never'}

    return func

  def _fieldCollectorFactory(self) -> CallMeMaybe:
    """Creates a function on the target class which creates a dictionary
    with key-value pairs given by 'field.name' and 'field.value' at moment
    the function is called. This logic is crucial for save and loading
    files."""
    raise NotImplementedError

  def __call__(self, cls: type) -> Any:
    """Applies to class"""

    name = self._getFieldName(NameFormat.NAME)
    _name = self._getFieldName(NameFormat.DASHNAME)
    Name = self._getFieldName(NameFormat.CAPNAME)
    altName = self._getFieldName(NameFormat.ALTNAME)
    type_ = self._getFieldType()

    setattr(cls, _name, self._fieldDefault)
    setattr(cls, altName, lambda: None)
    altDict = getattr(cls, '__altNames__', None)
    if altDict is None:
      setattr(cls, '__altNames__', {})
      altDict = getattr(cls, '__altNames__', None)
    altDict |= {name: {'altName': altName, 'type': type_}}
    setattr(cls, '__altNames__', altDict)
    getterName = '_get%s' % Name
    setterName = '_set%s' % Name
    deleterName = '_del%s' % Name

    legacyGetterName = '%sLegacy' % getterName
    legacySetterName = '%sLegacy' % setterName
    legacyDeleterName = '%sLegacy' % deleterName

    legacyGetter = getattr(cls, getterName, None)
    legacySetter = getattr(cls, setterName, None)
    legacyDeleter = getattr(cls, deleterName, None)
    goodGetter = self.getterFactory()
    goodSetter = self.setterFactory()
    goodDeleter = self.deleterFactory()
    badGetter = self.badGetterFactory()
    badSetter = self.badSetterFactory()
    badDeleter = self.badDeleterFactory()

    setattr(cls, legacyGetterName, legacyGetter)
    setattr(cls, legacySetterName, legacySetter)
    setattr(cls, legacyDeleterName, legacyDeleter)

    if self._useLegacyGetter:
      getterFunc = legacyGetter
    elif self._allowGetter:
      getterFunc = goodGetter
    else:
      getterFunc = badGetter

    if self._useLegacySetter:
      setterFunc = legacySetter
    elif self._allowSetter:
      setterFunc = goodSetter
    else:
      setterFunc = badSetter

    if self._useLegacyDeleter:
      deleterFunc = legacyDeleter
    elif self._allowSetter:
      deleterFunc = goodDeleter
    else:
      deleterFunc = badDeleter

    setattr(cls, getterName, getterFunc)
    setattr(cls, setterName, setterFunc)
    setattr(cls, deleterName, deleterFunc)
    setattr(cls, name, property(getterFunc, setterFunc, deleterFunc))

    return cls
