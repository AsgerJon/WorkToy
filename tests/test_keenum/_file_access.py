"""
FileAccess is a flags class whose members carry bytes values.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, Kee


class FileAccess(KeeFlags):
  """
  The value of a flags member is whatever the '_getValue' of the class
  that built it gives. 'FileAccess' gives each of its members its name
  in bytes, so its value type is 'bytes' and a lookup by value compares
  bytes with bytes. 'NULL' is built by 'KeeFlags', so its value is the
  text 'NULL'.
  """

  OPEN = Kee[str]()
  CLOSE = Kee[str]()

  def _getValue(self) -> bytes:
    return self.name.encode()
