"""BaseMeta provides a basic metaclass. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import Dispatch
from worktoy.mcls import AbstractMetaclass, Base
from worktoy.mcls import BaseSpace as BSpace
from worktoy.mcls import Types

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self, Callable, Never


class BaseMeta(AbstractMetaclass):
  """BaseMeta provides a basic metaclass."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Types, **kwargs) -> BSpace:
    """Prepare the class namespace."""
    return BSpace(mcls, name, bases, **kwargs)
