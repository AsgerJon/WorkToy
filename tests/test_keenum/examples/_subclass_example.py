"""
SubclassExample provides a subclass of FlagsExample.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlag
from . import FlagsExample


class SubclassExample(FlagsExample):
  """
  SubclassExample subclasses the 'FlagsExample' to test that subclassing
  functions correctly.
  """

  TOGETHER = KeeFlag('TOGETHER')
  FOREVER = KeeFlag('FOREVER')
