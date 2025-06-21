"""
HookPhases enumerates the different phases of the descriptor protocol flow
exposed to hooks.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class HookPhase(Enum):
  """
  HookPhases enumerates the different phases of the descriptor protocol flow
  exposed to hooks.
  """

  PRE_GET = 'pre_get'
  POST_GET = 'post_get'
  PRE_SET = 'pre_set'
  POST_SET = 'post_set'
  PRE_DELETE = 'pre_delete'
  POST_DELETE = 'post_delete'
