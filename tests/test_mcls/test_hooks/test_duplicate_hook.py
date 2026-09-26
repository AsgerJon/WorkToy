"""
TestDuplicateHook tests that 'DuplicateHook' is raised when a namespace
class body declares a hook at a name that a base namespace already uses
for a different hook. The hook registers itself from '__set_name__', so
the class statement itself fails, and the base keeps its own hook.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractNamespace
from worktoy.mcls.space_hooks import NamespaceHook
from worktoy.waitaminute.meta import DuplicateHook

from .. import MCLSTest


class TestDuplicateHook(MCLSTest):
  """
  TestDuplicateHook tests that 'DuplicateHook' is raised when a namespace
  class body declares a hook at a name a base namespace already uses.
  """

  def test_duplicate_hook(self) -> None:
    """
    Declaring a second 'NamespaceHook' at the name 'nameHook', which
    'AbstractNamespace' already uses, stops the class statement with
    'DuplicateHook', naming both hooks. Python 3.7 to 3.11 wrap an
    exception from '__set_name__' in 'RuntimeError', keeping the original
    as its '__cause__'.
    """
    existing = AbstractNamespace.__dict__['nameHook']
    with self.assertRaises(Exception) as context:
      class Space(AbstractNamespace):  # noqa: F841
        nameHook = NamespaceHook()
    e = context.exception.__cause__ or context.exception
    self.assertIsInstance(e, DuplicateHook)
    self.assertEqual(e.name, 'nameHook')
    self.assertIs(e.existingHook, existing)
    self.assertIsNot(e.newHook, existing)
    self.assertIsInstance(e.newHook, NamespaceHook)
    self.assertIn('nameHook', str(e))

  def test_base_keeps_its_hook(self) -> None:
    """
    After the refused declaration, the base namespace lists exactly the
    hooks it listed before.
    """
    before = AbstractNamespace.classGetHooks()
    with self.assertRaises(Exception):
      class Space(AbstractNamespace):  # noqa: F841
        nameHook = NamespaceHook()
    after = AbstractNamespace.classGetHooks()
    self.assertEqual(len(after), len(before))
    for old, new in zip(before, after):
      self.assertIs(old, new)
