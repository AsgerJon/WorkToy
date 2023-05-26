"""Field decorates classes with named properties right in the decorator"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import Any, Never, NoReturn

from worktoy.core import searchKeys, maybe, CallMeMaybe
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError
from worktoy.field import Perm, NameF, Accessor


class Field:
  """Field decorates classes with named properties right in the decorator
  :param name: name of the property representing the field
  :param defVal: default value on the field
  :param type_: type of the value on the field
  :param perm: permission profile
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  _decorations = []

  @classmethod
  def _getDecorations(cls, ) -> list[CallMeMaybe]:
    """Getter-function for list of decorating functions of this class"""
    return cls._decorations

  @staticmethod
  def parseArguments(*args, **kwargs) -> list:
    """Parses arguments"""
    args = [*args, *[None] * 4]
    nameArg = args[0]
    typeArg = args[1]
    defValArg = args[2]
    permArg = args[3]
    nameKeys = stringList('name, varName, id, fieldName')
    typeKeys = stringList('type, type_, class, class_')
    defValKeys = stringList('default, defVal, defValue, defaultValue')
    permKeys = stringList('perm, permission, permProfile, permissionProfile')
    nameKwarg = searchKeys(*nameKeys) @ str >> kwargs
    typeKwarg = searchKeys(*typeKeys) @ type >> kwargs
    defValKwarg = searchKeys(*defValKeys) >> kwargs
    permKwarg = searchKeys(*permKeys) @ Perm >> kwargs
    nameDefault = None
    typeDefault = None
    defValDefault = None
    permDefault = Perm.READSET
    name = maybe(nameArg, nameKwarg, nameDefault)
    type_ = maybe(typeArg, typeKwarg, typeDefault)
    defVal = maybe(defValArg, defValKwarg, defValDefault)
    perm = maybe(permArg, permKwarg, permDefault)
    return [name, type_, defVal, perm]

  def __init__(self, *args, **kwargs) -> None:
    parsed = self.parseArguments(*args, **kwargs)
    self._permissionProfile = parsed.pop()
    self._fieldDefault = parsed.pop()
    self._fieldType = parsed.pop()
    self._fieldName = parsed.pop()
    self._targetClass = None

  def _applyGetter(self, cls: type) -> type:
    """Applies the getter function"""
    name, type_ = self._fieldName, self._fieldType
    getterKey = Accessor.READ.functionName(name)
    privateKey = NameF.privateVariableName(name)
    setattr(cls, privateKey, self._fieldDefault)

    def allowGetter(instance: Any) -> Any:
      """Getter-function"""
      return getattr(instance, privateKey, )

    allowGetter.__annotations__ = {'return': '%s' % self._fieldType}
    allowGetter.__doc__ = Accessor.READ.allowDoc(name, type_, cls)

    def denyGetter(_: Any, ) -> Never:
      """Illegal getter function"""
      raise ReadOnlyError(privateKey)

    denyGetter.__annotations__ = {'return': 'Never'}
    denyGetter.__doc__ = Accessor.READ.denyDoc()
    if self._permissionProfile > 0:
      setattr(cls, getterKey, allowGetter)
    else:
      setattr(cls, getterKey, denyGetter)
    return cls

  def _applySetter(self, cls: type) -> type:
    """Applies setter function"""
    name, type_ = self._fieldName, self._fieldType
    setterKey = Accessor.SET.functionName(name)
    privateKey = NameF.dash(name)

    def allowSetter(instance: Any, value: Any) -> NoReturn:
      """Setter-function"""
      setattr(instance, privateKey, value)

    allowSetter.__annotations__ = {
      'value' : self._fieldType,
      'return': 'NoReturn'
    }
    allowSetter.__doc__ = Accessor.SET.allowDoc(name, type_, cls)

    def denySetter(__: Any, *_) -> Never:
      """Illegal setter function"""
      raise ReadOnlyError(privateKey)

    denySetter.__annotations__ = {'return': 'Never'}
    denySetter.__doc__ = Accessor.SET.denyDoc()
    if self._permissionProfile > 1:
      setattr(cls, setterKey, allowSetter)
    else:
      setattr(cls, setterKey, denySetter)
    return cls

  def _applyDeleter(self, cls: type) -> type:
    """Applies deleter function"""
    name, type_ = self._fieldName, self._fieldType
    deleterKey = Accessor.DEL.functionName(self._fieldName)
    privateKey = NameF.dash(self._fieldName)

    def allowDeleter(instance: Any, ) -> NoReturn:
      """Setter-function"""
      delattr(instance, privateKey, )

    allowDeleter.__annotations__ = {'return': 'NoReturn'}
    allowDeleter.__doc__ = Accessor.DEL.allowDoc(name, type_, cls)

    def denyDeleter(_: Any, ) -> Never:
      """Illegal deleter function"""
      raise ReadOnlyError(privateKey)

    denyDeleter.__annotations__ = {'return': 'Never'}
    denyDeleter.__doc__ = Accessor.DEL.denyDoc()

    if self._permissionProfile > 2:
      setattr(cls, deleterKey, allowDeleter)
    else:
      setattr(cls, deleterKey, denyDeleter)
    return cls

  def _applyProperty(self, cls: type) -> type:
    """Applies the property. This function should be invoked the others"""
    name = self._fieldName
    getFunction = getattr(cls, Accessor.READ.functionName(name))
    setFunction = getattr(cls, Accessor.SET.functionName(name))
    delFunction = getattr(cls, Accessor.DEL.functionName(name))
    setattr(cls, name, property(getFunction, setFunction, delFunction))
    return cls

  def __call__(self, cls: type) -> type:
    """When calling an instance on a cls, it returns a decorated version."""
    self._targetClass = cls
    cls = self._applyGetter(cls)
    cls = self._applySetter(cls)
    cls = self._applyDeleter(cls)
    cls = self._applyProperty(cls)
    return cls

  def __str__(self) -> str:
    """String Representation"""
    out = """Field named %s on class %s. Current value: %s"""
    name = self._fieldName
    className = self._targetClass.__name__
    value = getattr(self._targetClass, NameF.privateVariableName(name))
    return out % (name, className, value)
