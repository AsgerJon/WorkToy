"""
SlowMeta is a metaclass based on 'AbstractMetaclass' whose namespace is
'SlowSpace'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import AbstractMetaclass

from . import SlowSpace

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class SlowMeta(AbstractMetaclass):
  """
  A class statement under 'SlowMeta' runs its body in a 'SlowSpace', so
  every such statement leaves one record in 'SlowSpaceHook.seen'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> SlowSpace:
    return SlowSpace(mcls, name, bases, **kwargs)
