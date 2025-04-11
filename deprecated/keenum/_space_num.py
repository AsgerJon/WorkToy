"""SpaceNum provides the namespace class used by the MetaNum metaclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import LoadSpace
from worktoy.keenum import Num
from worktoy.castOLD import maybe
from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self, Callable

  NumList = list[Num]


class SpaceNum(LoadSpace):
  """SpaceNum provides the namespace class used by the MetaNum metaclass."""

  __num_entries__ = None
  __reserved_names__ = ['__num_entries__', '__init__', ]
