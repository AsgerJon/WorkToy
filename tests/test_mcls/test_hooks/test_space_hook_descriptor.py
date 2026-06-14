"""
TestSpaceHookDescriptor covers class-level access of an
'AbstractSpaceHook'. Reading a hook through the namespace class (rather
than a namespace instance) takes the 'instance is None' branch of
'__get__', which returns the hook descriptor itself without rebinding
'__space_object__'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractNamespace
from worktoy.mcls.space_hooks import NamespaceHook, AbstractSpaceHook
from . import SpaceHookTest


class TestSpaceHookDescriptor(SpaceHookTest):
  """
  TestSpaceHookDescriptor pins the class-level '__get__' of an
  'AbstractSpaceHook': accessed on the namespace class, the descriptor
  returns itself.
  """

  def test_class_level_get_returns_hook(self) -> None:
    """Accessing a hook on the namespace class returns the hook itself."""
    hook = AbstractNamespace.nameHook
    self.assertIsInstance(hook, NamespaceHook)
    self.assertIsInstance(hook, AbstractSpaceHook)
