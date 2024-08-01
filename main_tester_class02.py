"""LOL"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

if sys.version_info.minor < 9:
  Any = object
elif sys.version_info.minor < 10:
  Self = object
  from typing import Any, Callable
elif sys.version_info.minor < 11:
  Self = object
  from typing import Any
else:
  from typing import Any, Self


class Namespace:
  """LMAO"""

  __inner_space__ = None
  __iter_contents__ = None

  def _getInnerSpace(self) -> dict:
    """LMAO"""
    return {} if self.__inner_space__ is None else self.__inner_space__

  def __iter__(self, ) -> Self:
    """Implementation of iteration protocol"""
    self.__iter_contents__ = [k for (k, v) in self._getInnerSpace().items()]
    return self

  def __next__(self, ) -> Any:
    """Implementation of iteration protocol"""
    if self.__iter_contents__:
      return self.__iter_contents__.pop()
    raise StopIteration

  def __getitem__(self, key: str) -> Any:
    """LMAO"""
    innerSpace = self._getInnerSpace()
    try:
      return dict.__getitem__(innerSpace, key)
    except KeyError as keyError:
      raise keyError

  def __setitem__(self, key: str, value: Any) -> None:
    """LMAO"""
    innerSpace = self._getInnerSpace()
    self.__inner_space__ = {**innerSpace, **{key: value}}


class MetaType:
  """LMAO"""

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs) -> Namespace:
    """LMAO"""
    return Namespace()

  def __new__(mcls, name, bases, namespace, **kwargs) -> type:
    """LMAO"""
    attrs = {}
    if not isinstance(namespace, dict):
      for key in namespace:
        attrs[key] = namespace[key]
    else:
      attrs = namespace
    return type(name, bases, attrs)

  def __str__(cls, ) -> str:
    """String representation"""
    mcls = type(cls)
    mclsName = mcls.__name__
    clsName = cls.__name__
    moduleName = cls.__module__
    return """%s.%s(%s)""" % (moduleName, clsName, mclsName)

  def __getitem__(cls, key: str) -> Any:
    """LMAO"""
    print(getattr(cls, '__class_getitem__', 'LMAO'))
    mcls = type(cls)
    mclsName = mcls.__name__
    clsName = cls.__name__
    print('%s.%s[%s]' % (mclsName, clsName, key))

  __setitem__ = lambda: print('lmao')

  # def __setitem__(cls, key: str, value) -> None:
  #   """LMAO"""
  #   print("""%s.__setitem__[%s] = %s""" % (cls.__name__, key, str(value)))

  def __getattr__(cls, key: str) -> Any:
    """LMAO"""
    print("""%s.%s""" % (cls.__name__, key))

  def __getattribute__(self, key: str) -> Any:
    """LMAO"""
    if key == '__bases__':
      return (type,)
    if key == '__class__':
      return type
    return object.__getattribute__(self, key)


def factory(msg: str) -> Callable:
  """LMAO"""

  def inner() -> None:
    """LMAO"""
    print(msg)

  return inner


class TestClass(metaclass=MetaType):
  """LOL"""

  lmao = True

  def lol(self, callMeMaybe: Callable = None) -> Callable:
    if callMeMaybe is None:
      return self
    return callMeMaybe

  def fuckoff(self) -> None:
    """lmao"""
