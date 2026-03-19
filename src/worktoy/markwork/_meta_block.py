"""
MetaBlock subclasses 'BaseMeta' and provides the metaclass for block
components.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcls import BaseMeta
from . import BlockSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class MetaBlock(BaseMeta):
  """
  MetaBlock subclasses 'BaseMeta' and provides the metaclass for block
  components.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> BlockSpace:
    return BlockSpace(mcls, name, bases, **kwargs)
