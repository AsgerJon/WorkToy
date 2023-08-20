"""MetaNameSpace is """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.worktype import AbstractMetaType


class _MinimalNameSpace(dict):
  """This class provides the minimum methods required by a namespace. """

  def _getShadowContents(self, ) -> dict:
    """Getter-function for the shadow_contents"""
    existing = getattr(self, '__shadow_contents_value__', None)
    if existing is None:
      setattr(self, '__shadow_contents_value__', {})
    val = getattr(self, '__shadow_contents_value__', None)
    if val is None:
      raise TypeError
    return val

  def __getitem__(self, key: str) -> object:
    """Item getter"""
    if key not in self.__shadow_contents__.keys():
      raise KeyError(key)
    return self._explicitGetter(key)

  def __setitem__(self, key: str, val: object) -> None:
    """Item Setter"""
    self.__shadow_contents__.update({key: val})
    self._explicitSetter(key, val)

  def __delitem__(self, key: str) -> None:
    """Item Deleter"""
    self.__shadow_contents__.update({key: None})
    self._explicitDeleter(key)

  def __contains__(self, key: str) -> bool:
    """Implementation of membership check"""
    return True if key in self.__shadow_contents__.keys() else False

  def _explicitGetter(self, key: str) -> object:
    """The explicit getter"""
    val = self.__shadow_contents__.get(key, None)
    if val is not None:
      return val
    raise KeyError(key)

  def _explicitSetter(self, key: str, val: object) -> None:
    """The explicit setter"""
    self.__shadow_contents__.update({key: val})

  def _explicitDeleter(self, key: str) -> None:
    """The explicit deleter"""
    self.__shadow_contents__.update({key: None})

  __shadow_contents__ = property(_getShadowContents)


class MetaNameSpace(AbstractMetaType):
  """The meta-namespace class ensures that derived classes adheres to the
  namespace requirements described in the documentation of the
  AbstractNameSpace. This metaclass subclasses the AbstractMetaType."""

  def __new__(mcls,
              name: str,
              bases: tuple,
              nameSpace: dict,
              **_) -> type:
    keys = ['__getitem__', '__setitem__', '__delitem__', '__contains__']
    for key in keys:
      val = getattr(_MinimalNameSpace, key, None)
      if val is None:
        raise KeyError(key)
      nameSpace[key] = val
    keys = ['_explicitGetter', '_explicitSetter', '_explicitDeleter']
    for key in keys:
      existing = nameSpace.get(key, None)
      if existing is None:
        val = getattr(_MinimalNameSpace, key, None)
        if val is None:
          raise TypeError
        nameSpace |= {key: val}
    return AbstractMetaType.__new__(mcls, name, bases, nameSpace, )


class AbstractNameSpace(_MinimalNameSpace, metaclass=MetaNameSpace):
  """AbstractNameSpace provides a baseclass for custom namespaces used by
  a custom metaclass."""
  pass
