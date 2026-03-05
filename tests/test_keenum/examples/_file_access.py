"""
FileAccess demonstrates real-world bitmask flags for file permissions.
These are combinations of READ, WRITE, EXECUTE, and DELETE permissions.
The 'value' attribute is the bitmask representing the permissions.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeFlags, KeeFlag

if TYPE_CHECKING:  # pragma: no cover
  pass


class FileAccess(KeeFlags):
  """
  FileAccess demonstrates real-world bitmask flags for file permissions.
  These are combinations of READ, WRITE, EXECUTE, and DELETE permissions.
  The 'value' attribute is the bitmask representing the permissions.
  """

  READ = KeeFlag(0b0001, fieldName='read')
  WRITE = KeeFlag(0b0010, fieldName='write')
  EXECUTE = KeeFlag(0b0100, fieldName='execute')
  DELETE = KeeFlag(0b1000, fieldName='delete')

  def _getValue(self, ) -> bytes:
    out = 0
    for high in self.highs:
      out += 2 ** high.index
    return out.to_bytes(1, 'big')
