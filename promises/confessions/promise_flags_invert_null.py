"""
ConfessedFlagsInvertNull confesses that '~' of the 'NULL' member of a
'KeeFlags' class does not give the member with every flag.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase, skip

from ..keenum._file_access import FileAccess


class ConfessedFlagsInvertNull(TestCase):
  """
  Promised in 1.1.0: '~' gives a member, the one whose flags are those
  the operand lacks, so '~' of 'NULL' is the member with every flag of
  the class.

  Taken back in 1.2.0. 'NULL' is the member with no flag, and it stands
  for no flag in every flags class alike. Which flags it lacks depends
  on the class asked, and the member alone does not say which class
  that is, so there is no one member for '~' of 'NULL' to give. '~' of
  every other member is still owed, in
  'promises/keenum/promise_flags.py'.
  """

  @skip("Confessed in 1.2.0: '~' of 'NULL' gives no member.")
  def test_invert_null(self) -> None:
    self.assertIs(~FileAccess.NULL, FileAccess.READ_WRITE_EXECUTE)
