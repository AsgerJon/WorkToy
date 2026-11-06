"""
TestMclsPackage tests the public face of 'worktoy.mcls'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy import mcls
from worktoy.core import MetaType, Object
from worktoy.core._meta_type import _Chill
from worktoy.mcls import space_hooks
from . import MclsTest


class TestMclsPackage(MclsTest):
  """
  The package exports the abstract namespace and metaclass, 'BaseSpace',
  'BaseMeta', 'BaseObject' and the 'space_hooks' package, and the hooks
  package exports its seven names. The tests pin the exports and the
  layering: every metaclass of the package is built by 'MetaType', and
  'BaseObject' ends its resolution order as every worktoy class does.
  """

  def test_exports(self) -> None:
    expected = [
      'space_hooks', 'AbstractNamespace', 'AbstractMetaclass',
      'BaseSpace', 'BaseMeta', 'BaseObject',
    ]
    self.assertEqual(mcls.__all__, expected)
    for name in expected:
      with self.subTest(name=name):
        self.assertTrue(hasattr(mcls, name))

  def test_hook_exports(self) -> None:
    expected = [
      'SpaceDesc', 'ReservedNames', 'AbstractSpaceHook', 'FlexCallHook',
      'ReservedNamespaceHook', 'NamespaceHook', 'LoadSpaceHook',
    ]
    self.assertEqual(space_hooks.__all__, expected)
    for name in expected:
      with self.subTest(name=name):
        self.assertTrue(hasattr(space_hooks, name))

  def test_layering(self) -> None:
    self.assertIs(type(mcls.AbstractMetaclass), MetaType)
    self.assertIs(type(mcls.BaseMeta), MetaType)
    self.assertIsSubclass(mcls.BaseMeta, mcls.AbstractMetaclass)
    self.assertIsSubclass(mcls.AbstractMetaclass, MetaType)
    self.assertIsSubclass(mcls.BaseSpace, mcls.AbstractNamespace)
    self.assertIsSubclass(mcls.AbstractNamespace, dict)
    self.assertIs(type(mcls.BaseObject), mcls.BaseMeta)
    self.assertEqual(mcls.BaseObject.__mro__[-3:], (Object, _Chill, object))
    self.assertTrue(mcls.AbstractMetaclass.__abstract_metaclass__)
    self.assertTrue(mcls.BaseMeta.__abstract_metaclass__)
