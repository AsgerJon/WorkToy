"""
PostDeleteDecorator decorates the methods subclasses of
'AbstractDescriptorHook' to specify them as post-delete hooks.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from . import HookDecorator, HookPhase

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Any, Type
  from . import AbstractDescriptorHook as Hook

  AHook: TypeAlias = Type[Hook]


class PostDelete(HookDecorator):
  """
  PostDeleteDecorator decorates the methods subclasses of
  'AbstractDescriptorHook' to specify them as post-delete hooks.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getPrimaryHookPhase(self, ) -> HookPhase:
    """
    Returns the primary hook phase for this decorator.
    """
    return HookPhase.POST_DELETE
