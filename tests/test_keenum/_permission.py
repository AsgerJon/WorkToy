"""
Permission is a flags class of three flags.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag


class Permission(KeeFlags):
  """
  The everyday flags class: three single-bit flags, eight members from
  'NULL' to 'READ_WRITE_EXEC', values equal to the indices. 'Permission'
  is importable, so its members pickle by name.
  """

  READ = KeeFlag()
  WRITE = KeeFlag()
  EXEC = KeeFlag()
