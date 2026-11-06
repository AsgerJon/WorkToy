"""
TestEzdataPackage tests the public face of 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy import ezdata
from worktoy.core import Object
from worktoy.mcls import BaseMeta, BaseSpace
from worktoy.mcls.space_hooks import AbstractSpaceHook
from . import EzdataTest


class TestEzdataPackage(EzdataTest):
  """
  The package exports the field, the store, the hook, the namespace,
  the metaclass, the base and the 'fields' function. The tests pin the
  exports and the layering on 'worktoy.mcls' and 'worktoy.core'.
  """

  def test_exports(self) -> None:
    expected = (
      'EZField', 'EZStore', 'EZHook', 'EZSpace', 'EZMeta', 'EZData',
      'fields',
    )
    self.assertEqual(ezdata.__all__, expected)
    for name in expected:
      with self.subTest(name=name):
        self.assertTrue(hasattr(ezdata, name))

  def test_layering(self) -> None:
    self.assertIsSubclass(ezdata.EZMeta, BaseMeta)
    self.assertIsSubclass(ezdata.EZSpace, BaseSpace)
    self.assertIsSubclass(ezdata.EZHook, AbstractSpaceHook)
    self.assertIsSubclass(ezdata.EZData, Object)
    self.assertIs(type(ezdata.EZData), ezdata.EZMeta)
    self.assertIs(ezdata.EZMeta.getNamespaceClass(), ezdata.EZSpace)
    self.assertIs(ezdata.EZSpace.classGetHooks()[-1],
                  ezdata.EZSpace.__dict__['ezHook'])
    self.assertEqual(ezdata.EZData.fields, ())
    self.assertEqual(len(ezdata.EZData), 0)
