"""WorkToy - Core - Cls
A subclass of InlineDescriptor where source 'type' is the same as the owner
type. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.core import AbstractDescriptor

ic.configureOutput(includeContext=True)


class CLS(AbstractDescriptor):
  """WorkToy - Core - Cls
  A subclass of InlineDescriptor where source 'type' is the same as the owner
  type. """

  @classmethod
  def __special_descriptor__(cls, argTuple: tuple,
                             originCls: type) -> AbstractDescriptor:
    """Implementing alternative creation"""
    newInstance = originCls()
    newInstance.__unique_name__ = 'newInstance'
    ownerSetter = getattr(originCls, 'setOwner', None)
    valueTypeSetter = getattr(originCls, 'setValueType', None)

    if ownerSetter is None:
      raise TypeError

    def newSetter(self, owner: type) -> None:
      """Replacement setter function for value type"""
      if self is newInstance:
        valueTypeSetter(newInstance, owner)
      return ownerSetter(self, owner)

    setattr(originCls, 'setOwner', newSetter)
    return newInstance
