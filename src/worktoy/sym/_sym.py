"""WorkToy - SYM - SYM
The basic class implementing Enum like behaviour."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic

from worktoy.base import DefaultClass
from worktoy.core import ARGS, KWARGS
from worktoy.fields import AbstractField, StrField, IntField
from worktoy.guards import TypeGuard

ic.configureOutput(includeContext=True)


class SYM(DefaultClass):
  """WorkToy - SYM - AUTO
  Special class denoting an instance on the class body."""

  __symbolic_baseclass__ = True
  __decorated_classes__ = {}

  @classmethod
  def _incrementInstanceCount(cls, targetClass: type) -> None:
    count = cls.__decorated_classes__.get(targetClass, None)
    if count is None:
      cls.__decorated_classes__[targetClass] = 1
      setattr(targetClass, 'NULL', cls.auto())
    else:
      cls.__decorated_classes__[targetClass] += 1

  @classmethod
  def _getInstanceCount(cls, targetClass: type) -> int:
    return cls.__decorated_classes__.get(targetClass, 0)

  value = IntField(-1)
  name = StrField('DefaultName')
  owner = AbstractField(int)

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
    self.name = name
    self.owner = cls
    self.value = self._getInstanceCount(cls)
    self._incrementInstanceCount(cls)

  def setValue(self, value: int) -> None:
    """Setter-function for inner value"""
    self._value = self.intGuard(value, 'value')

  @classmethod
  def auto(cls, *args, **kwargs) -> SYM:
    """Used to define a new instance"""
    return cls(*args, **kwargs)

  def setInnerClass(self, *args, **kwargs) -> None:
    """Setter-function for the inner class."""
    self._innerClass = self.maybeType(type, *args)
    self.applyGetAttr(self._innerClass)

  def getInnerClass(self, ) -> type:
    """Getter-function for the inner class."""
    return self._innerClass

  def setInnerInstance(self, *args, **kwargs) -> None:
    """Setter-function for the inner instance."""
    self._innerInstance = self.maybeType(self.getInnerClass(), *args)
    setattr(self._innerInstance, '__symbolic_wrapper__', self)

  def getInnerInstance(self, ) -> Any:
    """Getter-function for the inner instance"""
    if isinstance(self._innerInstance, self._innerClass):
      return self._innerInstance

  def getArgs(self) -> ARGS:
    """Getter-function for args."""
    return self._args

  def getKwargs(self) -> KWARGS:
    """Getter-function for kwargs."""
    return {**self._kwargs, '__instance_creation__': True}

  def __str__(self) -> str:
    """String representation"""
    return self.name.upper()

  def __repr__(self) -> str:
    """String representation"""
    return """name: %s, value: %s""" % (self.name.upper(), self.value)

  def __getattr__(self, key: str) -> Any:
    innerClass = object.__getattribute__(self, 'innerClass')
    try:
      object.__getattribute__(innerClass, key)
    except AttributeError as e1:
      innerInstance = object.__getattribute__(self, 'innerInstance')
      try:
        object.__getattribute__(innerInstance, key)
      except AttributeError as e2:
        raise e1 from e2

  def applyGetAttr(self, cls: type) -> type:
    """Applies new __getattr__ to the target class."""

    def __new_getattr__(instance, key: str) -> Any:
      """Replacement getattr"""
      if key == 'getInstances':
        return object.__getattribute__(instance, '__symbolic_instances__')
      try:
        return object.__getattribute__(instance, key.lower())
      except AttributeError as e:
        return object.__getattribute__(self, key)

    setattr(self.getInnerClass(), '__getattr__', __new_getattr__)

    return self.getInnerClass()

  def __add__(self, other: Any) -> Any:
    if isinstance(other, int):
      cls = self.getInnerClass()
      from worktoy.sym import SyMeta
      if isinstance(cls, SyMeta):
        n = len(cls)
        ind = self.value + other
        return cls(ind % n)
    if isinstance(other, self.__class__):
      return self + other.value
    return NotImplemented

  def __sub__(self, other: Any) -> Any:
    if isinstance(other, int):
      cls = self.getInnerClass()
      from worktoy.sym import SyMeta
      if isinstance(cls, SyMeta):
        n = len(cls)
        ind = self.value - other
        while ind < 0:
          ind += n
        return cls(ind % n)
    if isinstance(other, self.__class__):
      return self - other.value
    return NotImplemented

  def __radd__(self, other: Any) -> Any:
    return self + other

  def __rsub__(self, other: Any) -> Any:
    if isinstance(other, int):
      return other - self.value

  def __ne__(self, other: Any) -> bool:
    if isinstance(other, int):
      return True if self - other else False
    if isinstance(other, self.__class__):
      return self != other.value
    return NotImplemented

  def __eq__(self, other: Any) -> bool:
    other = other.value if isinstance(other, self.__class__) else other
    if not isinstance(other, int):
      return NotImplemented
    return False if self - other else True

  def __call__(self, *args, **kwargs) -> Any:
    innerInstance = self.getInnerInstance()
    return innerInstance(*args, **kwargs)

  def __rshift__(self, other) -> Any:
    return self.getInnerInstance() >> other
