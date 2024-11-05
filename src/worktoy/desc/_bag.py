"""Bag wraps the field object managed by an instance of AttriBox"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from worktoy.meta import BaseMetaclass
from worktoy.parse import typeCast
from worktoy.text import typeMsg


# noinspection PyMissingConstructor
class Bag(metaclass=BaseMetaclass):
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
    else:
      self.__inner_object__ = typeCast(innerObject, self.getInnerClass())

  def getInnerClass(self) -> type:
    """Getter-function for the inner class. """
    if self.__inner_class__ is None:
      e = """The inner object has not been set!"""
      raise AttributeError(e)
    if isinstance(self.__inner_class__, type):
      return self.__inner_class__
    e = typeMsg('innerClass', self.__inner_class__, type)
    raise TypeError(e)

  def getOwningClass(self) -> type:
    """Getter-function for the owning class. """
    return self.__owning_class__
