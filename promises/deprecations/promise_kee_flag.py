"""
DeprecatedKeeFlag holds the promise of 'KeeFlag' from 'worktoy.keenum',
which ends at the next major update.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import warnings
from unittest import TestCase

from worktoy.keenum import KeeFlags, KeeFlag


class DeprecatedKeeFlag(TestCase):
  """
  Deprecated in 1.2.0: 'KeeFlag', the declaration of a flag.

  Promised in 1.1.0 and owed through 1.x: a 'KeeFlags' class with N
  flags declared as 'READ = KeeFlag()' holds one member for each
  combination of them, 2 ** N, 'NULL' included.

  Why it ends: 'KeeFlags' is built the way 'KeeNum' is since 1.2.0, and
  a declaration of its own for flags is no longer needed. What is
  written in its place is not promised yet. Everything else promised of
  a flags class is in 'promises/keenum/promise_flags.py', whose classes
  declare their flags with 'KeeFlag' until then.
  """

  def setUp(self) -> None:
    silenced = warnings.catch_warnings()
    silenced.__enter__()
    self.addCleanup(silenced.__exit__, None, None, None)
    warnings.simplefilter('ignore')

  def test_declares_flags(self) -> None:
    class Access(KeeFlags):
      READ = KeeFlag()
      WRITE = KeeFlag()

    self.assertEqual(len(Access), 4)
    self.assertEqual([m.name for m in Access],
                     ['NULL', 'READ', 'WRITE', 'READ_WRITE'])
