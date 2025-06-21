"""
PreSetDecorator decorates the methods subclasses of
'AbstractDescriptorHook' to specify them as pre-set hooks.
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
  pass


class PreSet(HookDecorator):
  """
  PreSetDecorator decorates the methods subclasses of
  'AbstractDescriptorHook' to specify them as post-get hooks.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getPrimaryHookPhase(self, ) -> HookPhase:
    """
    Returns the primary hook phase for this decorator.
    """
    return HookPhase.PRE_SET
