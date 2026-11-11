"""
DeprecatedOldControlFlowPath holds the promise of the names of
'worktoy.waitaminute.control_flow', which ends at the next major
update.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import warnings
from unittest import TestCase

import worktoy.core.control_flow
import worktoy.waitaminute.control_flow


class DeprecatedOldControlFlowPath(TestCase):
  """
  Deprecated in 1.2.0: importing the control-flow signals from
  'worktoy.waitaminute.control_flow'.

  Promised for the 1.x releases: 'ControlSpace', 'MetaFlow',
  'ControlFlow' and 'SkipSet' import from the old package as the same
  objects 'worktoy.core.control_flow' holds.

  Why it ends: a signal is a stateless class used by its type, as a
  sentinel is used by its identity, and is no exception. The signals
  moved beside the sentinels in 'worktoy.core', and the old package
  stayed as a re-export. The new home is promised in
  'promises/core/promise_public_names.py'.
  """

  def setUp(self) -> None:
    silenced = warnings.catch_warnings()
    silenced.__enter__()
    self.addCleanup(silenced.__exit__, None, None, None)
    warnings.simplefilter('ignore')

  def test_old_control_flow_path(self) -> None:
    old = worktoy.waitaminute.control_flow
    new = worktoy.core.control_flow
    for name in ('ControlSpace', 'MetaFlow', 'ControlFlow', 'SkipSet'):
      with self.subTest(name=name):
        self.assertIs(getattr(old, name), getattr(new, name))
