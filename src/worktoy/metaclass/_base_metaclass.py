"""WorkToy - MetaClass - BaseMeta
Basic metaclass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Bases
from worktoy.metaclass import AbstractMetaClass, BaseNameSpace


class BaseMetaClass(AbstractMetaClass):
  """WorkToy - MetaClass - BaseMeta
  Basic metaclass."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> BaseNameSpace:
    """Implementation of __prepare__"""
    return BaseNameSpace(name, bases, **kwargs)
