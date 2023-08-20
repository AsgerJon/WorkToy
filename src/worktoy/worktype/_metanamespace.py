"""MetaNameSpace is """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.worktype import AbstractMetaType

Keys = type({}.keys())
Values = type({}.values())
Items = type({}.items())


class _MinimalNameSpace:
  """Minimal namespace"""

  def __init__(self, name: str, bases: tuple) -> None:
    self._bases = bases
    self._className = name
    self._contents = {}

  def __contains__(self, key: str) -> bool:
    return True if key in self._contents.keys() else False

  def __setitem__(self, key: str, val: object) -> None:
    self._contents[key] = val

  def __getitem__(self, key: str) -> object:
    if key in self._contents.keys():
      return self._contents[key]
    raise KeyError

  def __delitem__(self, key: str) -> None:
    newDict = {}
    for (k, v) in self._contents.items():
      if k != v:
        newDict |= {k: v}
    self._contents = newDict

  def keys(self) -> Keys:
    """Implementation of keys method"""
    return self._contents.keys()

  def values(self) -> Values:
    """Implementation of values method"""
    return self._contents.values()

  def items(self) -> Items:
    """Implementation of items"""
    return self._contents.items()

  def asDict(self) -> dict:
    """creates a dict version"""
    return self._contents


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
    keys = []
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
