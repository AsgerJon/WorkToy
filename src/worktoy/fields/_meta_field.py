"""WorkToy - Fields - MetaField
Metaclass of the field classes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Bases
from worktoy.metaclass import BaseNameSpace, BaseMetaClass

from icecream import ic

ic.configureOutput(includeContext=True)


class MetaField(BaseMetaClass):
  """Meta field"""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    return BaseNameSpace(name, bases)

  @classmethod
  def __create_with__(mcls, other: type, **kwargs) -> type:
    otherName = getattr(other, '__qualname__', str(other))
    name = '%sField' % otherName
    bases = (*mcls.__bases__, other)
    nameSpace = mcls.__prepare__(name, bases, **kwargs)
    return mcls.__new__(mcls, name, bases, nameSpace, **kwargs)

  def __matmul__(cls, other: type) -> type:
    return cls.__create_with__(other, )
