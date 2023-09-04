"""WorkToy - MetaClass - MetaNumClass
The metaclass for custom numerical types."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Bases
from worktoy.metaclass import AbstractMetaClass, MetaNumSpace


class MetaNumClass(AbstractMetaClass):
  """WorkToy - MetaClass - MetaNumClass
  The metaclass for custom numerical types."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs):
    return MetaNumSpace()
