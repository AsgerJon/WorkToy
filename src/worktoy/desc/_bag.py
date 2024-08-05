"""Bag wraps the field object managed by an instance of AttriBox"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from worktoy.meta import BaseObject
from worktoy.text import typeMsg


class Bag(BaseObject):
  """Bag wraps the field object managed by an instance of AttriBox"""

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
