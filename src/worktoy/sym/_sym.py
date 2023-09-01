"""WorkToy - SYM - SYM
The basic class implementing Enum like behaviour."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.base import DefaultClass
from worktoy.core import ARGS, KWARGS
from worktoy.guards import TypeGuard


class SYM(DefaultClass):
  """WorkToy - SYM - AUTO
  Special class denoting an instance on the class body."""

  value = IntField(0)
  name = StringField('')

  __symbolic_baseclass__ = True

  intGuard = TypeGuard(int)
  classGuard = TypeGuard(type)

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._value = None
    self._name = None
    self._owner = None
    self._innerInstance = None
    self._innerClass = None
    self._args = args
    self._kwargs = kwargs
    setattr(self, '__symbolic_instance__', True)

  def __set_name__(self, cls: type, name: str) -> None:
    self._name = name
    self._owner = cls

  def setValue(self, value: int) -> None:
    """Setter-function for inner value"""
    self._value = self.intGuard(value, 'value')

  @classmethod
  def auto(cls, *args, **kwargs) -> SYM:
    """Used to define a new instance"""
    return cls(*args, **kwargs)

  def setInnerClass(self, *args, **kwargs) -> None:
    """Setter-function for the inner class."""
    self._innerClass = self.classGuard(self.maybeType(type, *args))
    self.applyGetAttr(self._innerClass)

  def getInnerClass(self, ) -> type:
    """Getter-function for the inner class."""
    return self.classGuard(self._innerClass)

  def setInnerInstance(self, *args, **kwargs) -> None:
    """Setter-function for the inner instance."""
    self._innerInstance = self.maybeType(self.getInnerClass(), *args)

  def getArgs(self) -> ARGS:
    """Getter-function for args."""
    return self._args

  def getKwargs(self) -> KWARGS:
    """Getter-function for kwargs."""
    return {**self._kwargs, '__instance_creation__': True}

  def __str__(self) -> str:
    """String representation"""
    return self._name.upper()

  def __repr__(self) -> str:
    """String representation"""
    return """name: %s, value: %s""" % (self._name.upper(), self._value)

  def applyGetAttr(self, cls: type) -> type:
    """Applies new __getattr__ to the target class."""

    def __new_getattr__(instance, key: str) -> Any:
      """Replacement getattr"""
      if key == 'getInstances':
        return object.__getattribute__(instance, '__symbolic_instances__')
      return object.__getattribute__(instance, key.lower())

    setattr(self.getInnerClass(), '__getattr__', __new_getattr__)

    return self.getInnerClass()
