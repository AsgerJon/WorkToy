"""WorkSide - MetaSide - MetaFactory
This provides the metaclass for the factories."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import AbstractMetaType, Bases, AbstractNameSpace


class MetaFactory(AbstractMetaType):
  """WorkSide - MetaSide - MetaFactory
  This provides the metaclass for the factories."""

  @classmethod
  def __prepare__(metacls, name: str, bases: Bases) -> AbstractNameSpace:
    """Returns an instance of the AbstractNameSpace"""
