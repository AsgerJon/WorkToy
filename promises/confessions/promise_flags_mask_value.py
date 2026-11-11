"""
ConfessedFlagsMaskValue confesses that the default value of a
'KeeFlags' member is not its bit mask.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase, skip

from ..keenum._file_access import FileAccess


class ConfessedFlagsMaskValue(TestCase):
  """
  Promised in 1.1.0: the 'value' of a 'KeeFlags' member is its index,
  the bit mask, unless a subclass overrides '_getValue'.

  Taken back in 1.2.0. The mask of a member is its position in one
  class, and members of a flags class and of its subclass with the same
  flags are promised to be equal. With two flags classes as bases the
  same flag sits at another bit in the subclass, so two equal members
  held different values, 1 and 2. A value taken from a position
  contradicts equality, and equality is the promise that was kept.

  What '_getValue' gives when a subclass overrides it is still owed, in
  'promises/keenum/promise_flags.py'.
  """

  @skip('Confessed in 1.2.0: the default value is not the bit mask.')
  def test_value_is_the_mask(self) -> None:
    self.assertEqual(FileAccess.READ_EXECUTE.value, 5)
