"""Field decorates classes with named properties right in the decorator"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import Any, Never, NoReturn

from worktoy.core import searchKeys, maybe, CallMeMaybe
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError
from worktoy.field import Perm, Name, Acc
from worktoy.field import FieldApply

applicator = FieldApply.applicator


class _FieldPropMixin:
  """Mixin class setting properties and static method parsing arguments"""

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

  def _getAllow(self) -> Any:
    """Getter-function for value"""
    return self._value

  def _setAllow(self, value: Any) -> NoReturn:
    """Setter-function for value"""
    self._value = value

  def _delAllow(self, ) -> Never:
    """Deleter-function"""
    self._value = None

  def _getDeny(self) -> Never:
    """Illegal getter-function"""
    raise ReadOnlyError(self._name)

  def _setDeny(self, *_) -> Never:
    """Illegal setter-function"""
    raise ReadOnlyError(self._name)

  def _delDeny(self, ) -> Never:
    """Illegal deleter-function"""
    raise ReadOnlyError(self._name)


class Field(_FieldPropMixin):
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

  def __init__(self, *args, **kwargs) -> None:
    parsed = self.parseArguments(*args, **kwargs)
    self._perms = parsed.pop()
    self._defVal = parsed.pop()
    self._type = parsed.pop()
    self._name = parsed.pop()
    self._target = None
    self._value = None

  def _applyGetter(self, cls: type) -> type:
    """Applies the getter function"""
    setattr(cls, Name.pvtName(self._name), self)
    self._getAllow.__annotations__ = {'return': '%s' % self._type}
    self._getAllow.__doc__ = Acc.READ.allowDoc(self._name, self._type, cls)
    self._getDeny.__annotations__ = {'return': 'Never'}
    self._getDeny.__doc__ = Acc.READ.denyDoc()
    _get = self._getAllow if self._perms > 0 else self._getDeny
    setattr(cls, Acc.READ.fName(self._name), _get)
    return cls

  def _applySetter(self, cls: type) -> type:
    """Applies setter function"""
    self._setAllow.__annotations__ = {
      'return': 'NoReturn', 'val': '%s' % self._type}
    self._setAllow.__doc__ = Acc.SET.allowDoc(self._name, self._type, cls)
    self._setDeny.__annotations__ = {'return': 'Never'}
    self._setDeny.__doc__ = Acc.SET.denyDoc()
    _set = self._setAllow if self._perms > 1 else self._setDeny
    setattr(cls, Acc.SET.fName(self._name), _set)
    return cls

  def _applyDeleter(self, cls: type) -> type:
    """Applies deleter function"""
    self._setAllow.__annotations__ = {'return': 'NoReturn'}
    self._setAllow.__doc__ = Acc.DEL.allowDoc(self._name, self._type, cls)
    self._setDeny.__annotations__ = {'return': 'Never'}
    self._setDeny.__doc__ = Acc.DEL.denyDoc()
    _del = self._setAllow if self._perms > 2 else self._delDeny
    setattr(cls, Acc.DEL.fName(self._name), _del)
    return cls

  def _applyProperty(self, cls: type) -> type:
    """Applies the property. This function should be invoked the others"""
    name = self._name
    getFunction = getattr(cls, Acc.READ.fName(name))
    setFunction = getattr(cls, Acc.SET.fName(name))
    delFunction = getattr(cls, Acc.DEL.fName(name))
    setattr(cls, name, property(getFunction, setFunction, delFunction))
    return cls

  def __call__(self, cls: type) -> type:
    """When calling an instance on a cls, it returns a decorated version."""
    self._target = cls
    cls = self._applyGetter(cls)
    cls = self._applySetter(cls)
    cls = self._applyDeleter(cls)
    cls = self._applyProperty(cls)
    return cls

  def __str__(self) -> str:
    """String Representation"""
    out = """Field named %s on class %s. Current value: %s"""
    name = self._name
    className = self._target.__name__
    value = getattr(self._target, Name.pvtName(name))
    return out % (name, className, value)
