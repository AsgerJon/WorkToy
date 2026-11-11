"""
The private file '_file_access' holds 'FileAccess', a flags class
defined at the top of a file, as pickling requires.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag


class FileAccess(KeeFlags):
  """
  'FileAccess' is the permissions of a file.
  """

  READ = KeeFlag()
  WRITE = KeeFlag()
  EXECUTE = KeeFlag()
