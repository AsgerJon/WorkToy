"""
TestKeenumPackage tests the public face of 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy import keenum
from worktoy.keenum import KeeMeta, KeeNum, KeeFlagsMeta, KeeFlags
from worktoy.keenum import KeeSpace, KeeFlagsSpace, KeeBox
from worktoy.mcls import BaseMeta, BaseSpace
from worktoy.desc import AttriBox
from . import KeenumTest


class TestKeenumPackage(KeenumTest):
  """
  The package exports fourteen names across the two enumeration
  systems and the shared pieces. The tests pin the exports and the
  layering on 'worktoy.mcls' and 'worktoy.desc'.
  """

  def test_exports(self) -> None:
    expected = (
      'Kee', 'KeeBase', 'KeeFlag', 'KeeSpaceHook', 'KeeFlagsHook',
      'KeeSpace', 'KeeMetaMeta', 'KeeMeta', 'KeeNum', 'KeeFlagsSpace',
      'KeeFlagsMeta', 'KeeFlags', 'KeeBox', 'AccessNum',
    )
    self.assertEqual(keenum.__all__, expected)
    for name in expected:
      with self.subTest(name=name):
        self.assertTrue(hasattr(keenum, name))

  def test_layering(self) -> None:
    self.assertIsSubclass(KeeMeta, BaseMeta)
    self.assertIsSubclass(KeeFlagsMeta, BaseMeta)
    self.assertIsSubclass(KeeSpace, BaseSpace)
    self.assertIsSubclass(KeeFlagsSpace, BaseSpace)
    self.assertIsSubclass(KeeBox, AttriBox)
    self.assertIs(type(KeeNum), KeeMeta)
    self.assertIs(type(KeeFlags), KeeFlagsMeta)
    self.assertIs(KeeMeta.getNamespaceClass(), KeeSpace)
    self.assertIs(KeeFlagsMeta.getNamespaceClass(), KeeFlagsSpace)
