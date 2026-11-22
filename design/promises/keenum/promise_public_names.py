"""
PromisePublicNames promises the names 'worktoy.keenum' exports.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

import worktoy.keenum


class PromisePublicNames(TestCase):
  """
  'KeeNum', 'Kee', 'KeeFlags', 'KeeFlag', 'KeeBox', 'AccessNum' and the
  machinery behind them import from 'worktoy.keenum'. Source: '__all__'
  of the package.
  """

  def test_names(self) -> None:
    names = ('Kee', 'KeeBase', 'KeeFlag', 'KeeSpaceHook', 'KeeFlagsHook',
             'KeeSpace', 'KeeMetaMeta', 'KeeMeta', 'KeeNum',
             'KeeFlagsSpace', 'KeeFlagsMeta', 'KeeFlags', 'KeeBox',
             'AccessNum')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.keenum, name))
