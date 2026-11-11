"""
Permission is a flags class of three flags.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, Kee


class Permission(KeeFlags):
  """
  The everyday flags class: three flags declared with 'Kee', eight
  members from 'NULL' to 'READ_WRITE_EXEC', each valued by its name.
  'Permission' is importable, so its members pickle by name.
  """

  READ = Kee[str]()
  WRITE = Kee[str]()
  EXEC = Kee[str]()
