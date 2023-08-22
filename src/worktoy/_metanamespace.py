"""MetaNameSpace is """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy import AbstractMetaType, DefaultClass

ic.configureOutput(includeContext=True)
Keys = type({}.keys())
Values = type({}.values())
Items = type({}.items())

Bases = tuple[type]


class _MinNameSpace(DefaultClass):
  """Minimal namespace"""

  def __init__(self,
               name: str = None,
               bases: tuple = None,
               *__, **_) -> None:
    self._iterContents = None
    self._bases = bases
    self._className = name
    self._contents = {}
    self._entries = []

  def _resetIterContents(self) -> None:
    """Creator function for the iterable object"""
    self._iterContents = [key for key in self.keys()]

  def _getIterContents(self) -> list[keys]:
    """Getter-function for the iterable object"""
    if self._iterContents:
      return self._iterContents
    self._iterContents = None
    raise StopIteration

  def __contains__(self, key: str) -> bool:
    return True if key in self._contents.keys() else False

  def __setitem__(self, key: str, val: object) -> None:
    self._contents[key] = val
    self._entries.append((key, val))
    self._explicitSetter(key, val)

  def __getitem__(self, key: str) -> object:
    if key not in self._contents.keys():
      raise KeyError
    explicitVal = self._explicitGetter(key)
    fallbackVal = self._contents[key]
    return self.maybe(explicitVal, fallbackVal)

  def __delitem__(self, key: str) -> None:
    if key not in self._contents.keys():
      raise KeyError
    self._contents.pop(key)
    self._explicitDeleter(key)

  def _explicitGetter(self, key: str) -> object:
    """Explicit Getter"""

  def _explicitSetter(self, key: str, val: object) -> None:
    """Explicit Setter"""

  def _explicitDeleter(self, key: str) -> None:
    """Explicit Deleter"""

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
    """Creates a dict version.
    Subclasses should reimplement this method because the base
    implementation does nothing beyond what is done by the builtin dict."""
    return self._contents

  def __iter__(self, ) -> _MinNameSpace:
    """Implementation of iteration"""
    self._resetIterContents()
    return self

  def __next__(self) -> str:
    """Implementation of iteration"""
    return self._getIterContents().pop()


class MetaNameSpace(AbstractMetaType):
  """The meta-namespace class ensures that derived classes adhere to the
  namespace requirements described in the documentation of the
  AbstractNameSpace. This metaclass is a subclass of the AbstractMetaType."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    """The meta namespace is the namespace dict collected during creation
    of the _MinNameSpace class. """
    nameSpace = getattr(_MinNameSpace, '__dict__', None)
    if nameSpace is None:
      raise TypeError
    out = {}
    for (key, val) in nameSpace.items():
      out |= {key: val}
    return out

  def __new__(mcls,
              name: str,
              bases: tuple,
              nameSpace: dict,
              **_) -> type:
    keys = ['__getitem__', '__setitem__', '__delitem__', '__contains__']
    for key in keys:
      val = getattr(_MinNameSpace, key, None)
      if val is None:
        raise KeyError(key)
      nameSpace[key] = val
    keys = ['_explicitGetter', '_explicitSetter', '_explicitDeleter']
    for key in keys:
      if key not in nameSpace:
        raise TypeError
    return AbstractMetaType.__new__(mcls, name, bases, nameSpace, )


class AbstractNameSpace(_MinNameSpace):
  """AbstractNameSpace provides a baseclass for custom namespaces used by
  a custom metaclass."""

  def __init__(self, *args, **kwargs) -> None:
    _MinNameSpace.__init__(self, *args, **kwargs)
