"""WorkToy - MetaClass - MetaField
Implementation of function overloading."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Bases
from worktoy.metaclass import AbstractMetaClass, FieldSpace


class MetaField(AbstractMetaClass):
  """WorkToy - MetaClass - MetaField
  Implementation of function overloading."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> FieldSpace:
    """Implementation of the nameSpace class."""
    return FieldSpace()
