"""
KeyboardModifier demonstrates keyboard modifier flags. These are
combinations of CTRL, SHIFT, ALT, and META keys. The 'value' attribute
is an arbitrary integer representing the modifier combination.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeFlags, KeeFlag

if TYPE_CHECKING:  # pragma: no cover
  pass


class KeyboardModifier(KeeFlags):
  """
  KeyboardModifier demonstrates keyboard modifier flags. These are
  combinations of CTRL, SHIFT, ALT, and META keys. The 'value' attribute
  is an arbitrary integer representing the modifier combination.
  """

  CTRL = KeeFlag('CTRL')
  SHIFT = KeeFlag('SHIFT')
  ALT = KeeFlag('ALT')
  META = KeeFlag('META')
