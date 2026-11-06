"""
TestSpaceDesc tests 'SpaceDesc' from 'worktoy.mcls.space_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls.space_hooks import AbstractSpaceHook, SpaceDesc
from . import MclsTest, LoggingHook, LoggedSpace, LoggedMeta


class TestSpaceDesc(MclsTest):
  """
  'SpaceDesc' hands a hook the namespace it is working for: through a
  hook it returns the namespace that last read the hook, through the
  class it returns itself. The tests pin both routes, the empty state of
  a fresh hook, and the generic subscript.
  """

  def test_through_class_gives_descriptor(self) -> None:
    desc = AbstractSpaceHook.__dict__['space']
    self.assertIsInstance(desc, SpaceDesc)
    self.assertIs(AbstractSpaceHook.space, desc)
    self.assertIs(LoggingHook.space, desc)

  def test_fresh_hook_has_no_namespace(self) -> None:
    hook = LoggingHook()
    self.assertIsNone(hook.space)

  def test_through_hook_gives_namespace(self) -> None:
    space = LoggedSpace(LoggedMeta, 'A', ())
    hook = LoggedSpace.__dict__['loggingHook']
    bound = hook.__get__(space, LoggedSpace)
    self.assertIs(bound, hook)
    self.assertIs(bound.space, space)
    other = LoggedSpace(LoggedMeta, 'B', ())
    hook.__get__(other, LoggedSpace)
    self.assertIs(hook.space, other)

  def test_subscript_is_generic(self) -> None:
    alias = SpaceDesc[LoggedSpace]
    self.assertIs(alias.__origin__, SpaceDesc)
    self.assertEqual(alias.__args__, (LoggedSpace,))
