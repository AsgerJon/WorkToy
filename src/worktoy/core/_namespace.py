"""NameSpace provides a flexible mapping for use in the __prepare__ method
of a metaclass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never

from icecream import ic

ic.configureOutput(includeContext=True)


class NameSpace(dict):
  """NameSpace provides a flexible mapping for use in the __prepare__ method
  of a metaclass."""

  def __init__(self, name: str) -> None:
    self._name = name
    dict.__init__(self, )

  def __setitem__(self, key: str, value: Any) -> None:
    """Implementation of item setting"""
    dict.__setitem__(self, key, value)

  def __getitem__(self, key: str, **kwargs) -> Any:
    """Implementation of item getting"""
    return dict.__getitem__(self, key)

  def __delitem__(self, key: str) -> None:
    """Deleter function"""
    dict.__delitem__(self, key, )

  def __missing__(self, key) -> Never:
    """Missing"""
    raise KeyError('Tried finding key: %s, triggering __missing__!' % key)

  def _getName(self) -> str:
    """Getter-function for name"""
    if isinstance(self._name, str):
      return self._name
    raise TypeError

  def _setName(self, *_) -> Never:
    """Illegal Setter function"""
    from worktoy.waitaminute import ReadOnlyError
    raise ReadOnlyError('name')

  def _delName(self) -> Never:
    """Illegal Deleter function"""
    from worktoy.waitaminute import ProtectedPropertyError
    raise ProtectedPropertyError('name')

  name = property(_getName, _setName, _delName)
