"""
ClaimedMeta is 'LoggedMeta' with 'ClaimedSpace' as its namespace.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import LoggedMeta, ClaimedSpace

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class ClaimedMeta(LoggedMeta):
  """
  A metaclass based on another may swap the namespace again.
  'ClaimedMeta' returns a 'ClaimedSpace', whose hooks claim, refuse and
  swap, so a class statement under it shows every hook route.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> ClaimedSpace:
    return ClaimedSpace(mcls, name, bases, **kwargs)
