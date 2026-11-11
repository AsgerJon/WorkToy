"""
PromisePublicNames promises the names 'worktoy.mcls' exports.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

import worktoy.mcls
import worktoy.mcls.space_hooks


class PromisePublicNames(TestCase):
  """
  'BaseObject', 'BaseMeta', 'BaseSpace', 'AbstractMetaclass' and
  'AbstractNamespace' import from 'worktoy.mcls', and the namespace
  hooks from 'worktoy.mcls.space_hooks'. Source: '__all__' of both
  packages.
  """

  def test_mcls(self) -> None:
    names = ('space_hooks', 'AbstractNamespace', 'AbstractMetaclass',
             'BaseSpace', 'BaseMeta', 'BaseObject')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.mcls, name))

  def test_space_hooks(self) -> None:
    names = ('SpaceDesc', 'ReservedNames', 'AbstractSpaceHook',
             'FlexCallHook', 'ReservedNamespaceHook', 'NamespaceHook',
             'LoadSpaceHook')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.mcls.space_hooks, name))
