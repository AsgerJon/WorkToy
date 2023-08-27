"""WorkToy - Core - DescriptorDictionary
Maps types to descriptors."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import (FLOAT, INT, STR, FLAG,
                          FunctionTuple, CLASS, CALL, AbstractDescriptor,
                          StringAware)


class DescriptorDictionary(StringAware):
  """WorkToy - Core - DescriptorDictionary
  Maps types to descriptors."""

  _descriptors = [FLAG, FLOAT, INT, STR, CALL, CLASS]
  _types = [bool, float, int, str, FunctionTuple, type]

  @classmethod
  def getNames(cls) -> list[str]:
    """Getter-function for descriptor names."""
    return cls().stringList('bool, float, int, str, func, type')

  @classmethod
  def getDescriptors(cls) -> list[type]:
    """Getter-function for descriptors."""
    return cls._descriptors

  @classmethod
  def getDescriptorTypes(cls) -> list:
    """Getter-function for the descriptors available."""
    return [bool, float, int, str, FunctionTuple, type]

  @classmethod
  def getDescriptorDictionary(cls) -> dict[str, AbstractDescriptor]:
    """Getter-function for the descriptor dictionary."""
    keys, values = cls.getNames(), cls.getDescriptors()
    return {k: v for (k, v) in zip(keys, values)}

  @classmethod
  def __class_getitem__(cls, typeName: object) -> type:
    """Returns the descriptor matching the name given. """
    names = cls.getNames()
    types = cls.getDescriptorTypes()
    descriptors = cls.getDescriptors()
    for (name, type_, desc) in zip(names, types, descriptors):
      if typeName is type_ or typeName == name:
        return desc
    return cls.getDescriptors()[-1]
