"""KeeFlagsMeta provides the metaclass for KeeFlags."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeMeta
from worktoy.mcls import AbstractMetaclass
from . import KeeFlagsSpace as KSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Self

  Bases: TypeAlias = tuple[type, ...]


class KeeFlagsMeta(KeeMeta):
  """KeeFlagsMeta is the metaclass for KeeFlags, providing additional
  functionality for handling flags."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kw) -> KSpace:
    """Replaces the KeeSpace with KeeFlagsSpace"""
    bases = (*[b for b in bases if b.__name__ != '_InitSub'],)
    return KSpace(mcls, name, bases, **kw)

  def __new__(mcls, name: str, bases: Bases, space: KSpace, **kw) -> Self:
    """
    Creates a new instance of the class.
    This method is called when the class is created.
    """
    if name == 'KeeFlags':
      return AbstractMetaclass.__new__(mcls, name, bases, space, **kw)
    return super().__new__(mcls, name, bases, space.expandNum(), **kw)
