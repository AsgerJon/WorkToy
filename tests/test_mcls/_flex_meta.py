"""
FlexMeta is a metaclass based on 'BaseMeta' whose namespace is
'FlexSpace'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseMeta

from . import FlexSpace

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class FlexMeta(BaseMeta):
  """
  A project's metaclass with a namespace of its own subclasses 'BaseMeta'
  and returns an instance of a 'BaseSpace' subclass from '__prepare__'.
  'FlexMeta' returns a 'FlexSpace'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> FlexSpace:
    return FlexSpace(mcls, name, bases, **kwargs)
