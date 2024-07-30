"""BaseMetaclass provides general functionality for derived classes. This
includes primarily function overloading. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from worktoy.meta import AbstractMetaclass, Bases, BaseNamespace
from worktoy.text import monoSpace, typeMsg


class BaseMetaclass(AbstractMetaclass):
  """BaseMetaclass provides general functionality for derived classes. This
  includes primarily function overloading. """

  def __instancecheck__(cls, instance: object) -> bool:
    """The __instancecheck__ method is called when the 'isinstance' function
    is called."""
    if getattr(cls, '__class_instancecheck__', None) is None:
      return AbstractMetaclass.__instancecheck__(cls, instance)
    instanceCheck = getattr(cls, '__class_instancecheck__', )
    if not callable(instanceCheck):
      e = typeMsg('instanceCheck', instanceCheck, Callable)
      raise TypeError(monoSpace(e))
    if not isinstance(instanceCheck, classmethod):
      e = """The instanceCheck method must be a classmethod!"""
      e2 = typeMsg('instanceCheck', instanceCheck, classmethod)
      raise TypeError(monoSpace("""%s %s""" % (e, e2)))
    if getattr(instanceCheck, '__self__', None) is None:
      return instanceCheck(cls, instance)
    return instanceCheck(instance)

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> BaseNamespace:
    """The __prepare__ method is invoked before the class is created. This
    implementation ensures that the created class has access to the safe
    __init__ and __init_subclass__ through the BaseObject class in its
    method resolution order."""
    return BaseNamespace(mcls, name, bases, **kwargs)

  def __new__(mcls,
              name: str,
              bases: Bases,
              space: BaseNamespace,
              **kwargs) -> type:
    """The __new__ method is invoked to create the class."""
    namespace = space.compile()
    if '__del__' in namespace and '__delete__' not in namespace:
      if not kwargs.get('trustMeBro', False):
        e = """The namespace encountered the '__del__' method! 
          This method has very limited practical use, significant 
          potential for unexpected behaviour and possibility of using the 
          name '__del__', when '__delete__' were intended. For this 
          reason, implementing the '__del__' method requires also 
          implementing the '__delete__' method or setting the keyword 
          argument 'trustMeBro' to True."""
        raise AttributeError(monoSpace(e))
    return super().__new__(mcls, name, bases, namespace, **kwargs)
