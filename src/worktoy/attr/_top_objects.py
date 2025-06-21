"""
This file provides the two private descriptors representing the top-level
instance and owner of the descriptor owning the hook that owns this
descriptor.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..static import AbstractObject

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Callable, Self


class _TopInstance(AbstractObject):
  """
  This private descriptor reflects the top-level instance of the descriptor
  owning the hook that owns this descriptor.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, **kwargs) -> Any:
    """
    Returns the top-level instance of the descriptor owning the hook.
    """
    return self.instance.instance


class _TopOwner(AbstractObject):
  """
  This private descriptor reflects the top-level owner of the descriptor
  owning the hook that owns this descriptor.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, **kwargs) -> Any:
    """
    Returns the top-level instance of the descriptor owning the hook.
    """
    return self.instance.owner
