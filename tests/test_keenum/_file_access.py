"""
FileAccess is a flags class whose members carry bytes values.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag


class FileAccess(KeeFlags):
  """
  The value of a flags member is whatever the nearest '_getValue' along
  the resolution order gives. 'FileAccess' gives each member its index
  as a digit in bytes, so its value type is 'bytes' and a lookup by
  value compares bytes with bytes.
  """

  OPEN = KeeFlag()
  CLOSE = KeeFlag()

  def _getValue(self) -> bytes:
    return str(self.index).encode()
