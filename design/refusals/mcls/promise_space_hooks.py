"""
RefusedSpaceHooks holds the refusals that belong with
'design.promises.mcls.promise_space_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import BaseSpace
from worktoy.mcls.space_hooks import LoadSpaceHook
from worktoy.waitaminute.meta import DuplicateHook


class RefusedSpaceHooks(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.3.0. A namespace class declaring a hook at a name an inherited
  hook already has raises 'DuplicateHook' as the namespace class is
  created, wrapped in 'RuntimeError' before Python 3.12, so an inherited
  hook is neither replaced nor moved that way. Source: the
  'AbstractNamespace' docstring and section 6 of the mcls part of
  'design/manual.md'.
  """

  def test_hook_at_an_inherited_name(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Replacing(BaseSpace):
        loadSpaceHook = LoadSpaceHook()
    self.assertIsInstance(refused.exception, (DuplicateHook, RuntimeError))
