"""
BlockHook is a minimal hook that prevents assignment to specific names
in a namespace. It overrides 'setItemHook' and returns True to block
the default behavior for any disallowed key.

This hook is intended for testing control flow in hook-enabled
namespace evaluation, especially to verify that hook return values can
intercept and block assignments during class construction.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls.hooks import AbstractHook

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class BlockHook(AbstractHook):
  """Blocks setting keys named 'blocked' or '_forbidden'."""

  def setItemHook(self, key: str, val: Any, old: Any) -> bool:
    """
    Return True to block setting the key if it matches one of the
    disallowed names.
    """
    return True if key in {'blocked', '_forbidden'} else False
