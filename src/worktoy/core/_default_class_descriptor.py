"""WorkToy - Core - DefaultClassDescriptor
Special descriptor allowing access to the default class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

ic.configureOutput(includeContext=True)


class STR:
  """Quick Descriptor"""

  def __set_name__(self, owner: type, name: str) -> None:
    self._name, self._owner = name, owner
    setattr(owner, '_%s' % self._name, '')

  def __get__(self, obj: object, cls: type) -> str:
    k = '_%s' % self._name
    val = (0, getattr(obj, k, (1, getattr(self._owner, k, (2, None)))))
    if val[0]:
      setattr(obj, k, val[1])
    return val[1]

  def __set__(self, obj: object, newVal: str) -> None:
    ic(self, obj, newVal)
    k = '_%s' % self._name
    setattr(obj, k, newVal) or setattr(self._owner, k, newVal)


class DefaultClassDescriptor:
  """WorkToy - Core - DefaultClassDescriptor
  Special descriptor allowing access to the default class."""

  fuck = STR()

  def __init__(self, ) -> None:
    self._fieldName = None
    self._owner = None

  def __set_name__(self, owner: type, name: str) -> None:
    self._setFieldName(name)
    self._setOwner(owner)

  def _setFieldName(self, name: str) -> None:
    self._fieldName = name

  def _setOwner(self, owner: type) -> None:
    self._owner = owner

  def _getFieldName(self, ) -> str:
    return self._fieldName

  def _getOwner(self) -> type:
    return self._owner

  def __str__(self) -> str:
    return self.fuck + '__str__'

  def __repr__(self) -> str:
    return self.fuck + '__repr__'
