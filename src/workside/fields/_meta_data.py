"""WorkSide - Fields - MetaData
Metaclass for use by data classes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.fields import DataSpace
from worktoy.core import Map, Bases
from worktoy.metaclass import AbstractMetaClass


class MetaData(AbstractMetaClass):
  """WorkSide - Fields - MetaData
  Metaclass for use by data classes."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> Map:
    return DataSpace(mcls, name, bases, **kwargs)
