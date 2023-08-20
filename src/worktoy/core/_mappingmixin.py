"""MappingMixin provides for dictionary like behaviour"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod


class AbstractMappingMixin:
  """MappingMixin provides for dictionary like behaviour"""

  @abstractmethod
  def _explicitItemGet(self, key: object, ) -> object:
    """Subclasses must implement what exactly should happen on the getter of
    the item at given key"""

  @abstractmethod
  def _explicitItemSet(self, key: object, value: object) -> None:
    """Subclasses must implement what exactly should happen on the setter of
    the item at given key"""

  @abstractmethod
  def _explicitItemDel(self, key: object, ) -> None:
    """Subclasses must implement what exactly should happen on the setter of
    the item at given key"""

  @abstractmethod
  def _getKeys(self) -> list[object]:
    """Subclasses must implement a getter function for the list of keys."""

  def __getitem__(self, key: object, ) -> object:
    """Item getter"""
    out = self._explicitItemGet(key)
    if out is None:
      raise KeyError(key)
    return out

  def __setitem__(self, key: object, val: object) -> None:
    """Item Setter"""
    self._explicitItemSet(key, val)

  def __delitem__(self, key: object) -> None:
    """Item deleter"""
    self._explicitItemDel(key)

  def keys(self) -> list[object]:
    """Implementation of keys"""
    return [key for key in self._getKeys()]

  def values(self) -> list[object]:
    """Implementation of values"""
    return [self[key] for key in self._getKeys()]

  def items(self) -> list[tuple[object, object]]:
    """Implementation of items"""
    return [(key, val) for (key, val) in zip(self.keys(), self.values())]


class MappingMixin(AbstractMappingMixin):
  """Simplified subclass. This subclass has only one abstract method. The
  _getContents(self) -> dict. The returned dictionary are accessed by this
  mixin."""

  @abstractmethod
  def _getContents(self) -> dict:
    """Subclasses must implement this method to specify the dictionary to
    be used as the basis of the mapping"""

  def _explicitItemGet(self, key: object, ) -> object:
    """Implementation of getter"""
    return self._getContents().get(key, None)

  def _explicitItemSet(self, key: object, val: object) -> object:
    """Implementation of getter"""
    return self._getContents().update({key: val})

  def _explicitItemDel(self, key: object, ) -> object:
    """Implementation of getter"""
    return self._getContents().update({key: None})

  def _getKeys(self) -> list[object]:
    """Implementation of key getter"""
    return [key for key in self._getContents()]
