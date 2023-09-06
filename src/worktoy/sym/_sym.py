"""WorkToy - SYM - SYM
The basic class implementing Enum like behaviour."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never

from icecream import ic

from worktoy.base import DefaultClass

ic.configureOutput(includeContext=True)


class SYM(DefaultClass):
  """WorkToy - SYM - AUTO
  Special class denoting an instance on the class body."""
  __symbolic_baseclass__ = True
  __decorated_classes__ = {}

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._value = None
    self._name = None
    self._owner = None
    self.innerClass = None
    self.innerInstance = None
    setattr(self, '__symbolic_instance__', True)

  @classmethod
  def auto(cls, *args, **kwargs) -> SYM:
    """Used to define a new instance"""
    return cls(*args, **kwargs)

  def getName(self) -> str:
    """Getter-function for name"""
    return self._name

  def __set_name__(self, cls: type, name: str) -> None:
    self._name = name
    self._owner = cls
    existing = self.__class__.__decorated_classes__.get(cls, [])
    self.__class__.__decorated_classes__[cls] = [*existing, cls]
    args = self.getArgs()
    kwargs = dict(__instance_creation__=True, **self.getKwargs())
    newInstance = cls(*args, **kwargs)
    setattr(self, 'innerClass', cls)
    setattr(self, 'innerInstance', newInstance)
    existing = getattr(self._owner, '__symbolic_instances__', [])
    setattr(self, 'value', len(existing))
    setattr(self._owner, '__symbolic_instances__', [*existing, self])

  def __get__(self, obj: object, cls: type) -> Any:
    try:
      return self
    except AttributeError as e:
      raise e

  def __set__(self, obj: object, newValue: Any) -> Never:
    if isinstance(newValue, SYM):
      innerInstance = getattr(newValue, 'innerInstance', None)
      if innerInstance.__class__ == obj.__class__:
        obj = innerInstance

  def __delete__(self, *_) -> Never:
    raise NotImplementedError

  def __getattr__(self, key: str) -> Any:
    try:
      return object.__getattribute__(self, key.lower())
    except AttributeError as e:
      raise e

  def __str__(self, ) -> str:
    if self.innerClass:
      clsName = self.innerClass.__qualname__
      insName = self.innerInstance.__name__
      return 'SYM wrapper on \'%s\' of %s' % (self._name, clsName)
    return 'SYM before wrapping'

  def __repr__(self, ) -> str:
    clsName = '' if self.innerClass is None else self.innerClass.__qualname__
    return 'SYM(%s.%s)' % (clsName, self._name)
