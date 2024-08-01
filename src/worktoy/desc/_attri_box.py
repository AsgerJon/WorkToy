"""AttriBox class improves the AttriBox class!"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Self

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
    return """__%s__""" % (''.join(chars),)

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Getter-function which instantiates the field object only when
    called for the first time and only if the instance is not missing."""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self._createFieldObject(instance))
      return self.__get__(instance, owner, _recursion=True)
    bag = getattr(instance, pvtName)
    if not isinstance(bag, _Bag):
      e = typeMsg('bag', bag, _Bag)
      raise TypeError(e)
    innerObject = bag.getInnerObject()
    if innerObject is None:
      e = """The inner object of the AttriBox instance is missing!"""
      raise AttributeError(e)
    fieldClass = self.getFieldClass()
    if isinstance(innerObject, fieldClass):
      self.notifyGet(instance, innerObject)
      return innerObject
    e = typeMsg('innerObject', innerObject, fieldClass)
    raise TypeError(e)

  def __set__(self, instance: object, newValue: object) -> None:
    """Setter-function which raises an error."""
    pvtName = self._getPrivateName()
    bag = getattr(instance, pvtName, None)
    if bag is None:
      bag = _Bag(instance, newValue)
      self.notifySet(instance, None, newValue)
      return setattr(instance, pvtName, bag)
    if isinstance(bag, _Bag):
      oldValue = bag.getInnerObject()
      self.notifySet(instance, oldValue, newValue)
      return bag.setInnerObject(newValue)
    e = typeMsg('bag', bag, _Bag)
    raise TypeError(e)

  def __delete__(self, instance: object = None) -> None:
    """Deleter-function is not implemented by the AttriBox class. """
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      return self.notifyDel(instance, None)
    oldValue = getattr(instance, pvtName, )
    self.notifyDel(instance, oldValue)
    delattr(instance, pvtName)
