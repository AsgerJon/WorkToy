"""Signature provides instances for use as keys in the AbstractParser. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Any


class Signature:
  """Provides for systematic searching for a variable"""

  def __init__(self, key: str, defVal: Any, type_: type = None) -> None:
    self._key = key
    self._defVal = defVal
    self._type = type_

  def _getKey(self) -> str:
    """Getter-function for key"""
    return self._key

  def _setKey(self, value: str) -> None:
    """Illegal setter function"""
    if self._key is not None:
      from worktoy.waitaminute import ReadOnlyError
      raise ReadOnlyError('key')
    self._key = value

  def _delKey(self, ) -> Never:
    """Illegal deleter function"""
    from worktoy.waitaminute import ProtectedPropertyError
    raise ProtectedPropertyError('key')

  def _getType(self) -> type:
    """Getter-function for type"""
    return self._type

  def _setType(self, type_: type) -> None:
    """Illegal setter function"""
    if self._type is not None:
      from worktoy.waitaminute import ReadOnlyError
      raise ReadOnlyError('type')
    self._type = type_

  def _delType(self, ) -> Never:
    """Illegal deleter function"""
    from worktoy.waitaminute import ProtectedPropertyError
    raise ProtectedPropertyError('type')

  def _getDefVal(self) -> Any:
    """Getter-function for defVal"""
    return self._defVal

  def _setDefVal(self, defVal: Any) -> None:
    """Illegal setter function"""
    if self._defVal is not None:
      from worktoy.waitaminute import ReadOnlyError
      raise ReadOnlyError('defVal')
    self._defVal = defVal

  def _delDefVal(self, ) -> Never:
    """Illegal deleter function"""
    from worktoy.waitaminute import ProtectedPropertyError
    raise ProtectedPropertyError('defVal')

  key = property(_getKey, _setKey, _delKey)
  type = property(_getType, _setType, _delType)
  defVal = property(_getDefVal, _setDefVal, _delDefVal)
