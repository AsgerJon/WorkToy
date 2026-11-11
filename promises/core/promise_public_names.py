"""
PromisePublicNames promises the names 'worktoy.core' exports.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

import worktoy.core
import worktoy.core.control_flow
import worktoy.core.sentinels


class PromisePublicNames(TestCase):
  """
  'MetaType', 'Object', 'ContextInstance' and 'ContextOwner' import
  from 'worktoy.core', the sentinels from 'worktoy.core.sentinels' and
  the control-flow signals from 'worktoy.core.control_flow'. The signals
  lived in 'worktoy.waitaminute.control_flow' before; that path is
  deprecated, with its reason in 'promises/deprecations'. Source:
  '__all__' of the three packages, and the 'worktoy.core.control_flow'
  docstring.
  """

  def test_core(self) -> None:
    names = ('MetaType', 'Object', 'ContextInstance', 'ContextOwner',
             'sentinels', 'control_flow')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.core, name))

  def test_sentinels(self) -> None:
    names = ('Sentinel', 'SentinelMeta', 'DELETED', 'OWNER', 'THIS', 'DESC',
             'METACALL', 'ARGS')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.core.sentinels, name))

  def test_control_flow(self) -> None:
    names = ('ControlSpace', 'MetaFlow', 'ControlFlow', 'SkipSet')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.core.control_flow, name))
