"""
FlagsExample provides an example of the use of the KeeFlags class used to
run the tests contained in the 'tests.test_keenum' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, Kee


class FlagsExample(KeeFlags):
  """
  FlagsExample is an example of the use of the KeeFlags class.
  It defines a set of flags with specific values.
  """

  NEVER = Kee[int](69)
  GONNA = Kee[int](420)
  GIVE = Kee[int](1337)
  YOU = Kee[int](80085)
  UP = Kee[int](8008135)


class FileAccess(KeeFlags):
  """
  FileAccess demonstrates real-world bitmask flags for file permissions.
  """
  READ = Kee[int](0b0001)
  WRITE = Kee[int](0b0010)
  EXECUTE = Kee[int](0b0100)
  DELETE = Kee[int](0b1000)
