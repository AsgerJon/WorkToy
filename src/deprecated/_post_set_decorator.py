"""
PostSetDecorator decorates the methods subclasses of
'AbstractDescriptorHook' to specify them as post-set hooks.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import HookDecorator, HookPhase

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import TypeAlias, Type
  from . import AbstractDescriptorHook

  AHook: TypeAlias = Type[AbstractDescriptorHook]


class PostSet(HookDecorator):
  """
  PostSet decorates methods that should be called during the post-set
  phase of the descriptor lifecycle in classes that inherit from
  'AbstractDescriptorHook'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getPrimaryHookPhase(self, ) -> HookPhase:
    """
    Returns the primary hook phase for this decorator.
    """
    return HookPhase.POST_SET
