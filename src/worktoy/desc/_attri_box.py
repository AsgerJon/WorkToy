"""AttriBox class improves the AttriBox class!"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Self, Never

from worktoy.desc import AbstractDescriptor
from worktoy.parse import maybe
from worktoy.text import typeMsg, monoSpace


class _Bag:
  """This private class wraps the field object. """

  __owning_instance__ = None
  __owning_class__ = None
  __inner_object__ = None
  __inner_class__ = None

  def __init__(self, owningInstance: object, innerObject: object) -> None:
    self.setOwningInstance(owningInstance)
    self.setInnerObject(innerObject)

  def getOwningInstance(self) -> object:
    """Getter-function for the owning instance. """
    return self.__owning_instance__

  def setOwningInstance(self, owningInstance: object) -> None:
    """Setter-function for the owning instance. """
    if self.__owning_instance__ is not None:
      if self.__owning_instance__ is owningInstance:
        return
      e = """The owning instance has already been assigned!"""
      raise AttributeError(e)
    self.__owning_instance__ = owningInstance
    self.__owning_class__ = type(owningInstance)

  def getInnerObject(self) -> object:
    """Getter-function for the inner object. """
    return self.__inner_object__

  def setInnerObject(self, innerObject: object) -> None:
    """Setter-function for the inner object. """
    if self.__inner_class__ is None:
      self.__inner_object__ = innerObject
      self.__inner_class__ = type(innerObject)
    elif isinstance(innerObject, self.getInnerClass()):
      self.__inner_object__ = innerObject
    else:
      if self.getInnerClass() is complex:
        if isinstance(innerObject, (int, float)):
          return self.setInnerObject(complex(innerObject))
      if self.getInnerClass() is float and isinstance(innerObject, int):
        return self.setInnerObject(float(innerObject))
      if self.getInnerClass() is int and isinstance(innerObject, float):
        if innerObject.is_integer():
          return self.setInnerObject(int(innerObject))
      e = typeMsg('innerObject', innerObject, self.getInnerClass())
      raise TypeError(e)

  def getInnerClass(self) -> type:
    """Getter-function for the inner class. """
    return self.__inner_class__

  def getOwningClass(self) -> type:
    """Getter-function for the owning class. """
    return self.__owning_class__


class AttriBox(AbstractDescriptor):
  """AttriBox class improves the AttriBox class!"""

  __field_class__ = None
  __pos_args__ = None
  __key_args__ = None

  @classmethod
  def __class_getitem__(cls, fieldClass: type) -> AttriBox:
    """Class method for creating a AttriBox instance."""
    return cls(fieldClass)

  def __init__(self, *args) -> None:
    AbstractDescriptor.__init__(self)
    for arg in args:
      if isinstance(arg, type):
        fieldClass = arg
        break
    else:
      e = """AttriBox constructor requires the fieldClass type!"""
      raise ValueError(e)
    if isinstance(fieldClass, type):
      self.__field_class__ = fieldClass
    else:
      e = """AttriBox constructor requires the fieldClass type!"""
      e2 = typeMsg('fieldClass', fieldClass, type)
      raise TypeError(monoSpace('%s\n%s' % (e, e2)))
    self.__field_class__ = fieldClass

  def __call__(self, *args, **kwargs) -> Self:
    self.__pos_args__ = [*args, ]
    self.__key_args__ = {**kwargs, }
    return self

  def getFieldClass(self, ) -> type:
    """Getter-function for the field class."""
    if self.__field_class__ is None:
      e = """The field class of the AttriBox instance has not been set!"""
      raise AttributeError(e)
    if isinstance(self.__field_class__, type):
      return self.__field_class__
    e = typeMsg('__field_class__', self.__field_class__, type)
    raise TypeError(e)

  def getArgs(self, ) -> list[Any]:
    """Getter-function for positional arguments"""
    return maybe(self.__pos_args__, [])

  def getKwargs(self, ) -> dict[str, Any]:
    """Getter-function for keyword arguments"""
    return maybe(self.__key_args__, {})

  def _createFieldObject(self, instance: object) -> _Bag:
    """Create the field object."""
    if self.__field_class__ is None:
      e = """AttriBox instance has not been initialized!"""
      raise AttributeError(e)
    if self.__pos_args__ is None or self.__key_args__ is None:
      e = """AttriBox instance has not been called!"""
      raise AttributeError(e)
    args, kwargs = self.getArgs(), self.getKwargs()
    fieldClass = self.getFieldClass()
    innerObject = fieldClass(*args, **kwargs)
    return _Bag(instance, innerObject)

  def _getPrivateName(self, ) -> str:
    """Returns the name of the private attribute used to store the inner
    object. """
    if self.getFieldName() is None:
      e = """Instance of 'AttriBox' does not belong to class. This 
      typically indicates that the owning class is still being created."""
      raise RuntimeError(monoSpace(e))
    chars = []
    for (i, char) in enumerate(self.__field_name__):
      if char.isupper() and i and i < len(self.__field_name__):
        chars.append('_')
      chars.append(char.lower())
    innerName = ''.join(chars)
    innerNames = innerName.split('_')
    if len(innerNames) == 1:
      innerNames.append('value')
    innerName = '_'.join(innerNames)
    return """__%s__""" % (innerName,)

  def __instance_get__(self, instance: object, **kwargs) -> Any:
    """Getter-function for the instance."""
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self._createFieldObject(instance))
      return self.__instance_get__(instance, _recursion=True)
    bag = getattr(instance, pvtName)
    if not isinstance(bag, _Bag):
      e = typeMsg('bag', bag, _Bag)
      raise TypeError(e)
    innerObject = bag.getInnerObject()
    if innerObject is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self._createFieldObject(instance))
      return self.__instance_get__(instance, _recursion=True)
    fieldClass = self.getFieldClass()
    if isinstance(innerObject, fieldClass):
      return innerObject
    e = typeMsg('innerObject', innerObject, fieldClass)
    raise TypeError(e)

  def __instance_set__(self, instance: object, value: object) -> None:
    """Setter-function for the instance."""
    pvtName = self._getPrivateName()
    bag = getattr(instance, pvtName, None)
    if bag is None:
      bag = self._createFieldObject(instance)
      bag.setInnerObject(value)
      return setattr(instance, pvtName, bag)
    if isinstance(bag, _Bag):
      return bag.setInnerObject(value)
    e = typeMsg('bag', bag, _Bag)
    raise TypeError(e)

  def __instance_del__(self, instance: object) -> Never:
    """Deleter-function for the instance."""
    e = """Deleter-function is not implemented by the AttriBox class."""
    raise TypeError(e)
