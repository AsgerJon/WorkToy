"""
KeyboardModifier demonstrates keyboard modifier flags. These are
combinations of CTRL, SHIFT, ALT, and META keys. The 'value' attribute
is an arbitrary integer representing the modifier combination.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag


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
