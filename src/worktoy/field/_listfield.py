"""ListField is a subclass of BaseField for use with lists"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Iterable, cast, Any

from worktoy.field import BaseField, PermissionLevel


class ListField(BaseField):
  """ListField is a subclass of BaseField for use with lists"""

  @classmethod
  def _getPermissionLevel(cls) -> PermissionLevel:
    """Implementation allowing setting and reading, but not deleting"""
    return PermissionLevel.READ_ONLY

  def __init__(self, ) -> None:
    BaseField.__init__(self, [], list)

  def _explicitSetter(self, newValue: Any) -> None:
    """Reimplementation which appends each value found in newValue to self
    if newValue is iterable, or simply appends newValue otherwise."""
    if getattr(newValue, '__iter__', None) is not None:
      for item in cast(Iterable, newValue):
        self.append(item)
    else:
      self.append(newValue)

  def __getattr__(self, key: str) -> Any:
    """Keys that are not present in this class namespace, might be present
    in the list namespace."""
    listNameSpace = getattr(list, '__iter__', )
    func = getattr(listNameSpace, key, None)
    if func is not None:
      if callable(func):
        return lambda instance, *args: func(self.value, *args)
    raise AttributeError(key)

  def __iter__(self) -> ListField:
    """Implementation of iteration"""
    self._curInd = 0
    return self

  def __next__(self) -> Any:
    """Implementation of iteration"""
    self._curInd += 1
    if self._curInd > len(self._value):
      raise StopIteration
    return self._value[self._curInd - 1]
